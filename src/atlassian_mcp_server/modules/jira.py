"""Jira module for core Jira functionality."""

from typing import List, Dict, Any, Optional
from mcp.server import Server
from .base import BaseModule
from ..clients import JiraClient


class JiraModule(BaseModule):
    """Module for core Jira functionality."""

    def __init__(self, config):
        super().__init__(config)
        self.client = JiraClient(config)

    @property
    def name(self) -> str:
        return "jira"

    @property
    def required_scopes(self) -> List[str]:
        return ["read:jira-work", "read:jira-user", "write:jira-work"]

    def register_tools(self, server: Server) -> None:
        """Register Jira tools."""

        @server.call_tool()
        async def jira_search(jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
            """Search Jira issues using JQL (Jira Query Language).

            Examples:
            - "assignee = currentUser() AND status != Done" - My open issues
            - "project = PROJ AND created >= -7d" - Recent issues in project
            - "text ~ 'bug' ORDER BY created DESC" - Issues containing 'bug'
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.jira_search(jql, max_results)

        @server.call_tool()
        async def jira_get_issue(issue_key: str) -> Dict[str, Any]:
            """Get detailed information about a specific Jira issue."""
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.jira_get_issue(issue_key)

        @server.call_tool()
        async def jira_create_issue(
            project_key: str, summary: str, description: str, issue_type: str = "Task"
        ) -> Dict[str, Any]:
            """Create a new Jira issue.

            Args:
                project_key: The project key (e.g., 'PROJ', 'DEV')
                summary: Brief title of the issue
                description: Detailed description of the issue
                issue_type: Type of issue (Task, Story, Bug, etc.)
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.jira_create_issue(
                project_key, summary, description, issue_type
            )

        @server.call_tool()
        async def jira_update_issue(
            issue_key: str, summary: Optional[str] = None, description: Optional[str] = None
        ) -> Dict[str, Any]:
            """Update an existing Jira issue."""
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.jira_update_issue(issue_key, summary, description)

        @server.call_tool()
        async def jira_add_comment(issue_key: str, comment: str) -> Dict[str, Any]:
            """Add a comment to a Jira issue."""
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.jira_add_comment(issue_key, comment)

    def register_resources(self, server: Server) -> None:
        """Register Jira resources."""
        # Jira resources will be added here if needed
