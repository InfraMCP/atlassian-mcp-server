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

1. Go to [Atlassian Developer Console](https://developer.atlassian.com/console/myapps/)
2. Create a new OAuth 2.0 app
3. Set redirect URI to `http://localhost:8080/callback`
4. Add the following **minimal required scopes**:

### Jira API Scopes
- `read:jira-work` - Read issues, projects, and search
- `read:jira-user` - Read user information
- `write:jira-work` - Create and update issues

### Confluence API Scopes  
- `read:confluence-content.all` - Read all Confluence content
- `search:confluence` - Search Confluence pages
- `read:confluence-space.summary` - Read space information

### Service Management API Scopes
- `read:servicedesk-request` - Read service management tickets

### Core Scopes
- `read:me` - User profile information
- `offline_access` - Token refresh capability

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
