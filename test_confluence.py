#!/usr/bin/env python3
"""Quick Confluence API test"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_confluence():
    token_file = Path.home() / ".atlassian_test_tokens.json"
    
    if not token_file.exists():
        print("❌ No tokens found. Run OAuth flow first.")
        return
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    access_token = tokens.get('access_token')
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    cloud_id = "9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26"  # From previous test
    
    async with httpx.AsyncClient() as client:
        # Test Confluence pages
        print("🧪 Testing Confluence API...")
        
        # Try v2 API
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages",
            headers=headers,
            params={"limit": 5}
        )
        
        print(f"Confluence v2 API: {response.status_code}")
        if response.status_code == 200:
            pages = response.json()
            print(f"✅ Found {len(pages.get('results', []))} pages")
            for page in pages.get('results', [])[:3]:
                print(f"  📄 {page.get('title', 'No title')}")
        else:
            print(f"❌ Error: {response.text}")
        
        # Try v1 API as fallback
        print("\n🧪 Testing Confluence v1 API...")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/content",
            headers=headers,
            params={"limit": 5}
        )
        
        print(f"Confluence v1 API: {response.status_code}")
        if response.status_code == 200:
            content = response.json()
            results = content.get('results', [])
            print(f"✅ Found {len(results)} content items")
            for item in results[:3]:
                print(f"  📄 {item.get('title', 'No title')} ({item.get('type', 'unknown')})")
        else:
            print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_confluence())
