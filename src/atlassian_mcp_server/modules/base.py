"""Base module class for Atlassian MCP Server modules."""

from abc import ABC, abstractmethod
from typing import List
from mcp.server import Server


class BaseModule(ABC):
    """Base class for all Atlassian MCP modules."""

    def __init__(self, client):
        """Initialize the module with an Atlassian client."""
        self.client = client

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the module name."""

    @property
    @abstractmethod
    def required_scopes(self) -> List[str]:
        """Return the required OAuth scopes for this module."""

    @abstractmethod
    def register_tools(self, server: Server) -> None:
        """Register MCP tools for this module."""

    @abstractmethod
    def register_resources(self, server: Server) -> None:
        """Register MCP resources for this module."""

    def is_available(self) -> bool:
        """Check if this module is available based on client configuration."""
        return self.client and self.client.config.access_token is not None
