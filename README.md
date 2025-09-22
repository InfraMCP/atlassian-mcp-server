# Atlassian MCP Server

MCP server for Atlassian Cloud (Confluence & Jira) with seamless OAuth 2.0 authentication. This server enables AI agents to help users document work in Confluence, manage Jira issues, and understand project context.

## Features

- **Seamless OAuth 2.0 Flow**: Automatic browser-based authentication with PKCE security
- **Jira Integration**: Search, create, and update issues; add comments; manage work
- **Confluence Integration**: Search and read content for context understanding
- **Service Management**: Access support tickets and requests
- **Automatic Token Management**: Handles token refresh automatically
- **Minimal Permissions**: Follows least privilege principle with only required scopes

## Use Cases

This MCP server is designed to help AI agents assist users with:

- **Work Documentation**: Help document work progress and decisions in Confluence
- **Issue Management**: Create, update, and track Jira issues based on conversations
- **Context Understanding**: Read Confluence pages to understand project background
- **Time & Activity Logging**: Track work activities and time spent on tasks
- **Service Requests**: Access service management tickets for support context
- **Project Coordination**: Search across Jira and Confluence for project information

## Installation

```bash
pip install -e .
```

## OAuth App Setup

### 1. Create OAuth App

1. Go to [Atlassian Developer Console](https://developer.atlassian.com/console/myapps/)
2. Click **Create** → **OAuth 2.0 integration**
3. Enter your app name and accept the terms
4. Set **Callback URL** to: `http://localhost:8080/callback`

### 2. Configure Required Scopes

**IMPORTANT**: You must add these exact scopes to your OAuth app before the MCP server can function properly.

#### Jira API Scopes
Navigate to **Permissions** → **Jira API** and add:
- `read:jira-work` - Read issues, projects, and search
- `read:jira-user` - Read user information  
- `write:jira-work` - Create and update issues

#### Confluence API Scopes
Navigate to **Permissions** → **Confluence API** and add:
- `read:confluence-content.all` - Read all Confluence content
- `search:confluence` - Search Confluence pages
- `read:confluence-space.summary` - Read space information
- `write:confluence-content` - Create and update pages *(optional - only if you need page creation)*

#### Service Management API Scopes
Navigate to **Permissions** → **Jira Service Management API** and add:
- `read:servicedesk-request` - Read service management tickets

#### User Identity API Scopes
Navigate to **Permissions** → **User identity API** and add:
- `read:me` - User profile information

#### Core Scopes
These are typically available by default:
- `offline_access` - Token refresh capability

### 3. Get Your Credentials

After configuring scopes:
1. Go to **Settings** tab in your OAuth app
2. Copy your **Client ID** and **Client Secret**
3. Set the environment variables (see Configuration section below)

### 4. Scope Configuration Summary

**Minimal Required (8 scopes):**
```
read:jira-work
read:jira-user  
write:jira-work
read:confluence-content.all
search:confluence
read:confluence-space.summary
read:servicedesk-request
read:me
offline_access
```

**Optional (add only if needed):**
```
write:confluence-content        # Only if creating/editing pages
write:servicedesk-request      # Only if creating service tickets
manage:* scopes                # Only for administrative operations
```

### 5. Troubleshooting Scopes

If you get scope-related errors:
- **"scope does not match"**: The scope isn't added to your OAuth app in Developer Console
- **"Current user not permitted"**: User lacks product-level permissions (contact your Atlassian admin)
- **"Unauthorized"**: Check that all required scopes are properly configured

**Note**: After adding new scopes to your OAuth app, you must re-authenticate using the `authenticate_atlassian` tool to get fresh tokens with the new permissions.

## Configuration

Set the following environment variables:

```bash
export ATLASSIAN_SITE_URL="https://your-domain.atlassian.net"
export ATLASSIAN_CLIENT_ID="your-oauth-client-id"
export ATLASSIAN_CLIENT_SECRET="your-oauth-client-secret"
```

## Usage

```bash
# Start the MCP server
python -m atlassian_mcp_server

# Or run directly
python src/atlassian_mcp_server/server.py
```

## MCP Client Configuration

### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "atlassian-mcp-server",
      "env": {
        "ATLASSIAN_SITE_URL": "https://your-domain.atlassian.net",
        "ATLASSIAN_CLIENT_ID": "your-oauth-client-id",
        "ATLASSIAN_CLIENT_SECRET": "your-oauth-client-secret"
      }
    }
  }
}
```

### Amazon Q Developer CLI

Create an agent configuration file:

**File**: `~/.aws/amazonq/cli-agents/atlassian.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/aws/amazon-q-developer-cli/refs/heads/main/schemas/agent-v1.json",
  "name": "atlassian",
  "description": "Atlassian Jira and Confluence integration agent",
  "prompt": "You are an AI assistant with access to Atlassian Jira and Confluence. Help users manage issues, search content, and document their work.",
  "mcpServers": {
    "atlassian-mcp-server": {
      "command": "atlassian-mcp-server",
      "args": [],
      "env": {
        "ATLASSIAN_SITE_URL": "https://your-domain.atlassian.net",
        "ATLASSIAN_CLIENT_ID": "your-oauth-client-id",
        "ATLASSIAN_CLIENT_SECRET": "your-oauth-client-secret"
      },
      "autoApprove": ["*"],
      "disabled": false,
      "timeout": 60000,
      "initTimeout": 120000
    }
  },
  "tools": [
    "@atlassian-mcp-server/*"
  ],
  "allowedTools": [
    "@atlassian-mcp-server/*"
  ]
}
```

Then use: `q chat --agent atlassian`

### VS Code with Continue

Add to your Continue configuration:

**File**: `~/.continue/config.json`

```json
{
  "models": [...],
  "mcpServers": {
    "atlassian": {
      "command": "atlassian-mcp-server",
      "env": {
        "ATLASSIAN_SITE_URL": "https://your-domain.atlassian.net",
        "ATLASSIAN_CLIENT_ID": "your-oauth-client-id",
        "ATLASSIAN_CLIENT_SECRET": "your-oauth-client-secret"
      }
    }
  }
}
```

### VS Code with GitHub Copilot Chat

For GitHub Copilot Chat with MCP support, add to workspace settings:

**File**: `.vscode/settings.json`

```json
{
  "github.copilot.chat.mcp.servers": {
    "atlassian": {
      "command": "atlassian-mcp-server",
      "env": {
        "ATLASSIAN_SITE_URL": "https://your-domain.atlassian.net",
        "ATLASSIAN_CLIENT_ID": "your-oauth-client-id",
        "ATLASSIAN_CLIENT_SECRET": "your-oauth-client-secret"
      }
    }
  }
}
```

### Cline (VS Code Extension)

Add to Cline's MCP configuration:

**File**: `~/.cline/mcp_servers.json`

```json
{
  "atlassian": {
    "command": "atlassian-mcp-server",
    "env": {
      "ATLASSIAN_SITE_URL": "https://your-domain.atlassian.net",
      "ATLASSIAN_CLIENT_ID": "your-oauth-client-id",
      "ATLASSIAN_CLIENT_SECRET": "your-oauth-client-secret"
    }
  }
}
```

### Environment Variables Setup

For security, set environment variables instead of hardcoding in config files:

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export ATLASSIAN_SITE_URL="https://your-domain.atlassian.net"
export ATLASSIAN_CLIENT_ID="your-oauth-client-id"
export ATLASSIAN_CLIENT_SECRET="your-oauth-client-secret"
```

Then use in configurations:
```json
{
  "env": {
    "ATLASSIAN_SITE_URL": "${ATLASSIAN_SITE_URL}",
    "ATLASSIAN_CLIENT_ID": "${ATLASSIAN_CLIENT_ID}",
    "ATLASSIAN_CLIENT_SECRET": "${ATLASSIAN_CLIENT_SECRET}"
  }
}
```

## Authentication Flow

1. Start the MCP server
2. Use the `authenticate_atlassian` tool to begin OAuth flow
3. Browser opens automatically to Atlassian login
4. After authorization, authentication completes automatically
5. Credentials are saved locally for future use

## Available Tools

### Authentication
- `authenticate_atlassian()` - Start seamless OAuth authentication flow

### Jira Operations
- `jira_search(jql, max_results=50)` - Search issues with JQL
- `jira_get_issue(issue_key)` - Get specific issue details
- `jira_create_issue(project_key, summary, description, issue_type="Task")` - Create new issue
- `jira_update_issue(issue_key, summary=None, description=None)` - Update existing issue
- `jira_add_comment(issue_key, comment)` - Add comment to issue

### Confluence Operations
- `confluence_search(query, limit=10)` - Search Confluence content
- `confluence_get_page(page_id)` - Get specific page content

## Example Usage

```python
# Authenticate (opens browser automatically)
await authenticate_atlassian()

# Search for recent issues assigned to current user
issues = await jira_search("assignee = currentUser() AND status != Done ORDER BY created DESC", max_results=10)

# Create a new issue
new_issue = await jira_create_issue(
    project_key="PROJ",
    summary="Document API integration approach",
    description="Need to document the approach for integrating with external APIs",
    issue_type="Task"
)

# Search Confluence for related documentation
docs = await confluence_search("API integration", limit=5)

# Get specific page content for context
page_content = await confluence_get_page("123456789")
```

## Testing

The repository includes comprehensive tests to verify functionality:

```bash
# Test OAuth flow with minimal scopes
python tests/test_oauth.py

# Test core functionality (run after OAuth test)
python tests/test_functionality.py
```

## Security Features

- **PKCE (Proof Key for Code Exchange)**: Enhanced OAuth security
- **Minimal Scopes**: Only requests permissions needed for functionality
- **Secure Storage**: Credentials stored with 0600 file permissions
- **Automatic Token Refresh**: Handles expired tokens transparently
- **State Validation**: Prevents CSRF attacks during OAuth flow

## Troubleshooting

### Authentication Issues
- Ensure redirect URI matches exactly: `http://localhost:8080/callback`
- Check that all required scopes are configured in Atlassian Developer Console
- Verify environment variables are set correctly

### Permission Issues
- Ensure your user has appropriate Jira and Confluence access
- Check that OAuth app has all required scopes enabled
- Verify user is in correct groups (e.g., confluence-users)

### API Errors
- Check that your Atlassian site URL is correct
- Ensure you have proper permissions for the resources you're accessing
- Run the test scripts to verify functionality

## Scope Requirements

This MCP server uses **minimal required scopes** following the principle of least privilege:

### Essential Scopes (9 total)
- **Jira**: `read:jira-work`, `read:jira-user`, `write:jira-work`
- **Confluence**: `read:confluence-content.all`, `search:confluence`, `read:confluence-space.summary`
- **Service Management**: `read:servicedesk-request`
- **Core**: `read:me`, `offline_access`

### Optional Scopes (add only if needed)
- `write:servicedesk-request` - Only if creating service management tickets
- `write:confluence-content` - Only if creating/editing Confluence pages
- `manage:*` scopes - Only for administrative operations

## Development

The server is built using:
- **FastMCP**: Modern MCP server framework
- **httpx**: Async HTTP client
- **Pydantic**: Data validation and settings management

## License

MIT License - see LICENSE file for details.
