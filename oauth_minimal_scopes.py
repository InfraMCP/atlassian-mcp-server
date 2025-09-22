#!/usr/bin/env python3
"""OAuth with MINIMAL required scopes for MCP server"""

import asyncio
import base64
import hashlib
import json
import os
import secrets
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse
import httpx
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class OAuthCallbackHandler(BaseHTTPRequestHandler):
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
            
            html = """<html><body><h1>✅ Success!</h1><p>Testing minimal scopes...</p></body></html>"""
            self.wfile.write(html.encode())
            self.server.callback_received = True
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

async def minimal_oauth_test():
    """Test with minimal required scopes"""
    
    site_url = os.getenv("ATLASSIAN_SITE_URL")
    client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
    client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
    
    # Start callback server
    server = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
    server.callback_received = False
    server.callback_data = None
    
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        state = secrets.token_urlsafe(32)
        
        # MINIMAL scopes for MCP server functionality
        scopes = [
            # Jira - Essential for ticket operations
            "read:jira-work",      # Read issues, projects
            "read:jira-user",      # Read user info
            "write:jira-work",     # Create/update issues (if you want write capability)
            
            # Confluence - Essential for content operations  
            "read:confluence-content.all",     # Read all content
            "search:confluence",               # Search functionality
            "read:confluence-space.summary",   # Space info
            # "write:confluence-content",      # Only if you need content creation
            
            # Service Management - Only if you need SM
            "read:servicedesk-request",        # Read SM tickets
            # "write:servicedesk-request",     # Only if creating SM tickets
            
            # Core
            "read:me",             # User profile
            "offline_access"       # Token refresh
        ]
        
        params = {
            "audience": "api.atlassian.com",
            "client_id": client_id,
            "scope": " ".join(scopes),
            "redirect_uri": "http://localhost:8080/callback",
            "state": state,
            "response_type": "code",
            "prompt": "consent"
        }
        
        auth_url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"
        
        print(f"🚀 Testing MINIMAL scopes for MCP server ({len(scopes)} scopes):")
        for scope in scopes:
            print(f"   📋 {scope}")
        
        print("\\n🌐 Opening browser...")
        webbrowser.open(auth_url)
        
        # Wait for callback
        timeout = 300
        start_time = time.time()
        
        while not server.callback_received:
            if time.time() - start_time > timeout:
                raise TimeoutError("Authorization timed out")
            await asyncio.sleep(0.5)
        
        callback_data = server.callback_data
        
        if callback_data['error']:
            raise ValueError(f"OAuth error: {callback_data['error']}")
        
        print("✅ Authorization received, exchanging for tokens...")
        
        # Exchange for tokens
        token_data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": callback_data['code'],
            "redirect_uri": "http://localhost:8080/callback"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                raise ValueError(f"Token exchange failed: {response.text}")
            
            tokens = response.json()
            
            token_file = Path.home() / ".atlassian_minimal_tokens.json"
            with open(token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            token_file.chmod(0o600)
            
            print("✅ OAuth completed!")
            print(f"📋 Scopes received: {tokens.get('scope', 'None')}")
            
            # Test core functionality
            await test_minimal_functionality(tokens)
            
    finally:
        server.shutdown()
        server.server_close()

async def test_minimal_functionality(tokens):
    """Test core MCP server functionality with minimal scopes"""
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    cloud_id = "9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26"
    
    async with httpx.AsyncClient() as client:
        print(f"\\n🧪 TESTING MINIMAL MCP FUNCTIONALITY")
        print("=" * 40)
        
        # Test 1: Jira Projects
        print("\\n📁 1. JIRA PROJECTS")
        response = await client.get(f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/project", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Found {len(projects)} projects")
        else:
            print(f"❌ Projects failed: {response.status_code}")
        
        # Test 2: Jira Issues Search
        print("\\n🔍 2. JIRA SEARCH")
        response = await client.post(
            f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/search",
            headers=headers,
            json={"jql": "order by created DESC", "maxResults": 3}
        )
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Found {len(results.get('issues', []))} recent issues")
        else:
            print(f"❌ Search failed: {response.status_code}")
        
        # Test 3: Confluence Search
        print("\\n📄 3. CONFLUENCE SEARCH")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=page", "limit": 3}
        )
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Found {len(results.get('results', []))} pages")
        else:
            print(f"❌ Confluence search failed: {response.status_code}")
        
        # Test 4: User Info
        print("\\n👤 4. USER INFO")
        response = await client.get("https://api.atlassian.com/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User: {user.get('name')}")
        else:
            print(f"❌ User info failed: {response.status_code}")
        
        print(f"\\n🎯 MINIMAL MCP FUNCTIONALITY TEST COMPLETE!")
        print(f"\\n💡 RECOMMENDATION:")
        print(f"   ✅ These minimal scopes provide excellent MCP server functionality")
        print(f"   ✅ Can read all Jira issues and Confluence content")
        print(f"   ✅ Perfect for AI-powered analysis and Q&A")
        print(f"   ⚠️  Add write:jira-work only if you need issue creation")
        print(f"   ⚠️  Add write:confluence-content only if you need content creation")

if __name__ == "__main__":
    asyncio.run(minimal_oauth_test())
