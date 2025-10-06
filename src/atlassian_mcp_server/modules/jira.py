"""Jira module for core Jira functionality."""

from typing import Dict, Any, List
from mcp.server import Server
import mcp.types as types
from .base import BaseModule


class JiraModule(BaseModule):
    """Module for core Jira functionality."""
    
    @property
    def name(self) -> str:
        return "jira"
    
    @property
    def required_scopes(self) -> List[str]:
        return ["read:jira-work", "read:jira-user", "write:jira-work"]
    
    def register_tools(self, server: Server) -> None:
        """Register Jira tools."""
        # TODO: Extract Jira tools from server.py
        pass
    
    def register_resources(self, server: Server) -> None:
        """Register Jira resources."""
        # TODO: Extract Jira resources from server.py
        pass
