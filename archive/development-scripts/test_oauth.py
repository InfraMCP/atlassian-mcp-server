#!/usr/bin/env python3
"""
Simple test script to validate Atlassian OAuth 2.0 flow.
Based on: https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/
"""

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


class AtlassianOAuthTest:
    def __init__(self):
        self.site_url = os.getenv("ATLASSIAN_SITE_URL")
        self.client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
        self.client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
        
        if not all([self.site_url, self.client_id, self.client_secret]):
            raise ValueError("Set ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, ATLASSIAN_CLIENT_SECRET")
        
        self.session_file = Path.home() / ".atlassian_test_session.json"
        self.token_file = Path.home() / ".atlassian_test_tokens.json"
        
    def generate_pkce(self):
        """Generate PKCE code verifier and challenge."""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        return code_verifier, code_challenge
    
    def start_oauth(self):
        """Step 1: Start OAuth flow and open browser."""
        code_verifier, code_challenge = self.generate_pkce()
        state = secrets.token_urlsafe(32)
        
        # Save session data
        session_data = {
            "state": state,
            "code_verifier": code_verifier,
            "code_challenge": code_challenge
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Build authorization URL
        params = {
            "audience": "api.atlassian.com",
            "client_id": self.client_id,
            "scope": "read:jira-work read:jira-user offline_access",  # Basic Jira scopes
            "redirect_uri": "http://localhost:8080/callback",
            "state": state,
            "response_type": "code",
            "prompt": "consent"
        }
        
        auth_url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"
        
        print("🚀 Starting OAuth flow...")
        print(f"📋 Authorization URL: {auth_url}")
        print("\n🌐 Opening browser...")
        webbrowser.open(auth_url)
        
        print("\n⚠️  After authorizing, you'll see 'This site can't be reached' - this is normal!")
        print("📝 Copy the full callback URL from your browser and run:")
        print("    python test_oauth.py complete 'http://localhost:8080/callback?code=...'")
        
    async def complete_oauth(self, callback_url: str):
        """Step 2: Complete OAuth flow with callback URL."""
        if not self.session_file.exists():
            raise ValueError("No OAuth session found. Run 'python test_oauth.py start' first.")
        
        # Load session data
        with open(self.session_file, 'r') as f:
            session_data = json.load(f)
        
        # Parse callback URL
        parsed = urlparse(callback_url)
        query_params = parse_qs(parsed.query)
        
        if 'error' in query_params:
            raise ValueError(f"OAuth error: {query_params['error'][0]}")
        
        code = query_params.get('code', [None])[0]
        state = query_params.get('state', [None])[0]
        
        if not code or not state:
            raise ValueError("Missing code or state in callback URL")
        
        if state != session_data['state']:
            raise ValueError("Invalid state parameter - possible CSRF attack")
        
        print("✅ Callback URL validated")
        
        # Exchange code for tokens
        token_data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": "http://localhost:8080/callback"
        }
        
        async with httpx.AsyncClient() as client:
            print("🔄 Exchanging code for tokens...")
            response = await client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                return
            
            tokens = response.json()
            print("✅ Tokens received!")
            
            # Save tokens
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            self.token_file.chmod(0o600)
            
            # Clean up session
            self.session_file.unlink(missing_ok=True)
            
            print(f"💾 Tokens saved to {self.token_file}")
            print("🧪 Run 'python test_oauth.py test' to test API access")
    
    async def test_api(self):
        """Step 3: Test API access with saved tokens."""
        if not self.token_file.exists():
            raise ValueError("No tokens found. Complete OAuth flow first.")
        
        with open(self.token_file, 'r') as f:
            tokens = json.load(f)
        
        access_token = tokens.get('access_token')
        if not access_token:
            raise ValueError("No access token found")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            # Test 1: Get accessible resources
            print("🧪 Test 1: Getting accessible resources...")
            response = await client.get(
                "https://api.atlassian.com/oauth/token/accessible-resources",
                headers=headers
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to get resources: {response.status_code}")
                print(f"Response: {response.text}")
                return
            
            resources = response.json()
            print(f"✅ Found {len(resources)} accessible resource(s)")
            
            for resource in resources:
                print(f"  📍 {resource['name']}: {resource['url']}")
                print(f"     Cloud ID: {resource['id']}")
                print(f"     Scopes: {', '.join(resource['scopes'])}")
            
            if not resources:
                print("❌ No accessible resources found")
                return
            
            # Use first resource for testing
            cloud_id = resources[0]['id']
            site_name = resources[0]['name']
            
            # Test 2: Get current user
            print(f"\n🧪 Test 2: Getting current user info...")
            response = await client.get(
                "https://api.atlassian.com/me",
                headers=headers
            )
            
            if response.status_code == 200:
                user = response.json()
                print(f"✅ Current user: {user.get('name')} ({user.get('email')})")
            else:
                print(f"⚠️  User info failed: {response.status_code}")
            
            # Test 3: Get Jira projects
            print(f"\n🧪 Test 3: Getting Jira projects from {site_name}...")
            response = await client.get(
                f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/project",
                headers=headers
            )
            
            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Found {len(projects)} project(s)")
                for project in projects[:3]:  # Show first 3
                    print(f"  📁 {project['key']}: {project['name']}")
            else:
                print(f"⚠️  Projects failed: {response.status_code} - {response.text}")
            
            # Test 4: Search issues
            print(f"\n🧪 Test 4: Searching recent issues...")
            search_data = {
                "jql": "order by created DESC",
                "maxResults": 5
            }
            
            response = await client.post(
                f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/2/search",
                headers=headers,
                json=search_data
            )
            
            if response.status_code == 200:
                results = response.json()
                issues = results.get('issues', [])
                print(f"✅ Found {len(issues)} recent issue(s)")
                for issue in issues:
                    print(f"  🎫 {issue['key']}: {issue['fields']['summary']}")
            else:
                print(f"⚠️  Issue search failed: {response.status_code} - {response.text}")
            
            print("\n🎉 API testing complete!")


async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_oauth.py start                    # Start OAuth flow")
        print("  python test_oauth.py complete 'callback_url'  # Complete with callback URL")
        print("  python test_oauth.py test                     # Test API access")
        return
    
    command = sys.argv[1]
    oauth_test = AtlassianOAuthTest()
    
    try:
        if command == "start":
            oauth_test.start_oauth()
        elif command == "complete":
            if len(sys.argv) < 3:
                print("❌ Missing callback URL")
                print("Usage: python test_oauth.py complete 'http://localhost:8080/callback?code=...'")
                return
            callback_url = sys.argv[2]
            await oauth_test.complete_oauth(callback_url)
        elif command == "test":
            await oauth_test.test_api()
        else:
            print(f"❌ Unknown command: {command}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
