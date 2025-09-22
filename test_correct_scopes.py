#!/usr/bin/env python3
"""Test with potentially missing scopes for Confluence"""

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

class CorrectScopesTest:
    def __init__(self):
        self.site_url = os.getenv("ATLASSIAN_SITE_URL")
        self.client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
        self.client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
        
        self.session_file = Path.home() / ".correct_scopes_session.json"
        self.token_file = Path.home() / ".correct_scopes_tokens.json"
        
    def generate_pkce(self):
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def start_oauth(self):
        """Start OAuth with potentially missing scopes."""
        code_verifier, code_challenge = self.generate_pkce()
        state = secrets.token_urlsafe(32)
        
        session_data = {"state": state, "code_verifier": code_verifier, "code_challenge": code_challenge}
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Try with additional scopes that might be missing
        scopes = [
            # Current scopes we have
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
            
            # Potentially missing scopes
            "manage:confluence-configuration",  # For admin operations
            "write:confluence-space",           # For space operations
            "read:confluence-space",            # Basic space read
            "write:confluence-props",           # Write properties
            "manage:confluence-space",          # Manage spaces
            
            # Jira scopes
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
        print("🚀 Starting OAuth with additional scopes...")
        print(f"📋 Total scopes: {len(scopes)}")
        print("🔍 Added scopes:")
        print("   - manage:confluence-configuration")
        print("   - write:confluence-space") 
        print("   - read:confluence-space")
        print("   - write:confluence-props")
        print("   - manage:confluence-space")
        webbrowser.open(auth_url)
        print("\n⚠️  Copy callback URL and run: python3 test_correct_scopes.py complete 'url'")
        
    async def complete_oauth(self, callback_url: str):
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
            
            tokens = response.json()
            print(f"✅ Tokens received")
            print(f"📋 Scopes: {tokens.get('scope', 'None')}")
            
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            self.token_file.chmod(0o600)
            self.session_file.unlink(missing_ok=True)
    
    async def test_with_new_scopes(self):
        """Test Confluence with new scopes."""
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            print("🧪 Testing with additional scopes...")
            
            # Test 1: Direct site access
            response = await client.get(
                "https://badideafactory.atlassian.net/wiki/rest/api/space",
                headers=headers,
                params={"limit": 3}
            )
            print(f"Direct site spaces: {response.status_code}")
            if response.status_code == 200:
                spaces = response.json()
                print(f"✅ SUCCESS! Found {len(spaces.get('results', []))} spaces")
                for space in spaces.get('results', [])[:2]:
                    print(f"  🏠 {space.get('name')} ({space.get('key')})")
                    
                # Test content access
                response = await client.get(
                    "https://badideafactory.atlassian.net/wiki/rest/api/content",
                    headers=headers,
                    params={"limit": 3, "expand": "body.storage"}
                )
                print(f"Direct content: {response.status_code}")
                if response.status_code == 200:
                    content = response.json()
                    print(f"✅ Content access working! {len(content.get('results', []))} items")
                else:
                    print(f"❌ Content failed: {response.text[:100]}")
                    
            else:
                print(f"❌ Still blocked: {response.text[:100]}")
            
            # Test 2: Check accessible resources for new scopes
            response = await client.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=headers)
            if response.status_code == 200:
                resources = response.json()
                for resource in resources:
                    if any('confluence' in scope.lower() for scope in resource.get('scopes', [])):
                        print(f"\n📋 Confluence scopes granted:")
                        for scope in resource['scopes']:
                            print(f"   ✅ {scope}")

async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 test_correct_scopes.py start")
        print("  python3 test_correct_scopes.py complete 'callback_url'")
        print("  python3 test_correct_scopes.py test")
        return
    
    command = sys.argv[1]
    test = CorrectScopesTest()
    
    if command == "start":
        test.start_oauth()
    elif command == "complete":
        await test.complete_oauth(sys.argv[2])
    elif command == "test":
        await test.test_with_new_scopes()

if __name__ == "__main__":
    asyncio.run(main())
