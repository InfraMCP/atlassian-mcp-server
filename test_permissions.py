#!/usr/bin/env python3
"""Quick test to check if Confluence permissions are fixed"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_permissions():
    token_file = Path.home() / ".confluence_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Confluence permissions...")
        
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
        else:
            print(f"❌ Still blocked: {response.text[:100]}")
        
        # Test 2: Try creating content if spaces work
        if response.status_code == 200:
            spaces = response.json().get('results', [])
            if spaces:
                space_key = spaces[0]['key']
                print(f"\n✏️  Testing page creation in '{space_key}'...")
                
                create_data = {
                    "type": "page",
                    "title": f"Permission Test - {int(asyncio.get_event_loop().time())}",
                    "space": {"key": space_key},
                    "body": {
                        "storage": {
                            "value": "<h1>Permission Test</h1><p>Testing if permissions are now working!</p>",
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
                else:
                    print(f"❌ Create failed: {response.text[:150]}")

if __name__ == "__main__":
    asyncio.run(test_permissions())
