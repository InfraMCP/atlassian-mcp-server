#!/usr/bin/env python3
"""Seamless OAuth server with automatic callback handling"""

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
    """Handle OAuth callback automatically"""
    
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
                <p>You can close this window. The application will continue automatically.</p>
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

class SeamlessAtlassianOAuth:
    def __init__(self):
        self.site_url = os.getenv("ATLASSIAN_SITE_URL")
        self.client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
        self.client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
        
        if not all([self.site_url, self.client_id, self.client_secret]):
            raise ValueError("Set ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, ATLASSIAN_CLIENT_SECRET")
        
        self.token_file = Path.home() / ".atlassian_seamless_tokens.json"
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
        print("🌐 Callback server started on http://localhost:8080")
    
    def stop_callback_server(self):
        """Stop the callback server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            if self.server_thread:
                self.server_thread.join(timeout=1)
        print("🛑 Callback server stopped")
    
    async def seamless_oauth_flow(self):
        """Complete OAuth flow with automatic callback handling"""
        print("🚀 Starting seamless OAuth flow...")
        
        # Start callback server
        self.start_callback_server()
        
        try:
            # Generate PKCE
            code_verifier, code_challenge = self.generate_pkce()
            state = secrets.token_urlsafe(32)
            
            # Build authorization URL with all scopes
            scopes = [
                "write:confluence-content",
                "read:confluence-space.summary", 
                "write:confluence-file",
                "read:confluence-props",
                "read:confluence-content.all",
                "read:confluence-content.summary",
                "search:confluence",
                "read:confluence-content.permission",
                "read:confluence-user",
                "read:confluence-groups",
                "readonly:content.attachment:confluence",
                "manage:confluence-configuration",
                "write:confluence-space",
                "write:confluence-props",
                "read:jira-work",
                "read:jira-user",
                "read:me",
                "offline_access"
            ]
            
            params = {
                "audience": "api.atlassian.com",
                "client_id": self.client_id,
                "scope": " ".join(scopes),
                "redirect_uri": "http://localhost:8080/callback",
                "state": state,
                "response_type": "code",
                "prompt": "consent"
            }
            
            auth_url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"
            
            print(f"🌐 Opening browser for authorization...")
            webbrowser.open(auth_url)
            
            # Wait for callback
            print("⏳ Waiting for authorization...")
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
                "client_id": self.client_id,
                "client_secret": self.client_secret,
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
                
                # Save tokens
                with open(self.token_file, 'w') as f:
                    json.dump(tokens, f, indent=2)
                self.token_file.chmod(0o600)
                
                print("✅ OAuth flow completed successfully!")
                print(f"💾 Tokens saved to {self.token_file}")
                print(f"📋 Scopes: {tokens.get('scope', 'None')}")
                
                return tokens
                
        finally:
            self.stop_callback_server()
    
    async def test_api_access(self):
        """Test API access with new tokens"""
        if not self.token_file.exists():
            print("❌ No tokens found. Run OAuth flow first.")
            return
        
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            print("\n🧪 Testing API access with fresh tokens...")
            
            # Test spaces
            response = await client.get(
                "https://badideafactory.atlassian.net/wiki/rest/api/space",
                headers=headers,
                params={"limit": 3}
            )
            print(f"Spaces: {response.status_code}")
            
            if response.status_code == 200:
                spaces = response.json()
                print(f"✅ SUCCESS! Found {len(spaces.get('results', []))} spaces")
                
                # Test content creation
                if spaces.get('results'):
                    space_key = spaces['results'][0]['key']
                    create_data = {
                        "type": "page",
                        "title": f"Seamless OAuth Test - {int(time.time())}",
                        "space": {"key": space_key},
                        "body": {
                            "storage": {
                                "value": "<h1>🎉 Seamless OAuth Success!</h1><p>Content creation working with automatic callback!</p>",
                                "representation": "storage"
                            }
                        }
                    }
                    
                    response = await client.post(
                        "https://badideafactory.atlassian.net/wiki/rest/api/content",
                        headers=headers,
                        json=create_data
                    )
                    print(f"Create page: {response.status_code}")
                    
                    if response.status_code == 200:
                        page = response.json()
                        print(f"✅ CONTENT CREATION SUCCESS! Created: {page['title']}")
                    else:
                        print(f"❌ Content creation failed: {response.text[:100]}")
            else:
                print(f"❌ Spaces failed: {response.text[:100]}")

async def main():
    oauth = SeamlessAtlassianOAuth()
    
    try:
        # Run seamless OAuth flow
        await oauth.seamless_oauth_flow()
        
        # Test API access
        await oauth.test_api_access()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
