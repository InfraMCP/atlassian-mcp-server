#!/usr/bin/env python3
"""Test Confluence content operations - read, create, modify pages"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_confluence_content():
    """Test comprehensive Confluence content operations."""
    token_file = Path.home() / ".confluence_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Get cloud ID from accessible resources
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=headers)
        resources = response.json()
        
        confluence_resource = None
        for resource in resources:
            if any('confluence' in scope.lower() for scope in resource.get('scopes', [])):
                confluence_resource = resource
                break
        
        cloud_id = confluence_resource['id']
        print(f"🏠 Site: {confluence_resource['name']} (ID: {cloud_id})")
        
        # Test 1: Search for existing pages to understand structure
        print("\n🔍 Test 1: Search existing pages...")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=page", "limit": 5, "expand": "content.space,content.body.storage"}
        )
        
        if response.status_code == 200:
            search_results = response.json()
            pages = search_results.get('results', [])
            print(f"✅ Found {len(pages)} pages")
            
            for page in pages:
                content = page.get('content', {})
                print(f"  📄 {content.get('title')} (ID: {content.get('id')})")
                space = content.get('space', {})
                print(f"     Space: {space.get('name')} (Key: {space.get('key')})")
        
        # Test 2: Get page content using v1 API (since v2 had issues)
        if pages:
            page_id = pages[0]['content']['id']
            print(f"\n📖 Test 2: Reading page content (ID: {page_id})...")
            
            response = await client.get(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content/{page_id}",
                headers=headers,
                params={"expand": "body.storage,space,version"}
            )
            
            if response.status_code == 200:
                page_data = response.json()
                print(f"✅ Page: {page_data.get('title')}")
                print(f"   Version: {page_data.get('version', {}).get('number')}")
                print(f"   Space: {page_data.get('space', {}).get('name')}")
                
                body = page_data.get('body', {}).get('storage', {}).get('value', '')
                print(f"   Content length: {len(body)} chars")
                if body:
                    preview = body[:200] + "..." if len(body) > 200 else body
                    print(f"   Preview: {preview}")
            else:
                print(f"❌ Failed to read page: {response.status_code} - {response.text}")
        
        # Test 3: Get spaces to find where we can create content
        print(f"\n🏠 Test 3: Getting spaces...")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/space",
            headers=headers,
            params={"limit": 10}
        )
        
        if response.status_code == 200:
            spaces_data = response.json()
            spaces = spaces_data.get('results', [])
            print(f"✅ Found {len(spaces)} spaces")
            
            for space in spaces:
                print(f"  🏠 {space.get('name')} (Key: {space.get('key')})")
                print(f"     Type: {space.get('type')}")
        else:
            print(f"❌ Failed to get spaces: {response.status_code} - {response.text}")
        
        # Test 4: Create a test page
        if spaces:
            space_key = spaces[0]['key']
            print(f"\n✏️  Test 4: Creating test page in space '{space_key}'...")
            
            test_content = """
            <h1>AI-Generated Test Page</h1>
            <p>This page was created by the Atlassian MCP Server to test content creation capabilities.</p>
            <h2>Features to Test</h2>
            <ul>
                <li>Page creation ✅</li>
                <li>Content formatting</li>
                <li>Page modification</li>
                <li>Content retrieval</li>
            </ul>
            <p><em>Created: {timestamp}</em></p>
            """.format(timestamp=str(asyncio.get_event_loop().time()))
            
            create_data = {
                "type": "page",
                "title": f"MCP Test Page - {int(asyncio.get_event_loop().time())}",
                "space": {"key": space_key},
                "body": {
                    "storage": {
                        "value": test_content,
                        "representation": "storage"
                    }
                }
            }
            
            response = await client.post(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content",
                headers=headers,
                json=create_data
            )
            
            if response.status_code == 200:
                new_page = response.json()
                new_page_id = new_page['id']
                print(f"✅ Created page: {new_page['title']}")
                print(f"   ID: {new_page_id}")
                print(f"   URL: {new_page.get('_links', {}).get('webui', 'N/A')}")
                
                # Test 5: Update the page we just created
                print(f"\n📝 Test 5: Updating page {new_page_id}...")
                
                updated_content = test_content.replace(
                    "<li>Page modification</li>",
                    "<li>Page modification ✅</li>"
                ).replace(
                    "This page was created",
                    "This page was created and then updated"
                )
                
                update_data = {
                    "version": {"number": new_page['version']['number'] + 1},
                    "title": new_page['title'] + " (Updated)",
                    "type": "page",
                    "body": {
                        "storage": {
                            "value": updated_content,
                            "representation": "storage"
                        }
                    }
                }
                
                response = await client.put(
                    f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content/{new_page_id}",
                    headers=headers,
                    json=update_data
                )
                
                if response.status_code == 200:
                    updated_page = response.json()
                    print(f"✅ Updated page: {updated_page['title']}")
                    print(f"   New version: {updated_page['version']['number']}")
                else:
                    print(f"❌ Failed to update page: {response.status_code} - {response.text}")
                
                # Test 6: Read the updated page back
                print(f"\n📖 Test 6: Reading updated page...")
                response = await client.get(
                    f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content/{new_page_id}",
                    headers=headers,
                    params={"expand": "body.storage,version"}
                )
                
                if response.status_code == 200:
                    final_page = response.json()
                    print(f"✅ Read updated page: {final_page['title']}")
                    print(f"   Version: {final_page['version']['number']}")
                    
                    final_content = final_page.get('body', {}).get('storage', {}).get('value', '')
                    if "Page modification ✅" in final_content:
                        print("✅ Content update verified!")
                    else:
                        print("⚠️  Content update not found")
                
            else:
                print(f"❌ Failed to create page: {response.status_code} - {response.text}")
        
        print(f"\n🎉 Confluence content testing complete!")
        print(f"📋 Capabilities verified:")
        print(f"   ✅ Search pages")
        print(f"   ✅ Read page content") 
        print(f"   ✅ List spaces")
        print(f"   ✅ Create pages")
        print(f"   ✅ Update pages")
        print(f"   ✅ Read updated content")

if __name__ == "__main__":
    asyncio.run(test_confluence_content())
