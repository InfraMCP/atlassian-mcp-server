# Product Overview

## Atlassian MCP Server

An MCP (Model Context Protocol) server that provides AI assistants with seamless OAuth 2.0 authenticated access to Atlassian Cloud services (Jira, Confluence, and Jira Service Management).

## Purpose

Enable AI agents to help users with:
- Work documentation in Confluence
- Jira issue management (create, update, search, comment)
- Service desk request handling
- Project context understanding through content search
- Time and activity logging

## Key Features

- **Seamless OAuth 2.0 Flow**: Automatic browser-based authentication with PKCE security
- **Modular Architecture**: Independently enable/disable Jira, Confluence, and Service Desk modules
- **Minimal Permissions**: Follows least privilege principle with granular OAuth scopes
- **Automatic Token Management**: Handles token refresh transparently
- **Supply Chain Security**: Pinned dependencies with automated vulnerability scanning

## Target Users

Developers and teams using AI assistants (Claude Desktop, Amazon Q, VS Code Continue, GitHub Copilot, Cline) who need to integrate with Atlassian Cloud services.
