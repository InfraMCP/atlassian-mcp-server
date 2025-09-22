#!/usr/bin/env python3
"""Diagnose with new management tokens"""

import asyncio
import json
from pathlib import Path
import httpx

async def diagnose_with_management_scopes():
    """Use new management tokens to diagnose the issue."""
    token_file = Path.home() / ".correct_scopes_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        print("🔍 Confluence Management Diagnostic")
        print("=" * 40)
        
        # Check what scopes we actually got
        response = await client.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=headers)
        if response.status_code == 200:
            resources = response.json()
            for resource in resources:
                if any('confluence' in scope.lower() for scope in resource.get('scopes', [])):
                    print(f"📋 Management scopes granted:")
                    for scope in resource['scopes']:
                        print(f"   ✅ {scope}")
                    break
        
        # Now test direct API access
        print(f"\n🧪 Testing Direct API Access:")
        
        # Test 1: Direct site spaces
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
                
            # Test content creation if spaces work
            if spaces.get('results'):
                space_key = spaces['results'][0]['key']
                print(f"\n✏️  Testing content creation in '{space_key}'...")
                
                create_data = {
                    "type": "page",
                    "title": f"Management Test - {int(asyncio.get_event_loop().time())}",
                    "space": {"key": space_key},
                    "body": {
                        "storage": {
                            "value": "<h1>Management Scope Test</h1><p>Testing with full management permissions!</p>",
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
                    print(f"✅ SUCCESS! Created: {page['title']}")
                    print(f"   ID: {page['id']}")
                    print(f"   URL: {page.get('_links', {}).get('webui', 'N/A')}")
                else:
                    print(f"❌ Create failed: {response.text[:200]}")
        else:
            print(f"❌ Still blocked: {response.text[:100]}")

if __name__ == "__main__":
    asyncio.run(diagnose_with_management_scopes())
