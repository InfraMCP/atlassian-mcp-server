"""
Jira client for Atlassian Cloud API operations.
"""

from typing import Any, Dict, List, Optional

from .base_client import BaseAtlassianClient


class JiraClient(BaseAtlassianClient):
    """Jira-specific client for issue management operations."""

    def __init__(self, config):
        super().__init__(config)
        self.jira_base = "https://api.atlassian.com/ex/jira"

    async def jira_search(
        self, jql: str, max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """Search Jira issues using JQL"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/api/3/search"
        data = {
            "jql": jql,
            "maxResults": max_results,
            "fields": [
                "summary",
                "status",
                "assignee",
                "priority",
                "issuetype",
                "description",
            ],
        }

        response = await self.make_request("POST", url, json=data)
        return response.json().get("issues", [])

    async def jira_get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get Jira issue details"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/api/3/issue/{issue_key}"

        response = await self.make_request("GET", url)
        return response.json()

    async def jira_create_issue(
        self, project_key: str, summary: str, description: str, issue_type: str = "Task"
    ) -> Dict[str, Any]:
        """Create a new Jira issue"""
        cloud_id = await self.get_cloud_id()

        # First get valid issue types for the project
        project_url = (
            f"{self.jira_base}/{cloud_id}/" f"rest/api/3/project/{project_key}"
        )
        project_response = await self.make_request("GET", project_url)
        project_data = project_response.json()

        # Find the issue type (use first available if specified type not found)
        issue_types = project_data.get("issueTypes", [])
        issue_type_id = None

        for it in issue_types:
            if it["name"].lower() == issue_type.lower():
                issue_type_id = it["id"]
                break

        if not issue_type_id and issue_types:
            issue_type_id = issue_types[0]["id"]  # Use first available

        if not issue_type_id:
            raise ValueError(f"No valid issue types found for project {project_key}")

        url = f"{self.jira_base}/{cloud_id}/rest/api/3/issue"
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}],
                        }
                    ],
                },
                "issuetype": {"id": issue_type_id},
            }
        }

        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def jira_update_issue(
        self,
        issue_key: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a Jira issue"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/api/3/issue/{issue_key}"

        fields = {}
        if summary:
            fields["summary"] = summary
        if description:
            fields["description"] = {  # type: ignore
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}],
                    }
                ],
            }

        data = {"fields": fields}
        await self.make_request("PUT", url, json=data)
        return {"success": True, "issue_key": issue_key}

    async def jira_add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """Add a comment to a Jira issue"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/api/3/issue/{issue_key}/comment"

        data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}],
                    }
                ],
            }
        }

        response = await self.make_request("POST", url, json=data)
        return response.json()
