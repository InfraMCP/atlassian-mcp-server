#!/usr/bin/env python3
"""Test with basic read:confluence-space scope"""

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

async def test_basic_scope():
    """Test if we need basic read:confluence-space scope."""
    
    # Check if we need to add read:confluence-space to the app first
    site_url = os.getenv("ATLASSIAN_SITE_URL")
    client_id = os.getenv("ATLASSIAN_CLIENT_ID") 
    client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")
    
    # Try with current tokens but different API endpoints
    token_file = Path.home() / '.confluence_full_tokens.json'
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Accept': 'application/json'
    }
    
    async with httpx.AsyncClient() as client:
        print('🔍 Testing different API endpoints...')
        
        # Try v2 API with different paths
        cloud_id = '9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26'
        
        endpoints = [
            f'https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/spaces',
            f'https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/v2/spaces',
            f'https://api.atlassian.com/ex/confluence/{cloud_id}/api/v2/spaces',
        ]
        
        for endpoint in endpoints:
            print(f'\\nTrying: {endpoint}')
            response = await client.get(endpoint, headers=headers, params={'limit': 3})
            print(f'Status: {response.status_code}')
            
            if response.status_code == 200:
                print('✅ SUCCESS!')
                spaces = response.json()
                results = spaces.get('results', [])
                print(f'Found {len(results)} spaces')
                for space in results[:2]:
                    print(f'  🏠 {space.get("name")} ({space.get("key")})')
                return True
            elif response.status_code == 401:
                print('❌ Unauthorized - scope issue')
            elif response.status_code == 404:
                print('❌ Not found - wrong endpoint')
            elif response.status_code == 410:
                print('❌ Gone - deprecated endpoint')
            else:
                print(f'❌ Error: {response.text[:100]}')
        
        print('\\n💡 All endpoints failed. The issue might be:')
        print('1. Missing read:confluence-space scope (need to add to app)')
        print('2. Confluence v2 API not available yet')
        print('3. Different authentication method needed')
        
        return False

if __name__ == "__main__":
    asyncio.run(test_basic_scope())
