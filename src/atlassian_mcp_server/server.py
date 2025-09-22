"""Atlassian MCP Server with seamless OAuth 2.0 flow for Jira and Confluence."""

import asyncio
import base64
import hashlib
import json
import logging
import os
import secrets
import sys
import threading
import time
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

# Configure logging to both stderr and file
log_file = Path.home() / ".atlassian-mcp-debug.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

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
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            
            self.server.callback_data = {
                'code': query_params.get('code', [None])[0],
                'state': query_params.get('state', [None])[0],
                'error': query_params.get('error', [None])[0]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if self.server.callback_data['error']:
                html = f"""<html><body><h1>❌ Authorization Failed</h1><p>Error: {self.server.callback_data['error']}</p></body></html>"""
            else:
                html = """<html><body><h1>✅ Authorization Successful!</h1><p>You can close this window.</p><script>setTimeout(() => window.close(), 3000);</script></body></html>"""
            
            self.wfile.write(html.encode())
            self.server.callback_received = True
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass


class AtlassianClient:
    """HTTP client for Atlassian Cloud APIs with seamless OAuth 2.0 flow."""
    
    def __init__(self, config: AtlassianConfig):
        self.config = config
        self.client = httpx.AsyncClient()
        self.credentials_file = Path.home() / ".atlassian_mcp_credentials.json"
        self.server = None
        self.server_thread = None
    
    def generate_pkce(self):
        """Generate PKCE codes"""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def start_callback_server(self):
        """Start the callback server"""
        self.server = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
        self.server.callback_received = False
        self.server.callback_data = None
        
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def stop_callback_server(self):
        """Stop the callback server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            if self.server_thread:
                self.server_thread.join(timeout=1)
    
    async def seamless_oauth_flow(self):
        """Complete OAuth flow with automatic callback handling"""
        # Start callback server
        self.start_callback_server()
        
        try:
            # Generate PKCE
            code_verifier, code_challenge = self.generate_pkce()
            state = secrets.token_urlsafe(32)
            
            # Minimal required scopes for MCP functionality
            scopes = [
                # Jira - Essential for ticket operations
                "read:jira-work",                    # Read issues, projects
                "read:jira-user",                    # Read user info
                "write:jira-work",                   # Create/update issues
                
                # Confluence - Essential for content operations  
                "read:confluence-content.all",       # Read all content
                "search:confluence",                 # Search functionality
                "read:confluence-space.summary",     # Space info
                "write:confluence-content",          # Create/update pages
                
                # Service Management - For support context
                "read:servicedesk-request",          # Read SM tickets
                
                # Core
                "read:me",                           # User profile
                "offline_access"                     # Token refresh
            ]
            
            params = {
                "audience": "api.atlassian.com",
                "client_id": self.config.client_id,
                "scope": " ".join(scopes),
                "redirect_uri": "http://localhost:8080/callback",
                "state": state,
                "response_type": "code",
                "prompt": "consent"
            }
            
            auth_url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"
            
            print("🚀 Starting Atlassian OAuth authentication...")
            print("🌐 Opening browser for authorization...")
            webbrowser.open(auth_url)
            
            # Wait for callback
            timeout = 300  # 5 minutes
            start_time = time.time()
            
            while not self.server.callback_received:
                if time.time() - start_time > timeout:
                    raise TimeoutError("Authorization timed out after 5 minutes")
                await asyncio.sleep(0.5)
            
            callback_data = self.server.callback_data
            
            if callback_data['error']:
                raise ValueError(f"OAuth error: {callback_data['error']}")
            
            if callback_data['state'] != state:
                raise ValueError("Invalid state parameter")
            
            print("✅ Authorization received, exchanging for tokens...")
            
            # Exchange code for tokens
            token_data = {
                "grant_type": "authorization_code",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "code": callback_data['code'],
                "redirect_uri": "http://localhost:8080/callback"
            }
            
            response = await self.client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                raise ValueError(f"Token exchange failed: {response.text}")
            
            tokens = response.json()
            
            # Save tokens
            self.config.access_token = tokens["access_token"]
            self.config.refresh_token = tokens.get("refresh_token")
            self.save_credentials()
            
            print("✅ OAuth flow completed successfully!")
            return tokens
                
        finally:
            self.stop_callback_server()
    
    def save_credentials(self):
        """Save credentials to file"""
        credentials = {
            "access_token": self.config.access_token,
            "refresh_token": self.config.refresh_token,
            "site_url": self.config.site_url,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret
        }
        
        with open(self.credentials_file, 'w') as f:
            json.dump(credentials, f, indent=2)
        self.credentials_file.chmod(0o600)
    
    def load_credentials(self) -> bool:
        """Load saved credentials"""
        if not self.credentials_file.exists():
            return False
        
        try:
            with open(self.credentials_file, 'r') as f:
                creds = json.load(f)
            
            self.config.access_token = creds.get("access_token")
            self.config.refresh_token = creds.get("refresh_token")
            return bool(self.config.access_token)
        except Exception:
            return False
    
    async def refresh_access_token(self) -> bool:
        """Refresh access token using refresh token"""
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
            self.save_credentials()
            return True
        except Exception:
            return False
    
    async def get_headers(self) -> Dict[str, str]:
        """Get authenticated headers"""
        if not self.config.access_token:
            raise ValueError("No access token available. Please authenticate first.")
        
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    async def make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make authenticated request with automatic token refresh"""
        headers = await self.get_headers()
        kwargs.setdefault('headers', {}).update(headers)
        
        response = await self.client.request(method, url, **kwargs)
        
        # Try to refresh token if unauthorized
        if response.status_code == 401 and self.config.refresh_token:
            if await self.refresh_access_token():
                headers = await self.get_headers()
                kwargs['headers'].update(headers)
                response = await self.client.request(method, url, **kwargs)
        
        # If still unauthorized, need re-authentication
        if response.status_code == 401:
            raise ValueError("Authentication required - use authenticate_atlassian tool")
        
        response.raise_for_status()
        return response
    
    async def get_cloud_id(self) -> str:
        """Get the cloud ID for the configured site"""
        url = "https://api.atlassian.com/oauth/token/accessible-resources"
        response = await self.make_request("GET", url)
        resources = response.json()
        
        logger.debug(f"Accessible resources: {resources}")
        logger.debug(f"Looking for site: {self.config.site_url}")
        
        for resource in resources:
            logger.debug(f"Checking resource: {resource}")
            if resource["url"] == self.config.site_url:
                logger.debug(f"Found matching site, cloud_id: {resource['id']}")
                return resource["id"]
        
        raise ValueError(f"Site {self.config.site_url} not found in accessible resources")
    
    # Jira Methods
    async def jira_search(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Search Jira issues using JQL"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/search"
        data = {"jql": jql, "maxResults": max_results, "fields": ["summary", "status", "assignee", "priority", "issuetype", "description"]}
        
        response = await self.make_request("POST", url, json=data)
        return response.json().get("issues", [])
    
    async def jira_get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get Jira issue details"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/issue/{issue_key}"
        
        response = await self.make_request("GET", url)
        return response.json()
    
    async def jira_create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        """Create a new Jira issue"""
        cloud_id = await self.get_cloud_id()
        
        # First get valid issue types for the project
        project_url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/project/{project_key}"
        project_response = await self.make_request("GET", project_url)
        project_data = project_response.json()
        
        # Find the issue type (use first available if specified type not found)
        issue_types = project_data.get('issueTypes', [])
        issue_type_id = None
        
        for it in issue_types:
            if it['name'].lower() == issue_type.lower():
                issue_type_id = it['id']
                break
        
        if not issue_type_id and issue_types:
            issue_type_id = issue_types[0]['id']  # Use first available
        
        if not issue_type_id:
            raise ValueError(f"No valid issue types found for project {project_key}")
        
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/issue"
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
                "issuetype": {"id": issue_type_id}
            }
        }
        
        response = await self.make_request("POST", url, json=data)
        return response.json()
    
    async def jira_update_issue(self, issue_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Update a Jira issue"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/issue/{issue_key}"
        
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
        return {"success": True, "issue_key": issue_key}
    
    async def jira_add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a Jira issue"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/issue/{issue_key}/comment"
        
        data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }
        
        response = await self.make_request("POST", url, json=data)
        return response.json()
    
    # Confluence Methods
    async def confluence_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Confluence content using CQL"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search"
        params = {"cql": f"type=page AND title~'{query}'", "limit": limit, "expand": "content.body.storage,content.space"}
        
        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])
    
    async def confluence_get_page(self, page_id: str) -> Dict[str, Any]:
        """Get Confluence page content"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search"
        params = {"cql": f"type=page AND id={page_id}", "expand": "content.body.storage,content.space,content.version"}
        
        response = await self.make_request("GET", url, params=params)
        results = response.json().get("results", [])
        
        if results:
            return results[0].get("content", {})
        else:
            raise ValueError(f"Page {page_id} not found")
    
    async def confluence_create_page(self, space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Confluence page"""
        try:
            cloud_id = await self.get_cloud_id()
            
            # Debug: Check accessible resources and scopes
            resources_url = "https://api.atlassian.com/oauth/token/accessible-resources"
            resources_response = await self.make_request("GET", resources_url)
            resources_data = resources_response.json()
            
            # Get space ID from space key using v2 API
            space_url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/spaces"
            space_response = await self.make_request("GET", space_url, params={"keys": space_key})
            spaces = space_response.json().get("results", [])
            if not spaces:
                return {
                    "error": f"Space with key '{space_key}' not found",
                    "debug_info": {
                        "cloud_id": cloud_id,
                        "accessible_resources": resources_data,
                        "space_lookup_url": space_url,
                        "space_response": space_response.json()
                    }
                }
            space_id = spaces[0]["id"]
            
            url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages"
            
            data = {
                "spaceId": space_id,
                "status": "current",
                "title": title,
                "body": {
                    "representation": "storage",
                    "value": content
                }
            }
            
            if parent_id:
                data["parentId"] = parent_id
            
            response = await self.make_request("POST", url, json=data)
            return response.json()
            
        except Exception as e:
            # Return debug info with the error
            return {
                "error": str(e),
                "debug_info": {
                    "site_url": self.config.site_url,
                    "has_access_token": bool(self.config.access_token),
                    "accessible_resources": resources_data if 'resources_data' in locals() else "Failed to retrieve",
                    "cloud_id": cloud_id if 'cloud_id' in locals() else "Failed to retrieve"
                }
            }
    
    async def confluence_update_page(self, page_id: str, title: str, content: str, version: int) -> Dict[str, Any]:
        """Update an existing Confluence page"""
        cloud_id = await self.get_cloud_id()
        url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}"
        
        data = {
            "id": page_id,
            "status": "current", 
            "title": title,
            "body": {
                "representation": "storage",
                "value": content
            },
            "version": {
                "number": version + 1
            }
        }
        
        response = await self.make_request("PUT", url, json=data)
        return response.json()


# Initialize MCP server
mcp = FastMCP("Atlassian Cloud")

# Global client instance
atlassian_client: Optional[AtlassianClient] = None


@mcp.tool()
async def authenticate_atlassian() -> str:
    """Start seamless Atlassian OAuth authentication flow."""
    if not atlassian_client:
        raise ValueError("Atlassian client not initialized")
    
    try:
        await atlassian_client.seamless_oauth_flow()
        return "✅ Authentication successful! You can now use Atlassian tools."
    except Exception as e:
        return f"❌ Authentication failed: {str(e)}"


@mcp.tool()
async def jira_search(jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """Search Jira issues using JQL (Jira Query Language).
    
    Examples:
    - "assignee = currentUser() AND status != Done" - My open issues
    - "project = PROJ AND created >= -7d" - Recent issues in project
    - "text ~ 'bug' ORDER BY created DESC" - Issues containing 'bug'
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_search(jql, max_results)


@mcp.tool()
async def jira_get_issue(issue_key: str) -> Dict[str, Any]:
    """Get detailed information about a specific Jira issue."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_get_issue(issue_key)


@mcp.tool()
async def jira_create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
    """Create a new Jira issue.
    
    Args:
        project_key: The project key (e.g., 'PROJ', 'DEV')
        summary: Brief title of the issue
        description: Detailed description of the issue
        issue_type: Type of issue (Task, Story, Bug, etc.)
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_create_issue(project_key, summary, description, issue_type)


@mcp.tool()
async def jira_update_issue(issue_key: str, summary: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing Jira issue."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_update_issue(issue_key, summary, description)


@mcp.tool()
async def jira_add_comment(issue_key: str, comment: str) -> Dict[str, Any]:
    """Add a comment to a Jira issue."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.jira_add_comment(issue_key, comment)


@mcp.tool()
async def confluence_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search Confluence pages and content.
    
    Args:
        query: Search term to find in page titles and content
        limit: Maximum number of results to return
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_search(query, limit)


@mcp.tool()
async def confluence_get_page(page_id: str) -> Dict[str, Any]:
    """Get detailed content of a specific Confluence page."""
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_get_page(page_id)


@mcp.tool()
async def confluence_create_page(space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new Confluence page.
    
    Args:
        space_key: The space key where to create the page (e.g., 'PROJ', 'DOC')
        title: Title of the new page
        content: HTML content of the page (use Confluence storage format)
        parent_id: Optional parent page ID to create as a child page
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_create_page(space_key, title, content, parent_id)


@mcp.tool()
async def confluence_update_page(page_id: str, title: str, content: str, version: int) -> Dict[str, Any]:
    """Update an existing Confluence page.
    
    Args:
        page_id: ID of the page to update
        title: New title for the page
        content: New HTML content (use Confluence storage format)
        version: Current version number of the page (get from confluence_get_page)
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_update_page(page_id, title, content, version)


async def initialize_client():
    """Initialize the Atlassian client."""
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
        try:
            # Test credentials
            await atlassian_client.get_headers()
            print("✅ Credentials are valid")
        except Exception:
            print("⚠️ Stored credentials are invalid. Use authenticate_atlassian tool to re-authenticate.")
    else:
        print("🔐 No existing credentials found. Use authenticate_atlassian tool to authenticate.")


def main():
    """Main entry point."""
    try:
        # Initialize client
        asyncio.run(initialize_client())
        
        # Run MCP server
        mcp.run()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1


if __name__ == "__main__":
    main()
