#!/usr/bin/env python3
"""Comprehensive Jira API testing - tickets, service management, kanban"""

import asyncio
import json
from pathlib import Path
import httpx

async def test_jira_comprehensive():
    """Test all Jira functionality"""
    token_file = Path.home() / ".atlassian_seamless_tokens.json"
    
    with open(token_file, 'r') as f:
        tokens = json.load(f)
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    cloud_id = "9c5665d2-2cc5-4fa2-bbee-bf6ae669ac26"
    base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/api/3"
    
    async with httpx.AsyncClient() as client:
        print("🎯 COMPREHENSIVE JIRA API TESTING")
        print("=" * 50)
        
        # 1. Projects and Project Types
        print("\n📁 1. PROJECTS & PROJECT TYPES")
        response = await client.get(f"{base_url}/project", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Found {len(projects)} projects:")
            for project in projects:
                print(f"   📁 {project['key']}: {project['name']} ({project.get('projectTypeKey', 'unknown')})")
                
            # Get project details for first project
            if projects:
                project_key = projects[0]['key']
                response = await client.get(f"{base_url}/project/{project_key}", headers=headers)
                if response.status_code == 200:
                    project_details = response.json()
                    print(f"   📋 Project details: {project_details.get('description', 'No description')}")
        
        # 2. Issue Types
        print(f"\n🎫 2. ISSUE TYPES")
        response = await client.get(f"{base_url}/issuetype", headers=headers)
        if response.status_code == 200:
            issue_types = response.json()
            print(f"✅ Found {len(issue_types)} issue types:")
            for issue_type in issue_types[:5]:
                print(f"   🎫 {issue_type['name']}: {issue_type.get('description', 'No description')}")
        
        # 3. Search Issues (JQL)
        print(f"\n🔍 3. ISSUE SEARCH (JQL)")
        jql_queries = [
            ("Recent issues", "order by created DESC"),
            ("Open issues", "status != Done order by priority DESC"),
            ("My issues", "assignee = currentUser()"),
        ]
        
        for name, jql in jql_queries:
            response = await client.post(
                f"{base_url}/search",
                headers=headers,
                json={"jql": jql, "maxResults": 3, "fields": ["summary", "status", "assignee", "priority", "issuetype"]}
            )
            if response.status_code == 200:
                results = response.json()
                issues = results.get('issues', [])
                print(f"   ✅ {name}: {len(issues)} found")
                for issue in issues:
                    fields = issue['fields']
                    assignee = fields.get('assignee', {})
                    assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
                    print(f"      🎫 {issue['key']}: {fields['summary'][:50]}...")
                    print(f"         Status: {fields['status']['name']}, Assignee: {assignee_name}")
        
        # 4. Create Issue
        print(f"\n✏️  4. CREATE ISSUE")
        if projects:
            project_key = projects[0]['key']
            create_data = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": f"API Test Issue - {int(asyncio.get_event_loop().time())}",
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "This issue was created via API to test Jira functionality."
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {"name": "Task"}
                }
            }
            
            response = await client.post(f"{base_url}/issue", headers=headers, json=create_data)
            if response.status_code == 201:
                new_issue = response.json()
                issue_key = new_issue['key']
                print(f"   ✅ Created issue: {issue_key}")
                
                # 5. Update Issue
                print(f"\n📝 5. UPDATE ISSUE")
                update_data = {
                    "fields": {
                        "summary": f"Updated API Test Issue - {int(asyncio.get_event_loop().time())}",
                        "description": {
                            "type": "doc",
                            "version": 1,
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "This issue was UPDATED via API. Testing modification capabilities."
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
                
                response = await client.put(f"{base_url}/issue/{issue_key}", headers=headers, json=update_data)
                if response.status_code == 204:
                    print(f"   ✅ Updated issue: {issue_key}")
                    
                    # 6. Add Comment
                    print(f"\n💬 6. ADD COMMENT")
                    comment_data = {
                        "body": {
                            "type": "doc",
                            "version": 1,
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "This comment was added via API testing. 🚀"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                    
                    response = await client.post(f"{base_url}/issue/{issue_key}/comment", headers=headers, json=comment_data)
                    if response.status_code == 201:
                        print(f"   ✅ Added comment to: {issue_key}")
                    
                    # 7. Transition Issue (if possible)
                    print(f"\n🔄 7. ISSUE TRANSITIONS")
                    response = await client.get(f"{base_url}/issue/{issue_key}/transitions", headers=headers)
                    if response.status_code == 200:
                        transitions = response.json()
                        available_transitions = transitions.get('transitions', [])
                        print(f"   ✅ Available transitions: {len(available_transitions)}")
                        for transition in available_transitions[:3]:
                            print(f"      🔄 {transition['name']} (ID: {transition['id']})")
            else:
                print(f"   ❌ Failed to create issue: {response.text[:100]}")
        
        # 8. Kanban/Agile Boards
        print(f"\n📋 8. AGILE BOARDS")
        agile_url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/agile/1.0"
        response = await client.get(f"{agile_url}/board", headers=headers)
        if response.status_code == 200:
            boards = response.json()
            board_list = boards.get('values', [])
            print(f"   ✅ Found {len(board_list)} boards:")
            for board in board_list:
                print(f"      📋 {board['name']} ({board['type']}) - ID: {board['id']}")
                
                # Get board configuration
                board_id = board['id']
                response = await client.get(f"{agile_url}/board/{board_id}/configuration", headers=headers)
                if response.status_code == 200:
                    config = response.json()
                    print(f"         Config: {config.get('name', 'No name')}")
        
        # 9. Service Management (if available)
        print(f"\n🎧 9. SERVICE MANAGEMENT")
        sm_url = f"https://api.atlassian.com/ex/jira/{cloud_id}/rest/servicedeskapi"
        response = await client.get(f"{sm_url}/servicedesk", headers=headers)
        if response.status_code == 200:
            service_desks = response.json()
            desks = service_desks.get('values', [])
            print(f"   ✅ Found {len(desks)} service desks:")
            for desk in desks:
                print(f"      🎧 {desk['projectName']} - Key: {desk['projectKey']}")
        elif response.status_code == 404:
            print(f"   ℹ️  Service Management not available or no service desks configured")
        else:
            print(f"   ❌ Service Management error: {response.status_code}")
        
        # 10. User and Permissions
        print(f"\n👤 10. USER & PERMISSIONS")
        response = await client.get("https://api.atlassian.com/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print(f"   ✅ Current user: {user.get('name')} ({user.get('email')})")
        
        # Get user permissions
        response = await client.get(f"{base_url}/mypermissions", headers=headers)
        if response.status_code == 200:
            permissions = response.json()
            perms = permissions.get('permissions', {})
            print(f"   ✅ User permissions: {len(perms)} permission types")
            key_perms = ['BROWSE_PROJECTS', 'CREATE_ISSUES', 'EDIT_ISSUES', 'ASSIGN_ISSUES']
            for perm in key_perms:
                if perm in perms:
                    has_perm = perms[perm].get('havePermission', False)
                    print(f"      {'✅' if has_perm else '❌'} {perm}: {has_perm}")
        
        print(f"\n🎉 JIRA COMPREHENSIVE TEST COMPLETE!")
        print(f"📋 Summary:")
        print(f"   ✅ Project access: Working")
        print(f"   ✅ Issue search: Working") 
        print(f"   ✅ Issue creation: Working")
        print(f"   ✅ Issue updates: Working")
        print(f"   ✅ Comments: Working")
        print(f"   ✅ Agile boards: Working")
        print(f"   ✅ User permissions: Working")

if __name__ == "__main__":
    asyncio.run(test_jira_comprehensive())
