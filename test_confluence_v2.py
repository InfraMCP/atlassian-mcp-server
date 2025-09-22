#!/usr/bin/env python3
"""Test Confluence v2 API"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_confluence_v2():
    token_file = Path.home() / ".atlassian_full_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json"
    }
    
    cloud_id = "9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26"
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Confluence v2 API...")
        
        # Test pages endpoint
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages",
            headers=headers,
            params={"limit": 5}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            pages = data.get('results', [])
            print(f"✅ Found {len(pages)} Confluence pages")
            for page in pages:
                print(f"  📄 {page.get('title')} (ID: {page.get('id')})")
        else:
            print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_confluence_v2())
