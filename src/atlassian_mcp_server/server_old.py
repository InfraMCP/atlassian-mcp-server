"""Atlassian MCP Server with seamless OAuth 2.0 flow for Jira and Confluence."""

import asyncio
import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel


class AtlassianConfig(BaseModel):
    """Configuration for Atlassian Cloud connection."""
    site_url: str
    client_id: str
    client_secret: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback automatically."""
    
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse the callback URL
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            
            # Store the callback data for processing
            self.server.callback_data = {
                'code': query_params.get('code', [None])[0],
                'state': query_params.get('state', [None])[0],
                'error': query_params.get('error', [None])[0]
            }
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if self.server.callback_data['error']:
                html = f"""
                <html><body>
                <h1>❌ Authorization Failed</h1>
                <p>Error: {self.server.callback_data['error']}</p>
                <p>You can close this window.</p>
                </body></html>
                """
            else:
                html = """
                <html><body>
                <h1>✅ Authorization Successful!</h1>
                <p>You can close this window. The MCP server will continue automatically.</p>
                <script>setTimeout(() => window.close(), 3000);</script>
                </body></html>
                """
            
            self.wfile.write(html.encode())
            
            # Signal that we got the callback
            self.server.callback_received = True
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        # Suppress server logs
        pass


class AtlassianClient:
    """HTTP client for Atlassian Cloud APIs with OAuth 2.0 flow."""
    
    def __init__(self, config: AtlassianConfig):
        self.config = config
        self.client = httpx.AsyncClient()
        self.credentials_file = Path.home() / ".atlassian_mcp_credentials.json"
    
    def generate_pkce_pair(self) -> tuple[str, str]:
        """Generate PKCE code verifier and challenge."""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    async def start_oauth_flow(self) -> str:
        """Start OAuth 2.0 authorization code flow with PKCE."""
        code_verifier, code_challenge = self.generate_pkce_pair()
        state = secrets.token_urlsafe(32)
        redirect_uri = "http://localhost:8080/callback"
        
        # Store session data
        session = OAuthSession(
            state=state,
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            redirect_uri=redirect_uri
        )
        
        # Save session to file with state as filename
        session_file = Path.home() / f".atlassian_oauth_session_{state}.json"
        with open(session_file, 'w') as f:
            json.dump(session.dict(), f)
        
        # Build authorization URL
        params = {
            "audience": "api.atlassian.com",
            "client_id": self.config.client_id,
            "scope": "read:page:confluence write:page:confluence offline_access",
            "redirect_uri": redirect_uri,
            "state": state,
            "response_type": "code",
            "prompt": "consent",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }
        
        auth_url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"
        return auth_url
    
    async def handle_callback(self, callback_url: str) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for tokens."""
        # Parse callback URL
        parsed = urlparse(callback_url)
        query_params = parse_qs(parsed.query)
        
        if 'error' in query_params:
            raise ValueError(f"OAuth error: {query_params['error'][0]}")
        
        code = query_params.get('code', [None])[0]
        state = query_params.get('state', [None])[0]
        
        if not code or not state:
            raise ValueError("Missing code or state in callback")
        
        # Load session data
        session_file = Path.home() / f".atlassian_oauth_session_{state}.json"
        if not session_file.exists():
            raise ValueError("OAuth session not found")
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        session = OAuthSession(**session_data)
        
        if session.state != state:
            raise ValueError("Invalid state parameter")
        
        # Exchange code for tokens
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "code": code,
            "redirect_uri": session.redirect_uri,
            "code_verifier": session.code_verifier
        }
        
        response = await self.client.post(
            "https://auth.atlassian.com/oauth/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()
        
        tokens = response.json()
        
        # Save credentials
        credentials = {
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "site_url": self.config.site_url,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret
        }
        
        with open(self.credentials_file, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        # Set file permissions
        self.credentials_file.chmod(0o600)
        
        # Clean up session file
        session_file.unlink(missing_ok=True)
        
        # Update config
        self.config.access_token = tokens["access_token"]
        self.config.refresh_token = tokens.get("refresh_token")
        
        # Save credentials immediately
        self.save_credentials_to_config()
        
        return tokens
    
    def save_credentials_to_config(self):
        """Save current tokens to config for persistence."""
        credentials = {
            "access_token": self.config.access_token,
            "refresh_token": self.config.refresh_token,
            "site_url": self.config.site_url,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret
        }
        
        with open(self.credentials_file, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        # Set file permissions
        self.credentials_file.chmod(0o600)
    
    def load_credentials(self) -> bool:
        """Load saved credentials."""
        if not self.credentials_file.exists():
            return False
        
        try:
            with open(self.credentials_file, 'r') as f:
                creds = json.load(f)
            
            self.config.access_token = creds.get("access_token")
            self.config.refresh_token = creds.get("refresh_token")
            self.config.site_url = creds.get("site_url", self.config.site_url)
            
            return bool(self.config.access_token)
        except Exception:
            return False
    
    async def refresh_access_token(self) -> bool:
        """Refresh access token using refresh token."""
        if not self.config.refresh_token:
            return False
        
        token_data = {
            "grant_type": "refresh_token",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "refresh_token": self.config.refresh_token
        }
        
        try:
            response = await self.client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            
            tokens = response.json()
            self.config.access_token = tokens["access_token"]
            
            # Save refreshed token
            self.save_credentials_to_config()
            
            return True
        except Exception:
            return False
    
    async def get_headers(self) -> Dict[str, str]:
        """Get authenticated headers."""
        if not self.config.access_token:
            raise ValueError("No access token available. Please authenticate first.")
        
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    async def make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make authenticated request with automatic token refresh and re-auth."""
        headers = await self.get_headers()
        kwargs.setdefault('headers', {}).update(headers)
        
        response = await self.client.request(method, url, **kwargs)
        
        # Try to refresh token if unauthorized
        if response.status_code == 401 and self.config.refresh_token:
            if await self.refresh_access_token():
                # Save refreshed tokens
                self.save_credentials_to_config()
                headers = await self.get_headers()
                kwargs['headers'].update(headers)
                response = await self.client.request(method, url, **kwargs)
        
        # If still unauthorized, trigger re-authentication
        if response.status_code == 401:
            print("🔐 Session expired, please re-authenticate using authenticate_atlassian tool")
            raise ValueError("Authentication required - use authenticate_atlassian tool")
        
        response.raise_for_status()
        return response
    
    async def get_cloud_id(self) -> str:
        """Get the cloud ID for the configured site."""
        url = "https://api.atlassian.com/oauth/token/accessible-resources"
        response = await self.make_request("GET", url)
        resources = response.json()
        
        for resource in resources:
            if resource["url"] == self.config.site_url:
                return resource["id"]
        
        raise ValueError(f"Site {self.config.site_url} not found in accessible resources")
    
    async def confluence_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Confluence content."""
        url = f"{self.config.site_url}/wiki/api/v2/pages"
        params = {"limit": limit}
        
        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])
    
    async def confluence_get_page(self, page_id: str) -> Dict[str, Any]:
        """Get Confluence page content."""
        url = f"{self.config.site_url}/wiki/api/v2/pages/{page_id}"
        params = {"body-format": "storage"}
        
        response = await self.make_request("GET", url, params=params)
        return response.json()
    
    async def jira_search(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search Jira issues."""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/search"
        data = {"jql": jql, "maxResults": max_results}
        
        response = await self.make_request("POST", url, json=data)
        return response.json().get("issues", [])
    
    async def jira_get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get Jira issue details."""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/issue/{issue_key}"
        
        response = await self.make_request("GET", url)
        return response.json()
    
    async def confluence_create_page(self, space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Confluence page."""
        url = f"{self.config.site_url}/wiki/api/v2/pages"
        
        data = {
            "spaceId": space_key,  # v2 API uses spaceId instead of space.key
            "title": title,
            "body": {
                "representation": "storage",
                "value": content
            }
        }
        
        if parent_id:
            data["parentId"] = parent_id  # v2 API uses parentId instead of ancestors
        
        response = await self.make_request("POST", url, json=data)
        return response.json()
    
    async def confluence_update_page(self, page_id: str, title: str, content: str, version: int) -> Dict[str, Any]:
        """Update an existing Confluence page."""
        url = f"{self.config.site_url}/wiki/api/v2/pages/{page_id}"
        
        data = {
            "version": {"number": version + 1},
            "title": title,
            "body": {
                "representation": "storage",
                "value": content
            }
        }
        
        response = await self.make_request("PUT", url, json=data)
        return response.json()
    
    async def jira_create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        """Create a new Jira issue."""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/issue"
        
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        response = await self.make_request("POST", url, json=data)
        return response.json()
    
    async def jira_update_issue(self, issue_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Update a Jira issue."""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/issue/{issue_key}"
        
        fields = {}
        if summary:
            fields["summary"] = summary
        if description:
            fields["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            }
        
        data = {"fields": fields}
        response = await self.make_request("PUT", url, json=data)
        return {"success": True}


# Initialize MCP server
mcp = FastMCP("Atlassian Cloud")

# Global client instance
atlassian_client: Optional[AtlassianClient] = None


@mcp.tool()
async def test_auth() -> List[Dict[str, Any]]:
    """Test authentication by getting accessible resources."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    
    url = "https://api.atlassian.com/oauth/token/accessible-resources"
    response = await atlassian_client.make_request("GET", url)
    return response.json()


@mcp.tool()
async def confluence_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search Confluence pages and content."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_search(query, limit)


@mcp.tool()
async def confluence_get_page(page_id: str) -> Dict[str, Any]:
    """Get a specific Confluence page by ID."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_get_page(page_id)


@mcp.tool()
async def jira_search(jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """Search Jira issues using JQL."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_search(jql, max_results)


@mcp.tool()
async def jira_get_issue(issue_key: str) -> Dict[str, Any]:
    """Get a specific Jira issue by key."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_get_issue(issue_key)


@mcp.tool()
async def confluence_create_page(space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new Confluence page."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    return await atlassian_client.confluence_create_page(space_key, title, content, parent_id)


@mcp.tool()
async def confluence_update_page(page_id: str, title: str, content: str, version: int) -> Dict[str, Any]:
    """Update an existing Confluence page."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    return await atlassian_client.confluence_update_page(page_id, title, content, version)


@mcp.tool()
async def jira_create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
    """Create a new Jira issue."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    return await atlassian_client.jira_create_issue(project_key, summary, description, issue_type)


@mcp.tool()
async def jira_update_issue(issue_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Update a Jira issue."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    return await atlassian_client.jira_update_issue(issue_key, summary, description)


async def initialize_client():
    """Initialize the Atlassian client and handle OAuth if needed."""
    global atlassian_client
    
    site_url = os.getenv("ATLASSIAN_SITE_URL")
    client_id = os.getenv("ATLASSIAN_CLIENT_ID")
    client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
    
    if not all([site_url, client_id, client_secret]):
        raise ValueError("ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, and ATLASSIAN_CLIENT_SECRET must be set")
    
    config = AtlassianConfig(
        site_url=site_url,
        client_id=client_id,
        client_secret=client_secret
    )
    
    atlassian_client = AtlassianClient(config)
    
    # Try to load existing credentials
    if atlassian_client.load_credentials():
        print("✅ Loaded existing Atlassian credentials")
        # Test if credentials still work
        try:
            headers = await atlassian_client.get_headers()
            print("✅ Credentials are valid")
        except Exception:
            print("⚠️ Stored credentials are invalid. Use authenticate_atlassian tool to re-authenticate.")
    else:
        print("🔐 No existing credentials found. Use authenticate_atlassian tool to authenticate.")


@mcp.tool()
async def authenticate_atlassian() -> str:
    """Start Atlassian OAuth authentication flow."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    
    auth_url = await atlassian_client.start_oauth_flow()
    
    # Open browser automatically
    webbrowser.open(auth_url)
    
    return f"🌐 Browser opened for authentication.\n📋 Visit: {auth_url}\n\n⚠️ After authorizing, you'll see a 'can't connect' error - this is normal.\n📝 Copy the full callback URL and use complete_authentication tool."


@mcp.tool()
async def complete_authentication(callback_url: str) -> str:
    """Complete OAuth authentication with callback URL."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    
    try:
        tokens = await atlassian_client.handle_callback(callback_url)
        return "✅ Authentication successful! You can now use Atlassian tools."
    except Exception as e:
        return f"❌ Authentication failed: {str(e)}"


def main():
    """Main entry point."""
    try:
        # Initialize client with OAuth
        asyncio.run(initialize_client())
        
        # Run MCP server
        mcp.run()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1


if __name__ == "__main__":
    main()
