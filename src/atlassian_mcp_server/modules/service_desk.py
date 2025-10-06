"""Service Desk module for Jira Service Management functionality."""

from typing import Dict, Any, List
from mcp.server import Server
import mcp.types as types
from .base import BaseModule


class ServiceDeskModule(BaseModule):
    """Module for Jira Service Management functionality including Assets."""
    
    @property
    def name(self) -> str:
        return "service_desk"
    
    @property
    def required_scopes(self) -> List[str]:
        return [
            "read:servicedesk-request",
            "write:servicedesk-request", 
            "manage:servicedesk-customer",
            "read:knowledgebase:jira-service-management"
        ]
    
    def register_tools(self, server: Server) -> None:
        """Register Service Desk tools including Assets."""
        
        # Assets functionality (part of Jira Service Management)
        @server.call_tool()
        async def assets_list_workspaces(
            start: int = 0, 
            limit: int = 50
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
            
            params = {
                "start": start,
                "limit": min(limit, 50)  # API max is 50
            }
            
            response = await self.client.make_request("GET", url, params=params)
            return response.get("values", [])
        
        # TODO: Extract other Service Desk tools from server.py
    
    def register_resources(self, server: Server) -> None:
        """Register Service Desk resources including Assets."""
        
        @server.list_resources()
        async def list_service_desk_resources() -> List[types.Resource]:
            """List available Service Desk resources."""
            return [
                types.Resource(
                    uri="service-desk://assets/workspaces",
                    name="Assets Workspaces",
                    description="List of Assets workspaces in Jira Service Management",
                    mimeType="application/json"
                )
            ]
        
        @server.read_resource()
        async def read_service_desk_resource(uri: types.AnyUrl) -> str:
            """Read Service Desk resource content."""
            if str(uri) == "service-desk://assets/workspaces":
                if not self.client:
                    return "Atlassian client not initialized"
                
                try:
                    workspaces = await assets_list_workspaces()
                    return f"Assets Workspaces ({len(workspaces)} found):\n" + \
                           "\n".join([f"- {ws.get('workspaceId', 'Unknown ID')}" 
                                    for ws in workspaces])
                except Exception as e:
                    return f"Error fetching Assets workspaces: {str(e)}"
            
            raise ValueError(f"Unknown resource: {uri}")
        
        # TODO: Extract other Service Desk resources from server.py
