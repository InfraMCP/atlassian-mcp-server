#!/usr/bin/env python3
"""Test OAuth flow with minimal required scopes."""

import asyncio
import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import httpx


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback automatically."""

    def do_GET(self):
        if self.path.startswith("/callback"):
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)

            self.server.callback_data = {
                "code": query_params.get("code", [None])[0],
                "state": query_params.get("state", [None])[0],
                "error": query_params.get("error", [None])[0],
            }

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """<html><body><h1>✅ Success!</h1><p>OAuth test completed. You can close this window.</p></body></html>"""
            self.wfile.write(html.encode())
            self.server.callback_received = True
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass


async def test_oauth_flow():
    """Test OAuth flow with minimal scopes for MCP server."""

    site_url = os.getenv("ATLASSIAN_SITE_URL")
    client_id = os.getenv("ATLASSIAN_CLIENT_ID")
    client_secret = os.getenv("ATLASSIAN_CLIENT_SECRET")

    if not all([site_url, client_id, client_secret]):
        print("❌ Missing environment variables:")
        print("   Set ATLASSIAN_SITE_URL, ATLASSIAN_CLIENT_ID, ATLASSIAN_CLIENT_SECRET")
        return False

    # Start callback server
    server = HTTPServer(("localhost", 8080), OAuthCallbackHandler)
    server.callback_received = False
    server.callback_data = None

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
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
        state = secrets.token_urlsafe(32)

        # Minimal required scopes for MCP server
        scopes = [
            "read:jira-work",  # Read issues, projects
            "read:jira-user",  # Read user info
            "write:jira-work",  # Create/update issues
            "read:confluence-content.all",  # Read all content
            "search:confluence",  # Search functionality
            "read:confluence-space.summary",  # Space info
            "read:servicedesk-request",  # Read SM tickets
            "read:me",  # User profile
            "offline_access",  # Token refresh
        ]

        params = {
            "audience": "api.atlassian.com",
            "client_id": client_id,
            "scope": " ".join(scopes),
            "redirect_uri": "http://localhost:8080/callback",
            "state": state,
            "response_type": "code",
            "prompt": "consent",
        }

        auth_url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"

        print(f"🚀 Testing OAuth with minimal MCP scopes ({len(scopes)} scopes):")
        for scope in scopes:
            print(f"   📋 {scope}")

        print("\\n🌐 Opening browser for authorization...")
        webbrowser.open(auth_url)

        # Wait for callback
        timeout = 300
        start_time = time.time()

        while not server.callback_received:
            if time.time() - start_time > timeout:
                print("❌ Authorization timed out after 5 minutes")
                return False
            await asyncio.sleep(0.5)

        callback_data = server.callback_data

        if callback_data["error"]:
            print(f"❌ OAuth error: {callback_data['error']}")
            return False

        print("✅ Authorization received, exchanging for tokens...")

        # Exchange for tokens
        token_data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": callback_data["code"],
            "redirect_uri": "http://localhost:8080/callback",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth.atlassian.com/oauth/token",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code != 200:
                print(f"❌ Token exchange failed: {response.text}")
                return False

            tokens = response.json()

            # Save test tokens
            token_file = Path.home() / ".atlassian_test_tokens.json"
            with open(token_file, "w") as f:
                json.dump(tokens, f, indent=2)
            token_file.chmod(0o600)

            print("✅ OAuth test completed successfully!")
            print(f"📋 Scopes received: {tokens.get('scope', 'None')}")
            print(f"💾 Tokens saved to: {token_file}")

            return True

    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    success = asyncio.run(test_oauth_flow())
    exit(0 if success else 1)
