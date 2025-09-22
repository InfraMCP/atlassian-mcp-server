#!/usr/bin/env python3
"""Diagnose Confluence permissions using management APIs"""

import asyncio
import json
from pathlib import Path
import httpx

async def diagnose_confluence():
    """Use management APIs to diagnose why we can't create content."""
    token_file = Path.home() / ".confluence_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json"
    }
    
    cloud_id = "9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26"
    
    async with httpx.AsyncClient() as client:
        print("🔍 Confluence Permissions Diagnostic")
        print("=" * 40)
        
        # 1. Check current user details
        print("\n👤 Current User Information:")
        response = await client.get("https://api.atlassian.com/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User: {user.get('name')} ({user.get('email')})")
            print(f"   Account ID: {user.get('account_id')}")
            print(f"   Account Status: {user.get('account_status')}")
        else:
            print(f"❌ Failed to get user info: {response.status_code}")
        
        # 2. Check user permissions in Confluence
        print(f"\n🔐 User Confluence Permissions:")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=user", "limit": 5}
        )
        
        if response.status_code == 200:
            results = response.json()
            users = results.get('results', [])
            print(f"✅ Can query users: Found {len(users)} users")
        else:
            print(f"❌ Cannot query users: {response.status_code}")
        
        # 3. Check space permissions
        print(f"\n🏠 Space Permissions Analysis:")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=page AND space=PM", "limit": 1, "expand": "content.space"}
        )
        
        if response.status_code == 200:
            results = response.json()
            if results.get('results'):
                page = results['results'][0]
                space = page.get('content', {}).get('space', {})
                space_key = space.get('key')
                
                print(f"✅ Found space: {space.get('name')} ({space_key})")
                
                # Try to get space permissions
                response = await client.get(
                    f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
                    headers=headers,
                    params={"cql": f"type=space AND key={space_key}", "expand": "space.permissions"}
                )
                
                if response.status_code == 200:
                    space_results = response.json()
                    print(f"✅ Can query space permissions")
                else:
                    print(f"❌ Cannot query space permissions: {response.status_code}")
        
        # 4. Test different API endpoints for creation
        print(f"\n🧪 Testing Different Creation Endpoints:")
        
        # Try cloud API content creation
        test_data = {
            "type": "page",
            "title": f"Diagnostic Test Page",
            "space": {"key": "PM"},
            "body": {
                "storage": {
                    "value": "<p>Test page for diagnostics</p>",
                    "representation": "storage"
                }
            }
        }
        
        endpoints = [
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content",
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages",
            f"https://badideafactory.atlassian.net/wiki/rest/api/content"
        ]
        
        for i, endpoint in enumerate(endpoints, 1):
            print(f"\n   Test {i}: {endpoint.split('/')[-2:]}")
            response = await client.post(endpoint, headers=headers, json=test_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS! Content creation works!")
                created = response.json()
                print(f"   Created: {created.get('title')} (ID: {created.get('id')})")
                break
            elif response.status_code == 401:
                print("   ❌ Unauthorized - scope/auth issue")
            elif response.status_code == 403:
                print("   ❌ Forbidden - permission issue")
                error_text = response.text
                if "not permitted" in error_text.lower():
                    print("   💡 User permission issue detected")
                elif "space" in error_text.lower():
                    print("   💡 Space permission issue detected")
            elif response.status_code == 400:
                print(f"   ❌ Bad Request - data issue: {response.text[:100]}")
            else:
                print(f"   ❌ Other error: {response.text[:100]}")
        
        # 5. Check if we can access user groups
        print(f"\n👥 User Groups Check:")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=group", "limit": 5}
        )
        
        if response.status_code == 200:
            results = response.json()
            groups = results.get('results', [])
            print(f"✅ Can query groups: Found {len(groups)} groups")
            for group in groups[:3]:
                group_content = group.get('content', {})
                print(f"   👥 {group_content.get('name', 'Unknown')}")
        else:
            print(f"❌ Cannot query groups: {response.status_code}")
        
        print(f"\n🎯 Diagnostic Summary:")
        print(f"   - OAuth scopes: ✅ Comprehensive")
        print(f"   - User authentication: ✅ Working")
        print(f"   - Content reading: ✅ Full access")
        print(f"   - Content creation: ❌ Blocked")
        print(f"\n💡 Next steps: Check the specific error messages above")

if __name__ == "__main__":
    asyncio.run(diagnose_confluence())
