"""Service Desk module for Jira Service Management functionality."""

from typing import Dict, Any, List
from mcp.server import Server
import mcp.types as types
from .base import BaseModule


class ServiceDeskModule(BaseModule):
    """Module for Jira Service Management functionality."""
    
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
        """Register Service Desk tools."""
        # TODO: Extract Service Desk tools from server.py
        pass
    
    def register_resources(self, server: Server) -> None:
        """Register Service Desk resources."""
        # TODO: Extract Service Desk resources from server.py
        pass
