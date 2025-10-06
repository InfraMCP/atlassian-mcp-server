"""Service Desk module for Jira Service Management functionality."""

from typing import Any, Dict, List, Optional

from mcp.server import Server

from ..clients import ServiceDeskClient
from .base import BaseModule


class ServiceDeskModule(BaseModule):
    """Module for Jira Service Management functionality including Assets."""

    def __init__(self, config):
        """Initialize the Service Desk module."""
        super().__init__(config)
        self.client = ServiceDeskClient(config)

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
        """Register Service Desk tools."""

        @server.tool()
        async def servicedesk_check_availability() -> Dict[str, Any]:
            """Check if Jira Service Management is available and configured."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_check_availability()

        @server.tool()
        async def servicedesk_list_service_desks(limit: int = 50) -> List[Dict[str, Any]]:
            """List available service desks for creating requests."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_list_service_desks(limit)

        @server.tool()
        async def servicedesk_list_request_types(
            service_desk_id: Optional[str] = None, limit: int = 50
        ) -> List[Dict[str, Any]]:
            """List available request types for creating service desk requests."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_list_request_types(service_desk_id, limit)

        @server.tool()
        async def servicedesk_get_requests(
            service_desk_id: Optional[str] = None, limit: int = 50, start: int = 0
        ) -> List[Dict[str, Any]]:
            """Get service desk requests with enhanced pagination."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_get_requests(
                service_desk_id, limit, start
            )

        @server.tool()
        async def servicedesk_get_request(issue_key: str) -> Dict[str, Any]:
            """Get detailed information about a specific service desk request."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.servicedesk_get_request(issue_key)

        @server.tool()
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

        @server.tool()
        async def assets_list_workspaces(
            start: int = 0, limit: int = 50
        ) -> List[Dict[str, Any]]:
            """List Assets workspaces available in Jira Service Management.
            
            Assets (formerly Insight) provides IT asset management capabilities
            within Jira Service Management.
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.assets_list_workspaces(start, limit)

        @server.tool()
        async def assets_get_objects(
            workspace_id: str, object_type_id: str, start: int = 0, limit: int = 50
        ) -> List[Dict[str, Any]]:
            """Get objects from an Assets workspace by object type."""
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.assets_get_objects(workspace_id, object_type_id, start, limit)

        @server.tool()
        async def assets_create_object(
            workspace_id: str, object_type_id: str, attributes: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Create a new object in Assets workspace.
            
            Args:
                workspace_id: Assets workspace ID
                object_type_id: Object type ID to create
                attributes: Dict mapping attribute IDs to values
            """
            if not self.client or not self.client.config.access_token:
                raise ValueError(
                    "Not authenticated. Use authenticate_atlassian tool first."
                )
            return await self.client.assets_create_object(workspace_id, object_type_id, attributes)

    def register_resources(self, server: Server) -> None:
        """Register Service Desk resources."""
        # Resources will be added here if needed in the future
        pass
