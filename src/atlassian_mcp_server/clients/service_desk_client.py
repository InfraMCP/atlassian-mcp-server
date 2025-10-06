"""
Service Desk client for Atlassian Cloud API operations.
"""

import logging
from typing import Any, Dict, List, Optional

import httpx

from .base_client import BaseAtlassianClient

logger = logging.getLogger(__name__)


class ServiceDeskClient(BaseAtlassianClient):  # pylint: disable=too-many-public-methods
    """Service Desk-specific client for service management operations."""

    def __init__(self, config):
        super().__init__(config)
        self.jira_base = "https://api.atlassian.com/ex/jira"
        self.load_credentials()  # Load saved credentials

    async def servicedesk_list_service_desks(
        self, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List available service desks for creating requests."""
        logger.debug(
            "servicedesk_list_service_desks: Fetching service desks (limit=%s)", limit
        )

        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/servicedesk"
        params = {"limit": limit}

        response = await self.make_request("GET", url, params=params)
        results = response.json().get("values", [])
        logger.debug(
            "servicedesk_list_service_desks: Found %s service desks", len(results)
        )
        return results

    async def servicedesk_get_service_desk(
        self, service_desk_id: str
    ) -> Dict[str, Any]:
        """Get detailed information about a specific service desk."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/servicedesk/{service_desk_id}"

        response = await self.make_request("GET", url)
        return response.json()

    async def servicedesk_list_request_types(
        self, service_desk_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List available request types for creating service desk requests."""
        cloud_id = await self.get_cloud_id()

        if service_desk_id:
            url = (
                f"{self.jira_base}/{cloud_id}/"
                f"rest/servicedeskapi/servicedesk/{service_desk_id}/requesttype"
            )
        else:
            url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/requesttype"

        params = {"limit": limit}
        response = await self.make_request("GET", url, params=params)
        return response.json().get("values", [])

    async def servicedesk_get_request_type(
        self, service_desk_id: str, request_type_id: str
    ) -> Dict[str, Any]:
        """Get detailed information about a specific request type."""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/"
            f"servicedesk/{service_desk_id}/requesttype/{request_type_id}"
        )

        response = await self.make_request("GET", url)
        return response.json()

    async def servicedesk_get_request_type_fields(
        self, service_desk_id: str, request_type_id: str
    ) -> List[Dict[str, Any]]:
        """Get required and optional fields for a specific request type."""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/"
            f"servicedesk/{service_desk_id}/requesttype/{request_type_id}/field"
        )

        response = await self.make_request("GET", url)
        return response.json().get("requestTypeFields", [])

    async def servicedesk_get_request_comments(
        self, issue_key: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get comments for a service desk request."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/comment"
        params = {"limit": limit}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("values", [])

    async def servicedesk_get_request_transitions(
        self, issue_key: str
    ) -> List[Dict[str, Any]]:
        """Get available transitions for a service desk request."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/transition"

        response = await self.make_request("GET", url)
        return response.json().get("values", [])

    async def servicedesk_transition_request(
        self, issue_key: str, transition_id: str, comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transition a service desk request to a new status."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/transition"

        data = {"id": transition_id}
        if comment:
            data["additionalComment"] = {"body": comment}  # type: ignore

        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def servicedesk_get_requests(
        self, service_desk_id: Optional[str] = None, limit: int = 50, start: int = 0
    ) -> List[Dict[str, Any]]:
        """Get service desk requests with enhanced pagination."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request"

        params = {"limit": limit, "start": start}
        if service_desk_id:
            params["serviceDeskId"] = service_desk_id  # type: ignore

        response = await self.make_request("GET", url, params=params)
        return response.json().get("values", [])

    async def servicedesk_get_request(self, issue_key: str) -> Dict[str, Any]:
        """Get specific service desk request details"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}"

        response = await self.make_request("GET", url)
        return response.json()

    async def servicedesk_create_request(
        self, service_desk_id: str, request_type_id: str, summary: str, description: str
    ) -> Dict[str, Any]:
        """Create a new service desk request"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request"

        data = {
            "serviceDeskId": service_desk_id,
            "requestTypeId": request_type_id,
            "requestFieldValues": {"summary": summary, "description": description},
        }

        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def servicedesk_add_comment(
        self, issue_key: str, comment: str, public: bool = True
    ) -> Dict[str, Any]:
        """Add comment to service desk request"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/comment"

        data = {"body": comment, "public": public}

        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def servicedesk_get_request_status(self, issue_key: str) -> Dict[str, Any]:
        """Get service desk request status"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/status"

        response = await self.make_request("GET", url)
        return response.json()

    async def servicedesk_get_approvals(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get approval information for a service desk request"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/approval"

        response = await self.make_request("GET", url)
        return response.json().get("values", [])

    async def servicedesk_approve_request(
        self, issue_key: str, approval_id: str, decision: str
    ) -> Dict[str, Any]:
        """Approve or decline a service desk request approval"""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/"
            f"{issue_key}/approval/{approval_id}"
        )

        data = {"decision": decision}
        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def servicedesk_get_participants(
        self, issue_key: str
    ) -> List[Dict[str, Any]]:
        """Get participants for a service desk request"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/participant"

        response = await self.make_request("GET", url)
        return response.json().get("values", [])

    async def servicedesk_add_participants(
        self, issue_key: str, usernames: List[str]
    ) -> Dict[str, Any]:
        """Add participants to a service desk request"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/participant"

        data = {"usernames": usernames}
        response = await self.make_request("POST", url, json=data)
        return response.json()

    async def servicedesk_manage_notifications(
        self, issue_key: str, subscribe: bool
    ) -> Dict[str, Any]:
        """Subscribe or unsubscribe from service desk request notifications"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/notification"

        if subscribe:
            await self.make_request("PUT", url)
        else:
            await self.make_request("DELETE", url)

        return {"success": True, "subscribed": subscribe}

    async def servicedesk_get_request_sla(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get SLA information for a service desk request."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/sla"

        response = await self.make_request("GET", url)
        return response.json().get("values", [])

    async def servicedesk_get_sla_metric(
        self, issue_key: str, sla_metric_id: str
    ) -> Dict[str, Any]:
        """Get detailed SLA metric information."""
        cloud_id = await self.get_cloud_id()
        url = (
            f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/"
            f"{issue_key}/sla/{sla_metric_id}"
        )

        response = await self.make_request("GET", url)
        return response.json()

    async def servicedesk_get_request_attachments(
        self, issue_key: str
    ) -> List[Dict[str, Any]]:
        """Get attachments for a service desk request."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/request/{issue_key}/attachment"

        response = await self.make_request("GET", url)
        return response.json().get("values", [])

    async def servicedesk_search_knowledge_base(
        self, query: str, service_desk_id: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search knowledge base articles."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/knowledgebase/article"

        params = {"query": query, "limit": limit}
        if service_desk_id:
            params["serviceDeskId"] = service_desk_id

        response = await self.make_request("GET", url, params=params)
        return response.json().get("values", [])

    async def servicedesk_debug_request(self, endpoint: str) -> Dict[str, Any]:
        """Debug Service Management API requests to see actual responses"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/{endpoint}"

        try:
            response = await self.make_request("GET", url)
            return {
                "success": True,
                "status_code": response.status_code,
                "url": url,
                "response_text": response.text[:500],  # First 500 chars
                "headers": dict(response.headers),
            }
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "status_code": getattr(e, "response", {}).get("status_code", "unknown"),
            }

    async def servicedesk_check_availability(self) -> Dict[str, Any]:
        """Check if Jira Service Management is available and configured"""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/servicedesk"

        try:
            response = await self.make_request("GET", url, params={"limit": 1})
            service_desks = response.json().get("values", [])

            return {
                "available": True,
                "service_desk_count": len(service_desks),
                "service_desks": service_desks,
                "message": (
                    f"Jira Service Management is available with "
                    f"{len(service_desks)} service desk(s) configured."
                ),
                "note": (
                    "If other servicedesk_ tools fail with 404 errors, you may need to "
                    "re-authenticate with: authenticate_atlassian()"
                ),
            }
        except (httpx.HTTPError, ValueError, KeyError) as e:
            return {
                "available": False,
                "service_desk_count": 0,
                "service_desks": [],
                "message": f"Jira Service Management not available: {str(e)}",
            }

    async def assets_list_workspaces(
        self, start: int = 0, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List Assets workspaces available in Jira Service Management.
        
        Assets (formerly Insight) is part of Jira Service Management and provides
        IT asset management capabilities.
        """
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/assets/workspace"
        params = {"start": start, "limit": limit}

        response = await self.make_request("GET", url, params=params)
        return response.json().get("values", [])

    async def assets_get_objects(
        self, workspace_id: str, object_type_id: str, start: int = 0, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get objects from an Assets workspace by object type."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/assets/workspace/{workspace_id}/v1/object/navlist/aql"
        
        data = {
            "qlQuery": f"objectType = {object_type_id}",
            "page": start // limit + 1,
            "resultsPerPage": limit
        }

        response = await self.make_request("POST", url, json=data)
        return response.json().get("objectEntries", [])

    async def assets_create_object(
        self, workspace_id: str, object_type_id: str, attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new object in Assets workspace."""
        # Use dedicated Assets REST API with workspace_id (not cloud_id)
        url = (
            f"https://api.atlassian.com/jsm/assets/workspace/"
            f"{workspace_id}/v1/object/create"
        )
        
        data = {
            "objectTypeId": object_type_id,
            "attributes": [
                {"objectTypeAttributeId": attr_id, "objectAttributeValues": [{"value": value}]}
                for attr_id, value in attributes.items()
            ]
        }

        response = await self.make_request("POST", url, json=data)
        return response.json()
    async def assets_get_object_types(
        self, workspace_id: str
    ) -> List[Dict[str, Any]]:
        """Get object types and their attributes from an Assets workspace."""
        cloud_id = await self.get_cloud_id()
        url = f"{self.jira_base}/{cloud_id}/rest/servicedeskapi/assets/workspace/{workspace_id}/v1/objecttype/list"

        response = await self.make_request("GET", url)
        return response.json().get("values", [])
