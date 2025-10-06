"""
Atlassian MCP Server with seamless OAuth 2.0 flow for Jira and Confluence.

This server provides comprehensive integration with Atlassian Cloud services,
enabling AI assistants to interact with Jira issues, Confluence pages, and
perform various administrative tasks through secure OAuth 2.0 authentication.
"""

import asyncio
import functools
import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .clients import AtlassianConfig, AtlassianError, BaseAtlassianClient
from .module_manager import ModuleManager

# Configure logging to both stderr and file
log_file = Path.home() / ".atlassian-mcp-debug.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr), logging.FileHandler(log_file)],
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Atlassian MCP Server")

# Global instances
ATLASSIAN_CLIENT = None
MODULE_MANAGER = None


def handle_atlassian_errors(func):
    """Decorator to convert AtlassianError to ValueError for MCP compatibility."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AtlassianError as e:
            # Convert to ValueError for MCP compatibility
            raise ValueError(str(e)) from e

    return wrapper


# Authentication tool
@mcp.tool()
@handle_atlassian_errors
async def authenticate_atlassian() -> str:
    """Start seamless Atlassian OAuth authentication flow."""
    if not ATLASSIAN_CLIENT:
        raise ValueError("Client not initialized")
    
    # Get required scopes from module manager
    scopes = None
    if MODULE_MANAGER:
        scopes = MODULE_MANAGER.get_required_scopes()

    return await ATLASSIAN_CLIENT.seamless_oauth_flow(scopes)


async def initialize_client():
    """Initialize and return the Atlassian client."""
    site_url = os.getenv("ATLASSIAN_SITE_URL")
    client_id = os.getenv("ATLASSIAN_CLIENT_ID")
    client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")

    if not all([site_url, client_id, client_secret]):
        raise ValueError(
            "Missing required environment variables: "
            "ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, ATLASSIAN_CLIENT_SECRET"
        )

    config = AtlassianConfig(
        site_url=site_url,
        client_id=client_id,
        client_secret=client_secret,
    )

    client = BaseAtlassianClient(config)
    client.load_credentials()
    return client


def main():
    """Main entry point."""
    global ATLASSIAN_CLIENT, MODULE_MANAGER  # pylint: disable=global-statement
    try:
        # Initialize client
        ATLASSIAN_CLIENT = asyncio.run(initialize_client())

        # Initialize and register modules with config
        MODULE_MANAGER = ModuleManager(ATLASSIAN_CLIENT.config)
        MODULE_MANAGER.register_all(mcp)

        print(
            f"✅ Initialized with modules: {list(MODULE_MANAGER.get_enabled_modules().keys())}"
        )

        # Run MCP server
        mcp.run()
        return 0
    except (ValueError, RuntimeError, OSError) as e:
        print(f"❌ Error starting server: {e}")
        return 1


if __name__ == "__main__":
    main()
