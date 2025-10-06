"""Service Desk module for Jira Service Management functionality."""

from typing import Any, Dict, List, Optional

from mcp import types
from mcp.server import Server

from ..clients import ServiceDeskClient
from .base import BaseModule


class ServiceDeskModule(BaseModule):
    """Module for Jira Service Management functionality including Assets."""

    def __init__(self, config):
        """Initialize the Service Desk module."""
        super().__init__(config)
        self.client = ServiceDeskClient(config)
        self._assets_list_workspaces = None

    @property
    def name(self) -> str:
        return "service_desk"

    @property
    def required_scopes(self) -> List[str]:
        return [
            "read:servicedesk-request",
            "write:servicedesk-request",
            "manage:servicedesk-customer",
            "read:knowledgebase:jira-service-management",
        ]

    def register_tools(self, server: Server) -> None:
        """Register Service Desk tools including Assets."""

        # Assets functionality (part of Jira Service Management)
        @server.call_tool()
        async def assets_list_workspaces(
            start: int = 0, limit: int = 50
        ) -> List[Dict[str, Any]]:
            """List Assets workspaces available in Jira Service Management.

            Assets (formerly Insight) is part of Jira Service Management and provides
            IT asset management capabilities.

            Args:
                start: Starting index for pagination (default: 0)
                limit: Maximum number of workspaces to return (default: 50, max: 50)

            Returns:
                List of Assets workspace information
            """
            if not self.client:
                raise ValueError("Atlassian client not initialized")

            cloud_id = await self.client.get_cloud_id()
            url = f"{self.client.jira_base}/{cloud_id}/rest/servicedeskapi/assets/workspace"

            params = {"start": start, "limit": min(limit, 50)}  # API max is 50

            response = await self.client.make_request("GET", url, params=params)
            return response.get("values", [])

        @server.call_tool()
        async def servicedesk_get_requests(
            service_desk_id: Optional[str] = None, limit: int = 50, start: int = 0
        ) -> List[Dict[str, Any]]:
            """Get service desk requests with pagination support."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_get_requests(
                service_desk_id, limit, start
            )

        @server.call_tool()
        async def servicedesk_get_request(issue_key: str) -> Dict[str, Any]:
            """Get detailed information about a specific service desk request."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_get_request(issue_key)

        @server.call_tool()
        async def servicedesk_create_request(
            service_desk_id: str, request_type_id: str, summary: str, description: str
        ) -> Dict[str, Any]:
            """Create a new service desk request."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_create_request(
                service_desk_id, request_type_id, summary, description
            )

        @server.call_tool()
        async def servicedesk_check_availability() -> Dict[str, Any]:
            """Check if Jira Service Management is available and configured on this
            Atlassian instance.

            Use this tool first to verify Service Management is set up before using
            other servicedesk_ tools.
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_check_availability()

        # Store reference for use in resources
        self._assets_list_workspaces = assets_list_workspaces

    def register_resources(self, server: Server) -> None:
        """Register Service Desk resources including Assets."""

        @server.list_resources()
        async def list_service_desk_resources() -> List[types.Resource]:
            """List available Service Desk resources."""
            return [
                types.Resource(
                    uri="service-desk://assets/workspaces",  # type: ignore
                    name="Assets Workspaces",
                    description="List of Assets workspaces in Jira Service Management",
                    mimeType="application/json",
                )
            ]

        @server.read_resource()
        async def read_service_desk_resource(uri: types.AnyUrl) -> str:
            """Read Service Desk resource content."""
            if str(uri) == "service-desk://assets/workspaces":
                if not self.client:
                    return "Atlassian client not initialized"

                try:
                    workspaces = await self._assets_list_workspaces()
                    return (
                        f"Assets Workspaces ({len(workspaces)} found):\n"
                        + "\n".join(
                            [
                                f"- {ws.get('workspaceId', 'Unknown ID')}"
                                for ws in workspaces
                            ]
                        )
                    )
                except (ValueError, KeyError, AttributeError) as e:
                    return f"Error fetching Assets workspaces: {str(e)}"

            raise ValueError(f"Unknown resource: {uri}")
