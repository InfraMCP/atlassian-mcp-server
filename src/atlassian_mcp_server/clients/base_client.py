"""
Base Atlassian client with OAuth 2.0 authentication and common HTTP functionality.
"""

import asyncio
import base64
import hashlib
import json
import logging
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AtlassianConfig(BaseModel):
    """Configuration for Atlassian Cloud connection."""

    site_url: str
    client_id: str
    client_secret: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class AtlassianError(Exception):
    """Structured error for AI agent consumption."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        message: str,
        error_code: str,
        *,
        context: Optional[Dict[str, Any]] = None,
        troubleshooting: Optional[List[str]] = None,
        suggested_actions: Optional[List[str]] = None,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.troubleshooting = troubleshooting or []
        self.suggested_actions = suggested_actions or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format for JSON serialization."""
        return {
            "success": False,
            "error": str(self),
            "error_code": self.error_code,
            "context": self.context,
            "troubleshooting": self.troubleshooting,
            "suggested_actions": self.suggested_actions,
        }


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback automatically."""

    def do_GET(self):  # pylint: disable=invalid-name
        """Handle GET requests for OAuth callback."""
        if self.path.startswith("/callback"):
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)

            self.server.callback_data = {
                "code": query_params.get("code", [None])[0],
                "state": query_params.get("state", [None])[0],
                "error": query_params.get("error", [None])[0],
            }

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(self._get_success_html())))
            self.end_headers()
            self.wfile.write(self._get_success_html().encode("utf-8"))

    def _get_success_html(self) -> str:
        """Return success HTML page."""
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Authentication Successful</title></head>
        <body>
            <h1>✅ Authentication Successful!</h1>
            <p>You can now close this window and return to your application.</p>
            <script>setTimeout(() => window.close(), 2000);</script>
        </body>
        </html>
        """

    def log_message(self, format, *args):  # pylint: disable=redefined-builtin
        """Suppress HTTP server log messages."""


class BaseAtlassianClient:
    """Base HTTP client for Atlassian Cloud APIs with OAuth 2.0 authentication."""

    def __init__(self, config: AtlassianConfig):
        self.config = config
        self.client = httpx.AsyncClient()
        self.credentials_file = Path.home() / ".atlassian_mcp_credentials.json"
        self.server = None
        self.server_thread = None
        self.code_verifier = None

    def generate_pkce(self):
        """Generate PKCE codes"""
        code_verifier = (
            base64.urlsafe_b64encode(secrets.token_bytes(32))
            .decode("utf-8")
            .rstrip("=")
        )
        code_challenge = (
            base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode("utf-8")).digest()
            )
            .decode("utf-8")
            .rstrip("=")
        )
        return code_verifier, code_challenge

    def start_callback_server(self):
        """Start the callback server"""
        self.server = HTTPServer(("localhost", 8080), OAuthCallbackHandler)
        self.server.callback_received = False
        self.server.callback_data = None

        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop_callback_server(self):
        """Stop the callback server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            if self.server_thread:
                self.server_thread.join(timeout=1)

    async def seamless_oauth_flow(self):
        """Complete OAuth flow with automatic callback handling"""
        self.start_callback_server()

        try:
            code_verifier, code_challenge = self.generate_pkce()
            self.code_verifier = code_verifier
            state = secrets.token_urlsafe(32)

            scopes = [  # pylint: disable=duplicate-code
                "read:jira-work",
                "read:jira-user",
                "write:jira-work",
                "read:page:confluence",
                "read:space:confluence",
                "write:page:confluence",
                "read:comment:confluence",
                "write:comment:confluence",
                "read:label:confluence",
                "read:attachment:confluence",
                "read:servicedesk-request",
                "write:servicedesk-request",
                "manage:servicedesk-customer",
                "read:knowledgebase:jira-service-management",
                "read:assets:jira-service-management",
                "write:assets:jira-service-management",
                "read:me",
                "offline_access",
            ]

            auth_params = {
                "audience": "api.atlassian.com",
                "client_id": self.config.client_id,
                "scope": " ".join(scopes),
                "redirect_uri": "http://localhost:8080/callback",
                "state": state,
                "response_type": "code",
                "prompt": "consent",
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }

            auth_url = f"https://auth.atlassian.com/authorize?{urlencode(auth_params)}"
            logger.info("Opening browser for authentication...")
            webbrowser.open(auth_url)

            # Wait for callback
            timeout = 300
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.server.callback_data:
                    break
                await asyncio.sleep(0.5)

            if not self.server.callback_data:
                raise AtlassianError(
                    "Authentication timeout - no callback received", "AUTH_TIMEOUT"
                )

            callback_data = self.server.callback_data
            if callback_data.get("error"):
                raise AtlassianError(
                    f"OAuth error: {callback_data['error']}", "OAUTH_ERROR"
                )

            # Exchange code for tokens
            token_data = {
                "grant_type": "authorization_code",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "code": callback_data["code"],
                "redirect_uri": "http://localhost:8080/callback",
                "code_verifier": code_verifier,
            }

            response = await self.client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code != 200:
                raise AtlassianError(
                    f"Token exchange failed: {response.text}", "TOKEN_EXCHANGE_FAILED"
                )

            tokens = response.json()
            self.config.access_token = tokens["access_token"]
            self.config.refresh_token = tokens["refresh_token"]
            self.save_credentials()

            return "✅ Authentication successful! You can now use Atlassian tools."

        finally:
            self.stop_callback_server()

    def save_credentials(self):
        """Save credentials to file"""
        credentials = {
            "site_url": self.config.site_url,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "access_token": self.config.access_token,
            "refresh_token": self.config.refresh_token,
        }
        with open(self.credentials_file, "w", encoding="utf-8") as f:
            json.dump(credentials, f, indent=2)

    def load_credentials(self) -> bool:
        """Load saved credentials"""
        if not self.credentials_file.exists():
            return False

        try:
            with open(self.credentials_file, "r", encoding="utf-8") as f:
                credentials = json.load(f)
                self.config.access_token = credentials.get("access_token")
                self.config.refresh_token = credentials.get("refresh_token")
                return bool(self.config.access_token)
        except (json.JSONDecodeError, KeyError):
            return False

    async def refresh_access_token(self) -> bool:
        """Refresh access token using refresh token"""
        if not self.config.refresh_token:
            return False

        token_data = {
            "grant_type": "refresh_token",
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "refresh_token": self.config.refresh_token,
        }

        response = await self.client.post(
            "https://auth.atlassian.com/oauth/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if response.status_code == 200:
            tokens = response.json()
            self.config.access_token = tokens["access_token"]
            if "refresh_token" in tokens:
                self.config.refresh_token = tokens["refresh_token"]
            self.save_credentials()
            return True
        return False

    async def get_headers(self) -> Dict[str, str]:
        """Get authenticated headers"""
        if not self.config.access_token:
            raise AtlassianError(
                "No access token available. Please authenticate first.",
                "NO_ACCESS_TOKEN",
            )
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make authenticated request with enhanced error handling."""
        headers = await self.get_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers

        try:
            response = await self.client.request(method, url, **kwargs)

            if response.status_code == 401:
                if await self.refresh_access_token():
                    headers = await self.get_headers()
                    kwargs["headers"] = headers
                    response = await self.client.request(method, url, **kwargs)
                else:
                    raise AtlassianError(
                        "Authentication failed. Please re-authenticate.", "AUTH_FAILED"
                    )

            return response

        except httpx.RequestError as e:
            raise AtlassianError(f"Request failed: {str(e)}", "REQUEST_FAILED") from e

    async def get_cloud_id(self, required_scopes: Optional[List[str]] = None) -> str:
        """Get the cloud ID for the configured site"""
        response = await self.make_request(
            "GET", "https://api.atlassian.com/oauth/token/accessible-resources"
        )

        if response.status_code != 200:
            raise AtlassianError(
                f"Failed to get accessible resources: {response.text}",
                "CLOUD_ID_FAILED",
            )

        resources = response.json()
        site_url = self.config.site_url.rstrip("/")

        for resource in resources:
            if resource["url"] == site_url:
                if required_scopes:
                    available_scopes = set(resource.get("scopes", []))
                    missing_scopes = set(required_scopes) - available_scopes
                    if missing_scopes:
                        raise AtlassianError(
                            f"Missing required scopes: {', '.join(missing_scopes)}",
                            "INSUFFICIENT_SCOPES",
                        )
                return resource["id"]

        raise AtlassianError(
            f"Site {site_url} not found in accessible resources", "SITE_NOT_FOUND"
        )
