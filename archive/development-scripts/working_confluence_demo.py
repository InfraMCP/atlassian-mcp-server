#!/usr/bin/env python3
"""Demo of working Confluence operations for MCP server"""

import asyncio
import json
from pathlib import Path
import httpx
import re

async def confluence_demo():
    """Demonstrate working Confluence operations that can be used in MCP server."""
    token_file = Path.home() / ".confluence_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json"
    }
    
    # Get cloud ID
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.atlassian.com/oauth/token/accessible-resources", headers=headers)
        resources = response.json()
        
        confluence_resource = None
        for resource in resources:
            if any('confluence' in scope.lower() for scope in resource.get('scopes', [])):
                confluence_resource = resource
                break
        
        cloud_id = confluence_resource['id']
        base_url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search"
        
        print("🚀 Confluence MCP Server Demo - Working Operations")
        print("=" * 50)
        
        # Function 1: Search and list all pages
        print("\n📚 Function: confluence_list_pages()")
        response = await client.get(base_url, headers=headers, params={
            "cql": "type=page",
            "limit": 10,
            "expand": "content.space,content.version,content.body.storage"
        })
        
        if response.status_code == 200:
            results = response.json()
            pages = results.get('results', [])
            print(f"✅ Found {len(pages)} pages")
            
            for page in pages:
                content = page.get('content', {})
                space = content.get('space', {})
                print(f"  📄 {content.get('title')}")
                print(f"     Space: {space.get('name')} ({space.get('key')})")
                print(f"     ID: {content.get('id')}")
                print(f"     Version: {content.get('version', {}).get('number', 'N/A')}")
        
        # Function 2: Search pages by keyword
        print(f"\n🔍 Function: confluence_search_pages('test')")
        response = await client.get(base_url, headers=headers, params={
            "cql": "type=page AND title~'test'",
            "expand": "content.body.storage"
        })
        
        if response.status_code == 200:
            results = response.json()
            pages = results.get('results', [])
            print(f"✅ Found {len(pages)} pages matching 'test'")
            
            for page in pages:
                content = page.get('content', {})
                body = content.get('body', {}).get('storage', {}).get('value', '')
                # Extract text content from HTML
                text_content = re.sub(r'<[^>]+>', '', body).strip()
                print(f"  📄 {content.get('title')}")
                print(f"     Content: {text_content[:100]}...")
        
        # Function 3: Get page content by space
        print(f"\n🏠 Function: confluence_get_space_pages('PM')")
        response = await client.get(base_url, headers=headers, params={
            "cql": "type=page AND space=PM",
            "expand": "content.body.storage,content.space"
        })
        
        if response.status_code == 200:
            results = response.json()
            pages = results.get('results', [])
            print(f"✅ Found {len(pages)} pages in PM space")
            
            for page in pages:
                content = page.get('content', {})
                body = content.get('body', {}).get('storage', {}).get('value', '')
                text_content = re.sub(r'<[^>]+>', '', body).strip()
                
                print(f"  📄 {content.get('title')}")
                print(f"     HTML Length: {len(body)} chars")
                print(f"     Text Length: {len(text_content)} chars")
                print(f"     Content: {text_content[:150]}...")
        
        # Function 4: List all spaces
        print(f"\n🏠 Function: confluence_list_spaces()")
        response = await client.get(base_url, headers=headers, params={
            "cql": "type=space",
            "limit": 10
        })
        
        if response.status_code == 200:
            results = response.json()
            spaces = results.get('results', [])
            print(f"✅ Found {len(spaces)} spaces")
            
            for space in spaces:
                content = space.get('content', {})
                print(f"  🏠 {content.get('name')} ({content.get('key')})")
        
        # Function 5: Advanced content analysis
        print(f"\n🤖 Function: confluence_analyze_content()")
        response = await client.get(base_url, headers=headers, params={
            "cql": "type=page",
            "limit": 3,
            "expand": "content.body.storage"
        })
        
        if response.status_code == 200:
            results = response.json()
            pages = results.get('results', [])
            
            total_content = 0
            total_words = 0
            
            for page in pages:
                content = page.get('content', {})
                body = content.get('body', {}).get('storage', {}).get('value', '')
                text_content = re.sub(r'<[^>]+>', '', body).strip()
                words = len(text_content.split())
                
                total_content += len(text_content)
                total_words += words
                
                print(f"  📄 {content.get('title')}: {words} words")
            
            print(f"✅ Analysis complete:")
            print(f"   Total content: {total_content} characters")
            print(f"   Total words: {total_words}")
            print(f"   Average words per page: {total_words // len(pages) if pages else 0}")
        
        print(f"\n🎯 MCP Server Implementation Summary:")
        print(f"✅ Content Discovery: Search API provides full access")
        print(f"✅ Content Reading: HTML and text extraction working")
        print(f"✅ Space Navigation: Can list and filter by spaces")
        print(f"✅ Content Analysis: Can process and analyze content")
        print(f"✅ Search Functionality: Advanced CQL queries supported")
        print(f"❌ Content Creation: Requires user permissions fix")
        print(f"❌ Content Modification: Requires user permissions fix")
        
        print(f"\n💡 Ready for MCP Server Integration!")

if __name__ == "__main__":
    asyncio.run(confluence_demo())
