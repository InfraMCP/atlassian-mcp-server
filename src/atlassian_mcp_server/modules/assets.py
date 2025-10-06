"""Assets module for Jira Service Management Assets (formerly Insight)."""

from typing import Dict, Any, List
from mcp.server import Server
import mcp.types as types
from .base import BaseModule


class AssetsModule(BaseModule):
    """Module for Jira Service Management Assets functionality."""
    
    @property
    def name(self) -> str:
        return "assets"
    
    @property
    def required_scopes(self) -> List[str]:
        return ["read:servicedesk-request"]
    
    def register_tools(self, server: Server) -> None:
        """Register Assets tools."""
        
        @server.call_tool()
        async def assets_list_workspaces(
            start: int = 0, 
            limit: int = 50
        ) -> List[Dict[str, Any]]:
            """List Assets workspaces available in Jira Service Management.
            
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
    
    def register_resources(self, server: Server) -> None:
        """Register Assets resources."""
        
        @server.list_resources()
        async def list_assets_resources() -> List[types.Resource]:
            """List available Assets resources."""
            return [
                types.Resource(
                    uri="assets://workspaces",
                    name="Assets Workspaces",
                    description="List of Assets workspaces in Jira Service Management",
                    mimeType="application/json"
                )
            ]
        
        @server.read_resource()
        async def read_assets_resource(uri: types.AnyUrl) -> str:
            """Read Assets resource content."""
            if str(uri) == "assets://workspaces":
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
