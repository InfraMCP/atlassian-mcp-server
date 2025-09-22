#!/usr/bin/env python3
"""OAuth with ALL Jira scopes from your Developer Console"""

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
            
            html = """
            <html><body>
            <h1>✅ Authorization Successful!</h1>
            <p>You can close this window. Testing Jira write operations...</p>
            </body></html>
            """
            self.wfile.write(html.encode())
            self.server.callback_received = True
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

async def full_jira_oauth_test():
    """Complete OAuth with ALL Jira scopes and test"""
    
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
    print("🌐 Callback server started")
    
    try:
        # Generate PKCE
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        state = secrets.token_urlsafe(32)
        
        # ALL scopes from your Developer Console
        scopes = [
            # Jira Platform REST API (from your screenshot)
            "read:jira-work",
            "read:jira-user", 
            "write:jira-work",
            "manage:jira-project",
            "manage:jira-configuration",
            "manage:jira-webhook",
            "manage:jira-data-provider",
            
            # Jira Service Management API (from your screenshot)
            "read:servicedesk-request",
            "write:servicedesk-request",
            "manage:servicedesk-customer",
            "read:servicemanagement-insight-objects",
            
            # Confluence (existing)
            "read:confluence-content.all",
            "search:confluence",
            "write:confluence-content",
            
            # User and offline
            "read:me",
            "offline_access"
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
        
        print(f"🚀 Starting OAuth with ALL Jira scopes ({len(scopes)} total)...")
        print("🌐 Opening browser...")
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
        
        if callback_data['state'] != state:
            raise ValueError("Invalid state parameter")
        
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
            
            # Save tokens
            token_file = Path.home() / ".atlassian_full_jira_tokens.json"
            with open(token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            token_file.chmod(0o600)
            
            print("✅ OAuth completed!")
            print(f"📋 Scopes received: {tokens.get('scope', 'None')}")
            
            # Test Jira write operations immediately
            await test_jira_write_operations(tokens)
            
    finally:
        server.shutdown()
        server.server_close()
        if server_thread:
            server_thread.join(timeout=1)

async def test_jira_write_operations(tokens):
    """Test Jira write operations with new tokens"""
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    cloud_id = "9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26"
    base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3"
    
    async with httpx.AsyncClient() as client:
        print(f"\\n🧪 TESTING JIRA WRITE OPERATIONS")
        print("=" * 40)
        
        # Test 1: Create Issue
        print("\\n✏️  1. CREATE ISSUE")
        create_data = {
            "fields": {
                "project": {"key": "MDP"},
                "summary": f"Full Scope Test Issue - {int(time.time())}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "🎉 This issue was created with FULL Jira write scopes!"
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Story"}
            }
        }
        
        response = await client.post(f"{base_url}/issue", headers=headers, json=create_data)
        print(f"Create issue: {response.status_code}")
        
        if response.status_code == 201:
            new_issue = response.json()
            issue_key = new_issue['key']
            print(f"✅ SUCCESS! Created: {issue_key}")
            
            # Test 2: Update Issue
            print(f"\\n📝 2. UPDATE ISSUE")
            update_data = {
                "fields": {
                    "summary": f"UPDATED: Full Scope Test Issue - {int(time.time())}",
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "🚀 This issue was UPDATED with full write permissions!"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            
            response = await client.put(f"{base_url}/issue/{issue_key}", headers=headers, json=update_data)
            print(f"Update issue: {response.status_code}")
            
            if response.status_code == 204:
                print(f"✅ SUCCESS! Updated: {issue_key}")
                
                # Test 3: Add Comment
                print(f"\\n💬 3. ADD COMMENT")
                comment_data = {
                    "body": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "🎯 Comment added via API with full write scopes!"
                                    }
                                ]
                            }
                        ]
                    }
                }
                
                response = await client.post(f"{base_url}/issue/{issue_key}/comment", headers=headers, json=comment_data)
                print(f"Add comment: {response.status_code}")
                
                if response.status_code == 201:
                    print(f"✅ SUCCESS! Comment added to: {issue_key}")
                    
                    print(f"\\n🎉 ALL JIRA WRITE OPERATIONS SUCCESSFUL!")
                    print(f"   ✅ Issue creation: Working")
                    print(f"   ✅ Issue updates: Working") 
                    print(f"   ✅ Comments: Working")
                    print(f"   🎫 Created issue: {issue_key}")
                else:
                    print(f"❌ Comment failed: {response.text[:100]}")
            else:
                print(f"❌ Update failed: {response.text[:100]}")
        else:
            print(f"❌ Create failed: {response.text[:150]}")

if __name__ == "__main__":
    asyncio.run(full_jira_oauth_test())
