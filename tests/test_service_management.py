#!/usr/bin/env python3
"""Test Service Management functionality for Atlassian MCP Server."""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from atlassian_mcp_server.server import AtlassianClient, AtlassianConfig


async def test_service_management():
    """Test Service Management API calls."""

    # Load configuration
    site_url = os.getenv("ATLASSIAN_SITE_URL")
    client_id = os.getenv("ATLASSIAN_CLIENT_ID")
    client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")

    if not all([site_url, client_id, client_secret]):
        print("❌ Missing required environment variables:")
        print("   ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, ATLASSIAN_CLIENT_SECRET")
        return False

    config = AtlassianConfig(
        site_url=site_url, client_id=client_id, client_secret=client_secret
    )

    client = AtlassianClient(config)

    # Load existing credentials
    if not await client.load_credentials():
        print("❌ No valid credentials found. Run test_oauth.py first.")
        return False

    print("🔧 Testing Service Management functionality...")

    try:
        # Test 1: Get service desk requests
        print("\n1️⃣ Testing servicedesk_get_requests...")
        requests = await client.servicedesk_get_requests(limit=5)
        print(f"✅ Retrieved {len(requests)} service desk requests")

        if requests:
            # Test 2: Get specific request details
            first_request = requests[0]
            issue_key = first_request.get("issueKey")
            if issue_key:
                print(f"\n2️⃣ Testing servicedesk_get_request for {issue_key}...")
                request_details = await client.servicedesk_get_request(issue_key)
                print(f"✅ Retrieved details for request {issue_key}")

                # Test 3: Get request status
                print(f"\n3️⃣ Testing servicedesk_get_request_status for {issue_key}...")
                status = await client.servicedesk_get_request_status(issue_key)
                print(
                    f"✅ Retrieved status: {status.get('status', {}).get('status', 'Unknown')}"
                )

                # Test 4: Add comment (if write permissions available)
                print(f"\n4️⃣ Testing servicedesk_add_comment for {issue_key}...")
                try:
                    comment_result = await client.servicedesk_add_comment(
                        issue_key,
                        "Test comment from Atlassian MCP Server - Service Management integration test",
                        public=False,  # Internal comment for testing
                    )
                    print("✅ Successfully added comment to request")
                except Exception as e:
                    print(f"⚠️  Comment test failed (may need write permissions): {e}")

        print("\n🎉 Service Management tests completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Service Management test failed: {e}")
        return False

    finally:
        await client.client.aclose()


if __name__ == "__main__":
    success = asyncio.run(test_service_management())
    sys.exit(0 if success else 1)
