#!/usr/bin/env python3
"""Test all Confluence scopes"""

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

class ConfluenceFullTest:
    def __init__(self):
        self.site_url = os.getenv("ATLASSIAN_SITE_URL")
        self.client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
        self.client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
        
        self.session_file = Path.home() / ".confluence_full_session.json"
        self.token_file = Path.home() / ".confluence_full_tokens.json"
        
    def generate_pkce(self):
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def start_oauth(self):
        """Start OAuth with ALL Confluence scopes."""
        code_verifier, code_challenge = self.generate_pkce()
        state = secrets.token_urlsafe(32)
        
        session_data = {"state": state, "code_verifier": code_verifier, "code_challenge": code_challenge}
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # ALL your Confluence scopes
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
        print("🚀 Starting OAuth with ALL Confluence scopes...")
        print(f"📋 Scopes: {len(scopes)} total")
        webbrowser.open(auth_url)
        print("\n⚠️  Copy callback URL and run: python3 test_confluence_full.py complete 'url'")
        
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
            print(f"✅ Tokens received with scopes: {tokens.get('scope')}")
            
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            self.token_file.chmod(0o600)
            self.session_file.unlink(missing_ok=True)
    
    async def test_confluence_apis(self):
        """Test comprehensive Confluence APIs."""
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            # Get resources
            response = await client.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=headers)
            resources = response.json()
            
            confluence_resource = None
            for resource in resources:
                if 'confluence' in ' '.join(resource.get('scopes', [])).lower():
                    confluence_resource = resource
                    break
            
            if not confluence_resource:
                print("❌ No Confluence resource found")
                return
                
            cloud_id = confluence_resource['id']
            print(f"✅ Confluence site: {confluence_resource['name']}")
            print(f"📋 Confluence scopes: {confluence_resource['scopes']}")
            
            # Test 1: Spaces
            print("\n🧪 Test 1: Getting spaces...")
            response = await client.get(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/spaces",
                headers=headers,
                params={"limit": 5}
            )
            print(f"Spaces API: {response.status_code}")
            if response.status_code == 200:
                spaces = response.json()
                results = spaces.get('results', [])
                print(f"✅ Found {len(results)} space(s)")
                for space in results:
                    print(f"  🏠 {space.get('name')} (Key: {space.get('key')})")
            else:
                print(f"❌ Spaces error: {response.text}")
            
            # Test 2: Pages
            print("\n🧪 Test 2: Getting pages...")
            response = await client.get(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages",
                headers=headers,
                params={"limit": 5}
            )
            print(f"Pages API: {response.status_code}")
            if response.status_code == 200:
                pages = response.json()
                results = pages.get('results', [])
                print(f"✅ Found {len(results)} page(s)")
                for page in results:
                    print(f"  📄 {page.get('title')} (ID: {page.get('id')})")
            else:
                print(f"❌ Pages error: {response.text}")
            
            # Test 3: Search
            print("\n🧪 Test 3: Search...")
            response = await client.get(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
                headers=headers,
                params={"cql": "type=page", "limit": 3}
            )
            print(f"Search API: {response.status_code}")
            if response.status_code == 200:
                search = response.json()
                results = search.get('results', [])
                print(f"✅ Search found {len(results)} result(s)")
                for result in results:
                    print(f"  🔍 {result.get('title')} ({result.get('content', {}).get('type', 'unknown')})")
            else:
                print(f"❌ Search error: {response.text}")
            
            # Test 4: Users
            print("\n🧪 Test 4: Current user...")
            response = await client.get("https://api.atlassian.com/me", headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"✅ User: {user.get('name')} ({user.get('email')})")
            else:
                print(f"❌ User error: {response.status_code}")

async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 test_confluence_full.py start")
        print("  python3 test_confluence_full.py complete 'callback_url'")
        print("  python3 test_confluence_full.py test")
        return
    
    command = sys.argv[1]
    test = ConfluenceFullTest()
    
    if command == "start":
        test.start_oauth()
    elif command == "complete":
        await test.complete_oauth(sys.argv[2])
    elif command == "test":
        await test.test_confluence_apis()

if __name__ == "__main__":
    asyncio.run(main())
