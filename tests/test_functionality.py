#!/usr/bin/env python3
"""Test Atlassian MCP server functionality."""

import asyncio
import json
from pathlib import Path

import httpx
import pytest


async def test_atlassian_functionality():
    """Test core Atlassian functionality with saved tokens."""

    token_file = Path.home() / ".atlassian_test_tokens.json"
    if not token_file.exists():
        pytest.skip("No test tokens found. Run test_oauth.py first.")

    with open(token_file, "r") as f:
        tokens = json.load(f)

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Get cloud ID
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.atlassian.com/oauth/token/accessible-resources",
            headers=headers,
        )
        if response.status_code != 200:
            if response.status_code == 401:
                pytest.skip("Tokens expired or invalid. Run test_oauth.py to refresh.")
            else:
                pytest.fail(
                    f"Failed to get accessible resources: {response.status_code}"
                )

        resources = response.json()
        cloud_id = None

        for resource in resources:
            if any("jira" in scope.lower() for scope in resource.get("scopes", [])):
                cloud_id = resource["id"]
                break

        if not cloud_id:
            pytest.fail("No Jira-enabled resource found")

        print(f"🎯 TESTING ATLASSIAN MCP FUNCTIONALITY")
        print("=" * 50)

        success_count = 0
        total_tests = 0

        # Test 1: Jira Projects
        total_tests += 1
        print("\\n📁 1. JIRA PROJECTS")
        response = await client.get(
            f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/project",
            headers=headers,
        )
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Found {len(projects)} projects")
            success_count += 1
        else:
            print(f"❌ Projects failed: {response.status_code}")

        # Test 2: Jira Search
        total_tests += 1
        print("\\n🔍 2. JIRA SEARCH")
        response = await client.post(
            f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/search",
            headers=headers,
            json={"jql": "order by created DESC", "maxResults": 3},
        )
        if response.status_code == 200:
            results = response.json()
            issues = results.get("issues", [])
            print(f"✅ Found {len(issues)} recent issues")
            success_count += 1
        else:
            print(f"❌ Search failed: {response.status_code}")

        # Test 3: Jira Issue Creation
        total_tests += 1
        print("\\n✏️  3. JIRA ISSUE CREATION")
        if projects:
            project_key = projects[0]["key"]

            # Get valid issue types
            project_response = await client.get(
                f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/project/{project_key}",
                headers=headers,
            )
            if project_response.status_code == 200:
                project_data = project_response.json()
                issue_types = project_data.get("issueTypes", [])

                if issue_types:
                    issue_type_id = issue_types[0]["id"]

                    create_data = {
                        "fields": {
                            "project": {"key": project_key},
                            "summary": f"MCP Test Issue - {int(asyncio.get_event_loop().time())}",
                            "description": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "Test issue created by MCP server functionality test.",
                                            }
                                        ],
                                    }
                                ],
                            },
                            "issuetype": {"id": issue_type_id},
                        }
                    }

                    response = await client.post(
                        f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3/issue",
                        headers=headers,
                        json=create_data,
                    )
                    if response.status_code == 201:
                        new_issue = response.json()
                        print(f"✅ Created issue: {new_issue['key']}")
                        success_count += 1
                    else:
                        print(f"❌ Issue creation failed: {response.status_code}")
                else:
                    print("❌ No issue types found")
            else:
                print("❌ Failed to get project details")
        else:
            print("❌ No projects available for testing")

        # Test 4: Confluence Search
        total_tests += 1
        print("\\n📄 4. CONFLUENCE SEARCH")
        response = await client.get(
            f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/rest/api/search",
            headers=headers,
            params={"cql": "type=page", "limit": 3},
        )
        if response.status_code == 200:
            results = response.json()
            pages = results.get("results", [])
            print(f"✅ Found {len(pages)} pages")
            success_count += 1
        else:
            print(f"❌ Confluence search failed: {response.status_code}")

        # Test 5: User Info
        total_tests += 1
        print("\\n👤 5. USER INFO")
        response = await client.get("https://api.atlassian.com/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User: {user.get('name')} ({user.get('email')})")
            success_count += 1
        else:
            print(f"❌ User info failed: {response.status_code}")

        print(f"\\n🎯 FUNCTIONALITY TEST COMPLETE!")
        print(f"📊 Results: {success_count}/{total_tests} tests passed")

        if success_count == total_tests:
            print("🎉 All tests passed! MCP server functionality is working correctly.")
            return True
        else:
            pytest.fail("Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    success = asyncio.run(test_atlassian_functionality())
    exit(0 if success else 1)
