"""Confluence module for Confluence functionality."""

from typing import Dict, Any, List
from mcp.server import Server
import mcp.types as types
from .base import BaseModule


class ConfluenceModule(BaseModule):
    """Module for Confluence functionality."""
    
    @property
    def name(self) -> str:
        return "confluence"
    
    @property
    def required_scopes(self) -> List[str]:
        return [
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
        # TODO: Extract Confluence tools from server.py
        pass
    
    def register_resources(self, server: Server) -> None:
        """Register Confluence resources."""
        # TODO: Extract Confluence resources from server.py
        pass
