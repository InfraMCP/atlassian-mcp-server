"""
Atlassian client classes for different services.
"""

from .base_client import AtlassianConfig, AtlassianError, BaseAtlassianClient
from .confluence_client import ConfluenceClient
from .jira_client import JiraClient
from .service_desk_client import ServiceDeskClient

__all__ = [
    "BaseAtlassianClient",
    "AtlassianConfig",
    "AtlassianError",
    "JiraClient",
    "ConfluenceClient",
    "ServiceDeskClient",
]
