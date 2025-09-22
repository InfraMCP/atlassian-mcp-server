#!/usr/bin/env python3
"""OAuth test with both Jira and Confluence scopes"""

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

class FullAtlassianOAuthTest:
    def __init__(self):
        self.site_url = os.getenv("ATLASSIAN_SITE_URL")
        self.client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
        self.client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
        
        if not all([self.site_url, self.client_id, self.client_secret]):
            raise ValueError("Set ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, ATLASSIAN_CLIENT_SECRET")
        
        self.session_file = Path.home() / ".atlassian_full_session.json"
        self.token_file = Path.home() / ".atlassian_full_tokens.json"
        
    def generate_pkce(self):
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def start_oauth(self):
        """Start OAuth with full scopes."""
        code_verifier, code_challenge = self.generate_pkce()
        state = secrets.token_urlsafe(32)
        
        session_data = {
            "state": state,
            "code_verifier": code_verifier,
            "code_challenge": code_challenge
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Full scopes for both Jira and Confluence
        scopes = [
            "read:jira-work",
            "read:jira-user", 
            "read:confluence-content.summary",
            "read:confluence-content.all",
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
        
        print("🚀 Starting OAuth with FULL scopes (Jira + Confluence)...")
        print(f"📋 Scopes: {', '.join(scopes)}")
        print(f"🌐 Opening: {auth_url}")
        webbrowser.open(auth_url)
        
        print("\n⚠️  After authorizing, copy the callback URL and run:")
        print("    python3 test_oauth_full.py complete 'callback_url'")
        
    async def complete_oauth(self, callback_url: str):
        """Complete OAuth flow."""
        if not self.session_file.exists():
            raise ValueError("No session found. Run start first.")
        
        with open(self.session_file, 'r') as f:
            session_data = json.load(f)
        
        parsed = urlparse(callback_url)
        query_params = parse_qs(parsed.query)
        
        code = query_params.get('code', [None])[0]
        state = query_params.get('state', [None])[0]
        
        if state != session_data['state']:
            raise ValueError("Invalid state")
        
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": "http://localhost:8080/callback"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                print(f"❌ Token exchange failed: {response.text}")
                return
            
            tokens = response.json()
            print("✅ Tokens received with scopes:", tokens.get('scope'))
            
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            self.token_file.chmod(0o600)
            
            self.session_file.unlink(missing_ok=True)
            print("🧪 Run 'python3 test_oauth_full.py test' to test APIs")
    
    async def test_apis(self):
        """Test both Jira and Confluence APIs."""
        if not self.token_file.exists():
            raise ValueError("No tokens found")
        
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            # Get resources
            response = await client.get(
                "https://api.atlassian.com/oauth/token/accessible-resources",
                headers=headers
            )
            
            resources = response.json()
            cloud_id = resources[0]['id']
            print(f"✅ Site: {resources[0]['name']}")
            print(f"📋 Scopes: {', '.join(resources[0]['scopes'])}")
            
            # Test user info
            print("\n🧪 Testing user info...")
            response = await client.get("https://api.atlassian.com/me", headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"✅ User: {user.get('name')} ({user.get('email')})")
            else:
                print(f"❌ User info failed: {response.status_code}")
            
            # Test Confluence
            print("\n🧪 Testing Confluence...")
            response = await client.get(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content",
                headers=headers,
                params={"limit": 3}
            )
            
            if response.status_code == 200:
                content = response.json()
                results = content.get('results', [])
                print(f"✅ Found {len(results)} Confluence items")
                for item in results:
                    print(f"  📄 {item.get('title')} ({item.get('type')})")
            else:
                print(f"❌ Confluence failed: {response.status_code} - {response.text}")
            
            # Test Jira
            print("\n🧪 Testing Jira...")
            response = await client.get(
                f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/project",
                headers=headers
            )
            
            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Found {len(projects)} Jira projects")
                for project in projects[:3]:
                    print(f"  📁 {project['key']}: {project['name']}")
            else:
                print(f"❌ Jira failed: {response.status_code}")

async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 test_oauth_full.py start")
        print("  python3 test_oauth_full.py complete 'callback_url'")
        print("  python3 test_oauth_full.py test")
        return
    
    command = sys.argv[1]
    oauth_test = FullAtlassianOAuthTest()
    
    if command == "start":
        oauth_test.start_oauth()
    elif command == "complete":
        callback_url = sys.argv[2]
        await oauth_test.complete_oauth(callback_url)
    elif command == "test":
        await oauth_test.test_apis()

if __name__ == "__main__":
    asyncio.run(main())
