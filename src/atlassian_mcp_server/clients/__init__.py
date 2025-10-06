"""
Atlassian client classes for different services.
"""

from .base_client import BaseAtlassianClient, AtlassianConfig, AtlassianError
from .jira_client import JiraClient
from .confluence_client import ConfluenceClient
from .service_desk_client import ServiceDeskClient

__all__ = [
    "BaseAtlassianClient",
    "AtlassianConfig", 
    "AtlassianError",
    "JiraClient",
    "ConfluenceClient",
    "ServiceDeskClient",
]
