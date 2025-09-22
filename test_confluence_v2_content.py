#!/usr/bin/env python3
"""Test Confluence v2 API content operations"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_confluence_v2():
    """Test Confluence v2 API operations."""
    token_file = Path.home() / ".confluence_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        # Get cloud ID
        response = await client.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=headers)
        resources = response.json()
        
        confluence_resource = None
        for resource in resources:
            if any('confluence' in scope.lower() for scope in resource.get('scopes', [])):
                confluence_resource = resource
                break
        
        cloud_id = confluence_resource['id']
        print(f"🏠 Site: {confluence_resource['name']} (ID: {cloud_id})")
        
        # Test different API approaches
        base_urls = [
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2",
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/v2", 
            f"https://badideafactory.atlassian.net/wiki/api/v2"
        ]
        
        for i, base_url in enumerate(base_urls, 1):
            print(f"\n🧪 Test {i}: Trying {base_url}")
            
            # Test spaces
            response = await client.get(f"{base_url}/spaces", headers=headers, params={"limit": 3})
            print(f"   Spaces: {response.status_code}")
            if response.status_code == 200:
                spaces = response.json()
                results = spaces.get('results', [])
                print(f"   ✅ Found {len(results)} spaces")
                for space in results[:2]:
                    print(f"      🏠 {space.get('name')} (Key: {space.get('key')})")
                
                # Test pages if spaces work
                response = await client.get(f"{base_url}/pages", headers=headers, params={"limit": 3})
                print(f"   Pages: {response.status_code}")
                if response.status_code == 200:
                    pages = response.json()
                    page_results = pages.get('results', [])
                    print(f"   ✅ Found {len(page_results)} pages")
                    for page in page_results[:2]:
                        print(f"      📄 {page.get('title')} (ID: {page.get('id')})")
                    
                    # Test getting specific page content
                    if page_results:
                        page_id = page_results[0]['id']
                        response = await client.get(f"{base_url}/pages/{page_id}", headers=headers, params={"body-format": "storage"})
                        print(f"   Page content: {response.status_code}")
                        if response.status_code == 200:
                            page_data = response.json()
                            print(f"   ✅ Read page: {page_data.get('title')}")
                            body = page_data.get('body', {})
                            if body:
                                content = body.get('storage', {}).get('value', '') or body.get('value', '')
                                print(f"      Content length: {len(content)} chars")
                        else:
                            print(f"   ❌ Page content error: {response.text[:100]}")
                else:
                    print(f"   ❌ Pages error: {response.text[:100]}")
                    
                break  # Found working API
            else:
                print(f"   ❌ Spaces error: {response.text[:100]}")
        
        # Test creating content if we found a working API
        print(f"\n📝 Testing content creation...")
        
        # Try direct site URL approach for creation
        site_base = "https://badideafactory.atlassian.net/wiki/rest/api"
        
        # Get spaces first
        response = await client.get(f"{site_base}/space", headers=headers, params={"limit": 5})
        print(f"Direct site spaces: {response.status_code}")
        
        if response.status_code == 200:
            spaces_data = response.json()
            spaces = spaces_data.get('results', [])
            print(f"✅ Found {len(spaces)} spaces via direct site URL")
            
            for space in spaces[:3]:
                print(f"  🏠 {space.get('name')} (Key: {space.get('key')})")
            
            # Try creating a page
            if spaces:
                space_key = spaces[0]['key']
                print(f"\n✏️  Creating test page in space '{space_key}'...")
                
                create_data = {
                    "type": "page",
                    "title": f"MCP API Test - {int(asyncio.get_event_loop().time())}",
                    "space": {"key": space_key},
                    "body": {
                        "storage": {
                            "value": "<h1>API Test Page</h1><p>Testing Confluence API access from MCP server.</p>",
                            "representation": "storage"
                        }
                    }
                }
                
                response = await client.post(f"{site_base}/content", headers=headers, json=create_data)
                print(f"Create page: {response.status_code}")
                
                if response.status_code == 200:
                    new_page = response.json()
                    print(f"✅ Created: {new_page['title']} (ID: {new_page['id']})")
                else:
                    print(f"❌ Create failed: {response.text[:200]}")
        else:
            print(f"❌ Direct site spaces failed: {response.text[:100]}")

if __name__ == "__main__":
    asyncio.run(test_confluence_v2())
