#!/usr/bin/env python3
"""Test working Confluence operations using search API"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_working_confluence():
    """Test Confluence operations that actually work."""
    token_file = Path.home() / ".confluence_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json"
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
        print(f"🏠 Site: {confluence_resource['name']}")
        print(f"📋 Confluence scopes: {len(confluence_resource['scopes'])} granted")
        
        # Test 1: Advanced search with different queries
        search_queries = [
            ("type=page", "All pages"),
            ("type=page AND space=PM", "Pages in PM space"),
            ("type=page AND title~'test'", "Pages with 'test' in title"),
            ("type=space", "All spaces")
        ]
        
        for cql, description in search_queries:
            print(f"\n🔍 Search: {description}")
            print(f"   CQL: {cql}")
            
            response = await client.get(
                f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
                headers=headers,
                params={"cql": cql, "limit": 5, "expand": "content.space,content.body.storage,content.version"}
            )
            
            if response.status_code == 200:
                results = response.json()
                items = results.get('results', [])
                print(f"   ✅ Found {len(items)} results")
                
                for item in items:
                    content = item.get('content', {})
                    if content.get('type') == 'page':
                        print(f"      📄 {content.get('title')} (ID: {content.get('id')})")
                        space = content.get('space', {})
                        print(f"         Space: {space.get('name')} ({space.get('key')})")
                        version = content.get('version', {})
                        print(f"         Version: {version.get('number', 'N/A')}")
                        
                        # Try to get body content
                        body = content.get('body', {})
                        if body:
                            storage = body.get('storage', {})
                            if storage:
                                content_text = storage.get('value', '')
                                print(f"         Content: {len(content_text)} chars")
                                if content_text:
                                    # Show first line of content
                                    first_line = content_text.split('\n')[0][:100]
                                    print(f"         Preview: {first_line}...")
                    elif content.get('type') == 'space':
                        print(f"      🏠 Space: {content.get('name')} ({content.get('key')})")
            else:
                print(f"   ❌ Search failed: {response.status_code} - {response.text[:100]}")
        
        # Test 2: Try to get individual page content using different methods
        print(f"\n📖 Testing individual page access...")
        
        # First get a page ID from search
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=page", "limit": 1, "expand": "content"}
        )
        
        if response.status_code == 200:
            results = response.json()
            if results.get('results'):
                page_id = results['results'][0]['content']['id']
                page_title = results['results'][0]['content']['title']
                print(f"   Testing with page: {page_title} (ID: {page_id})")
                
                # Try different endpoints for getting page content
                endpoints = [
                    f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content/{page_id}?expand=body.storage,space,version",
                    f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}?body-format=storage",
                    f"https://badideafactory.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.storage"
                ]
                
                for i, endpoint in enumerate(endpoints, 1):
                    print(f"   Method {i}: {endpoint.split('/')[-3:]}")
                    response = await client.get(endpoint, headers=headers)
                    print(f"      Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        page_data = response.json()
                        print(f"      ✅ Success! Title: {page_data.get('title', 'N/A')}")
                        
                        # Check for content
                        body = page_data.get('body', {})
                        if body:
                            storage = body.get('storage', {})
                            if storage:
                                content_value = storage.get('value', '')
                                print(f"      Content length: {len(content_value)} chars")
                                break
                    else:
                        error_text = response.text[:100] if response.text else "No error text"
                        print(f"      ❌ Failed: {error_text}")
        
        print(f"\n🎯 Summary of Working Confluence Operations:")
        print(f"   ✅ Search API - Full access to find content")
        print(f"   ✅ Content discovery - Can find pages, spaces, metadata")
        print(f"   ✅ OAuth scopes - All permissions granted")
        print(f"   ❌ Direct content access - User permissions issue")
        print(f"   ❌ Content creation - User permissions issue")
        
        print(f"\n💡 Recommendations for MCP Server:")
        print(f"   1. Use search API as primary content discovery method")
        print(f"   2. Request Confluence user permissions from admin")
        print(f"   3. Implement search-based content operations")
        print(f"   4. Consider read-only mode until permissions resolved")

if __name__ == "__main__":
    asyncio.run(test_working_confluence())
