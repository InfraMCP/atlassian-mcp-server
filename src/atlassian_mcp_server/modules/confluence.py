"""Confluence module for Confluence functionality."""

from typing import List
from mcp.server import Server
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

    def register_resources(self, server: Server) -> None:
        """Register Confluence resources."""
