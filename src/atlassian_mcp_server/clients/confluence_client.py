"""
Confluence client for Atlassian Cloud API operations.
"""

from typing import Any, Dict, List, Optional

import httpx

from .base_client import BaseAtlassianClient


class ConfluenceClient(BaseAtlassianClient):
    """Confluence-specific client for content management operations."""

    def __init__(self, config):
        super().__init__(config)
        self.confluence_base = "https://api.atlassian.com/ex/confluence"

    async def confluence_search(
        self, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search Confluence content using v2 API"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages"
        params = {"title": query, "limit": limit, "body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_page(self, page_id: str) -> Dict[str, Any]:
        """Get Confluence page content"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages/{page_id}"
        params = {"body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json()

    async def _get_space_id(self, cloud_id: str, space_key: str) -> str:
        """Helper method to get space ID from space key."""
        space_url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/spaces"
        space_response = await self.make_request(
            "GET", space_url, params={"keys": space_key}
        )
        spaces = space_response.json().get("results", [])
        if not spaces:
            raise ValueError(f"Space '{space_key}' not found")
        return spaces[0]["id"]

    async def _build_page_data(
        self, space_id: str, title: str, content: str, parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Helper method to build page creation data."""
        data = {
            "spaceId": space_id,
            "status": "current",
            "title": title,
            "body": {"representation": "storage", "value": content},
            "subtype": "live",
        }
        if parent_id:
            data["parentId"] = parent_id
        return data

    async def confluence_create_page(
        self, space_key: str, title: str, content: str, parent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new Confluence page"""
        try:
            cloud_id = await self.get_cloud_id()
            space_id = await self._get_space_id(cloud_id, space_key)

            url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages"
            data = await self._build_page_data(space_id, title, content, parent_id)

            try:
                await self.get_headers()
                response = await self.make_request("POST", url, json=data)
                return response.json()
            except ValueError as auth_error:
                return {
                    "error": f"Authentication error: {str(auth_error)}",
                    "debug_info": {
                        "api_url": url,
                        "request_data": data,
                        "space_id": space_id,
                        "access_token_present": bool(self.config.access_token),
                        "access_token_length": (
                            len(self.config.access_token)
                            if self.config.access_token
                            else 0
                        ),
                        "refresh_token_present": bool(self.config.refresh_token),
                        "site_url": self.config.site_url,
                    },
                }
            except (httpx.HTTPError, KeyError) as api_error:
                return {
                    "error": f"API call failed: {str(api_error)}",
                    "debug_info": {
                        "api_url": url,
                        "request_data": data,
                        "space_id": space_id,
                    },
                }

        except (httpx.HTTPError, ValueError, KeyError, AttributeError) as e:
            return {
                "error": str(e),
                "debug_info": {
                    "site_url": self.config.site_url,
                    "has_access_token": bool(self.config.access_token),
                },
            }

    async def confluence_update_page(
        self, page_id: str, title: str, content: str, version: int
    ) -> Dict[str, Any]:
        """Update an existing Confluence page"""
        cloud_id = await self.get_cloud_id(required_scopes=["write:page:confluence"])
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages/{page_id}"

        data = {
            "id": page_id,
            "status": "current",
            "title": title,
            "body": {"representation": "storage", "value": content},
            "version": {"number": version + 1},
        }

        response = await self.make_request("PUT", url, json=data)
        return response.json()

    async def confluence_list_spaces(
        self, limit: int = 25, space_type: Optional[str] = None, status: str = "current"
    ) -> List[Dict[str, Any]]:
        """List Confluence spaces with filtering options."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/spaces"

        params = {"limit": limit, "status": status}
        if space_type:
            params["type"] = space_type

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_space(
        self, space_id: str, include_icon: bool = False
    ) -> Dict[str, Any]:
        """Get detailed information about a specific space."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/spaces/{space_id}"

        params = {"include-icon": include_icon}

        response = await self.make_request("GET", url, params=params)
        return response.json()

    async def confluence_get_space_pages(
        self, space_id: str, limit: int = 25, status: str = "current"
    ) -> List[Dict[str, Any]]:
        """Get pages in a specific space."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages"

        params = {
            "space-id": space_id,
            "limit": limit,
            "status": status,
            "body-format": "storage",
        }

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_search_content(
        self, query: str, limit: int = 25, space_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Advanced search across Confluence content."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages"

        params = {"title": query, "limit": limit, "body-format": "storage"}
        if space_id:
            params["space-id"] = space_id

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_page_children(
        self, page_id: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Get child pages of a specific page."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages/{page_id}/children"

        params = {"limit": limit, "body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_page_comments(
        self, page_id: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Get comments for a specific page."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/footer-comments"

        params = {"page-id": page_id, "limit": limit, "body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_add_comment(
        self, page_id: str, comment: str, parent_comment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a comment to a page."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/footer-comments"

        data = {
            "pageId": page_id,
            "body": {"representation": "storage", "value": comment},
        }

        if parent_comment_id:
            data["parentCommentId"] = parent_comment_id

        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def confluence_get_comment(self, comment_id: str) -> Dict[str, Any]:
        """Get a specific comment by ID."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/footer-comments/{comment_id}"

        params = {"body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json()

    async def confluence_get_page_labels(
        self, page_id: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Get labels for a specific page."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages/{page_id}/labels"

        params = {"limit": limit}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_search_by_label(
        self, label_id: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Find pages with a specific label."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/labels/{label_id}/pages"

        params = {"limit": limit, "body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_list_labels(
        self, limit: int = 25, prefix: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List all labels with optional filtering."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/labels"

        params = {"limit": limit}
        if prefix:
            params["prefix"] = prefix  # type: ignore

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_page_attachments(
        self, page_id: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Get attachments for a specific page."""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages/{page_id}/attachments"
        )

        params = {"limit": limit}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_attachment(self, attachment_id: str) -> Dict[str, Any]:
        """Get details of a specific attachment."""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.confluence_base}/{cloud_id}/wiki/api/v2/attachments/{attachment_id}"
        )

        response = await self.make_request("GET", url)
        return response.json()

    async def confluence_get_page_versions(
        self, page_id: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Get version history for a page."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.confluence_base}/{cloud_id}/wiki/api/v2/pages/{page_id}/versions"

        params = {"limit": limit, "body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("results", [])

    async def confluence_get_page_version(
        self, page_id: str, version_number: int
    ) -> Dict[str, Any]:
        """Get a specific version of a page."""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.confluence_base}/{cloud_id}/"
            f"wiki/api/v2/pages/{page_id}/versions/{version_number}"
        )

        params = {"body-format": "storage"}

        response = await self.make_request("GET", url, params=params)
        return response.json()
