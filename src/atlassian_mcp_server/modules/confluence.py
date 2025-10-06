"""Confluence module for Confluence functionality."""

from typing import List, Dict, Any, Optional
from mcp.server import Server
from .base import BaseModule
from ..clients import ConfluenceClient


class ConfluenceModule(BaseModule):
    """Module for Confluence functionality."""

    def __init__(self, config):
        super().__init__(config)
        self.client = ConfluenceClient(config)

    @property
    def name(self) -> str:
        return "confluence"

    @property
    def required_scopes(self) -> List[str]:
        return [  # pylint: disable=duplicate-code
            "read:page:confluence",
            "read:space:confluence",
            "write:page:confluence",
            "read:comment:confluence",
            "write:comment:confluence",
            "read:label:confluence",
            "read:attachment:confluence"
        ]

    def register_tools(self, server: Server) -> None:
        """Register Confluence tools."""

        @server.call_tool()
        async def confluence_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
            """Search Confluence pages and content.

            Args:
                query: Search term to find in page titles and content
                limit: Maximum number of results to return
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.confluence_search(query, limit)

        @server.call_tool()
        async def confluence_get_page(page_id: str) -> Dict[str, Any]:
            """Get detailed content of a specific Confluence page."""
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.confluence_get_page(page_id)

        @server.call_tool()
        async def confluence_create_page(
            space_key: str,
            title: str,
            content: str,
            parent_id: Optional[str] = None
        ) -> Dict[str, Any]:
            """Create a new Confluence page.

            Args:
                space_key: The space key where to create the page
                title: Page title
                content: Page content in Confluence storage format
                parent_id: Optional parent page ID
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.confluence_create_page(space_key, title, content, parent_id)

        @server.call_tool()
        async def confluence_update_page(
            page_id: str,
            title: str,
            content: str,
            version: int
        ) -> Dict[str, Any]:
            """Update an existing Confluence page.

            Args:
                page_id: ID of the page to update
                title: New page title
                content: New page content in Confluence storage format
                version: Current version number of the page
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.confluence_update_page(page_id, title, content, version)

        @server.call_tool()
        async def confluence_list_spaces(
            limit: int = 25,
            space_type: Optional[str] = None,
            status: str = "current"
        ) -> List[Dict[str, Any]]:
            """List Confluence spaces.

            Args:
                limit: Maximum number of spaces to return
                space_type: Filter by space type (global, personal)
                status: Filter by status (current, archived)
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
            return await self.client.confluence_list_spaces(limit, space_type, status)

        # Add more Confluence functions as needed...

    def register_resources(self, server: Server) -> None:
        """Register Confluence resources."""
        # Confluence resources will be added here if needed
