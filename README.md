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
- `read:page:confluence` - Read page content (granular scope for v2 API)
- `read:space:confluence` - Read space information (granular scope for v2 API)  
- `write:page:confluence` - Create and update pages (granular scope for v2 API)

#### Service Management API Scopes
Navigate to **Permissions** → **Jira Service Management API** and add:
- `read:servicedesk-request` - Read service management requests
- `write:servicedesk-request` - Create and update service management requests  
- `manage:servicedesk-customer` - Manage service desk customers and participants
- `read:knowledgebase:jira-service-management` - Search knowledge base articles

#### User Identity API Scopes
Navigate to **Permissions** → **User identity API** and add:
- `read:me` - User profile information

#### Core Scopes
These are typically available by default:
- `offline_access` - Token refresh capability

### 3. Install App to Your Atlassian Site

After configuring scopes, you need to install the app to your Atlassian site:

1. In your OAuth app, go to **Authorization** tab
2. Use the **Authorization URL generator** to create an installation URL:
   - Select your configured scopes
   - Choose your Atlassian site from the dropdown
   - Click **Generate URL**
3. **Visit the generated URL** in your browser to install the app to your site
4. **Grant permissions** when prompted by Atlassian

**Note**: This step is required before the MCP server can access your Atlassian data. The app must be installed and authorized for your specific site.

### 4. Get Your Credentials

After installing the app:
1. Go to **Settings** tab in your OAuth app
2. Copy your **Client ID** and **Client Secret**
3. Set the environment variables (see Configuration section below)

### 5. Scope Configuration Summary

**Minimal Required (12 scopes):**
```
read:jira-work
read:jira-user  
write:jira-work
read:page:confluence
read:space:confluence
write:page:confluence
read:servicedesk-request
write:servicedesk-request
manage:servicedesk-customer
read:knowledgebase:jira-service-management
read:me
offline_access
```

**Optional (add only if needed):**
```
write:servicedesk-request      # Only if creating service tickets
manage:* scopes                # Only for administrative operations
```

### 6. Troubleshooting Scopes

If you get scope-related errors:
- **"scope does not match"**: The scope isn't added to your OAuth app in Developer Console
- **"Current user not permitted"**: User lacks product-level permissions (contact your Atlassian admin)
- **"Unauthorized"**: Check that all required scopes are properly configured

**Note**: After adding new scopes to your OAuth app, you must re-authenticate using the `authenticate_atlassian` tool to get fresh tokens with the new permissions.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip3 package manager
- Access to an Atlassian Cloud site
- OAuth app configured (see OAuth App Setup above)

### Install from PyPI (Recommended)

```bash
pip3 install atlassian-mcp-server
```

### Install from GitHub Repository

```bash
# Install directly from GitHub repository
pip3 install git+https://github.com/rorymcmahon/atlassian-mcp-server.git
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/rorymcmahon/atlassian-mcp-server.git
cd atlassian-mcp-server

# Install in development mode
pip3 install -e .
```

### Verify Installation

```bash
# Check that the command is available
atlassian-mcp-server --help

# Or check the Python module
python -m atlassian_mcp_server --help
```

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
- `confluence_create_page(space_key, title, content, parent_id=None)` - Create new Confluence page
- `confluence_update_page(page_id, title, content, version)` - Update existing Confluence page

### Service Management Operations

#### Discovery Tools (Essential for AI Agents)
- `servicedesk_check_availability()` - Check if Jira Service Management is configured
- `servicedesk_list_service_desks(limit=50)` - List available service desks for creating requests
- `servicedesk_get_service_desk(service_desk_id)` - Get detailed service desk information
- `servicedesk_list_request_types(service_desk_id=None, limit=50)` - List available request types
- `servicedesk_get_request_type(service_desk_id, request_type_id)` - Get detailed request type information
- `servicedesk_get_request_type_fields(service_desk_id, request_type_id)` - Get required/optional fields for request type

#### Request Management
- `servicedesk_get_requests(service_desk_id=None, limit=50)` - Get service desk requests
- `servicedesk_get_request(issue_key)` - Get specific service desk request details
- `servicedesk_create_request(service_desk_id, request_type_id, summary, description)` - Create new service request
- `servicedesk_add_comment(issue_key, comment, public=True)` - Add comment to service request
- `servicedesk_get_request_comments(issue_key, limit=50)` - Get comments for a service request
- `servicedesk_get_request_status(issue_key)` - Get service request status
- `servicedesk_get_request_transitions(issue_key)` - Get available status transitions for request
- `servicedesk_transition_request(issue_key, transition_id, comment=None)` - Transition request to new status

#### Approval & Participant Management
- `servicedesk_get_approvals(issue_key)` - Get approval information for request
- `servicedesk_approve_request(issue_key, approval_id, decision)` - Approve or decline request approval
- `servicedesk_get_participants(issue_key)` - Get participants for request
- `servicedesk_add_participants(issue_key, usernames)` - Add participants to request (with confirmation prompts)
- `servicedesk_manage_notifications(issue_key, subscribe)` - Subscribe/unsubscribe from request notifications

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

# Service Management workflow example
# 1. Discover available service desks
service_desks = await servicedesk_list_service_desks()
service_desk_id = service_desks[0]["id"]

# 2. Find available request types
request_types = await servicedesk_list_request_types(service_desk_id)
request_type_id = request_types[0]["id"]

# 3. Check required fields for the request type
fields = await servicedesk_get_request_type_fields(service_desk_id, request_type_id)
required_fields = [f for f in fields if f.get("required", False)]

# 4. Create a service desk request
new_request = await servicedesk_create_request(
    service_desk_id=service_desk_id,
    request_type_id=request_type_id,
    summary="Need help with system access",
    description="User needs access to the development environment"
)

# 5. Add a comment and manage the request
await servicedesk_add_comment(new_request["issueKey"], "Additional context: User is a new team member")

# 6. Check available transitions and move to next status
transitions = await servicedesk_get_request_transitions(new_request["issueKey"])
if transitions:
    await servicedesk_transition_request(new_request["issueKey"], transitions[0]["id"], "Moving to in progress")
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

### Essential Scopes (12 total)
- **Jira**: `read:jira-work`, `read:jira-user`, `write:jira-work`
- **Confluence**: `read:page:confluence`, `read:space:confluence`, `write:page:confluence`
- **Service Management**: `read:servicedesk-request`, `write:servicedesk-request`, `manage:servicedesk-customer`, `read:knowledgebase:jira-service-management`
- **Core**: `read:me`, `offline_access`

### Optional Scopes (add only if needed)
- `write:servicedesk-request` - Only if creating service management tickets
- `manage:*` scopes - Only for administrative operations

## Important: Granular Scopes for v2 API

This MCP server uses **granular scopes** for Confluence operations to ensure compatibility with Confluence v2 API endpoints. The v2 API provides better performance and future-proofing compared to the deprecated v1 REST API.

**Granular vs Classic Scopes:**
- **Granular** (recommended): `read:page:confluence`, `write:page:confluence` - Works with v2 API
- **Classic** (deprecated): `read:confluence-content.all`, `write:confluence-content` - Only works with v1 API

If you previously configured classic scopes, you'll need to update your OAuth app to use granular scopes and re-authenticate to get fresh tokens.

## Development

The server is built using:
- **FastMCP**: Modern MCP server framework
- **httpx**: Async HTTP client
- **Pydantic**: Data validation and settings management

## License

MIT License - see LICENSE file for details.

## Planned Features (Future Releases)

### 🎯 Service Management Enhancements

The following Jira Service Management features are planned for future releases to provide comprehensive support ticket management capabilities:

**Reference:** [Jira Service Management REST API Documentation](https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/)

#### Request Management
- **`servicedesk_create_request()`** - Create service desk requests with custom fields and attachments
- **`servicedesk_get_request_status()`** - Track request status and workflow transitions  
- **`servicedesk_transition_request()`** - Move requests through workflow states
- **`servicedesk_add_request_comment()`** - Add public/internal comments to requests

#### Approval Workflows  
- **`servicedesk_get_approvals()`** - View pending and completed approvals
- **`servicedesk_approve_request()`** - Approve or decline approval requests
- **`servicedesk_get_approval_status()`** - Check approval workflow status

#### Participant & Notification Management
- **`servicedesk_add_participants()`** - Add users to request conversations
- **`servicedesk_manage_notifications()`** - Subscribe/unsubscribe from request updates
- **`servicedesk_get_participants()`** - List all request participants

#### SLA & Performance Tracking
- **`servicedesk_get_sla_info()`** - Monitor SLA performance and breach status
- **`servicedesk_get_request_metrics()`** - Track response times and resolution metrics

#### Attachment & File Management
- **`servicedesk_upload_attachment()`** - Upload files to requests with comments
- **`servicedesk_get_attachments()`** - List and download request attachments

#### Customer Feedback
- **`servicedesk_submit_feedback()`** - Submit CSAT ratings and feedback
- **`servicedesk_get_feedback()`** - Retrieve customer satisfaction data

### 📋 Required OAuth Scopes

To support these Service Management features, the following **additional scopes** will be required:

#### Classic Scopes (Current Approach)
```
write:servicedesk-request          # Create and update service requests
read:request.approval              # View approval workflows  
write:request.approval             # Approve/decline requests
read:request.attachment            # Access request attachments
write:request.attachment           # Upload files to requests
read:request.participant           # View request participants
write:request.participant          # Manage request participants
read:request.notification          # Check notification subscriptions
write:request.notification         # Manage notification preferences
read:request.feedback              # View customer feedback
write:request.feedback             # Submit feedback and ratings
```

#### Granular Scopes (Alternative)
```
read:request:jira-service-management           # Read service requests
write:request:jira-service-management          # Create/update requests
read:request.approval:jira-service-management  # View approvals
write:request.approval:jira-service-management # Process approvals
read:request.attachment:jira-service-management # Access attachments
write:request.attachment:jira-service-management # Upload attachments
read:request.participant:jira-service-management # View participants
write:request.participant:jira-service-management # Manage participants
read:request.notification:jira-service-management # View notifications
write:request.notification:jira-service-management # Manage notifications
read:request.feedback:jira-service-management  # View feedback
write:request.feedback:jira-service-management # Submit feedback
read:request.sla:jira-service-management       # View SLA metrics
read:request.status:jira-service-management    # View request status
write:request.status:jira-service-management   # Update request status
```

### 🎯 Use Cases

These Service Management features will enable AI agents to:

- **Automated Ticket Creation** - Create service requests from conversations with proper categorization
- **Approval Automation** - Process approval workflows and notify stakeholders  
- **SLA Monitoring** - Track service level agreements and alert on potential breaches
- **Customer Communication** - Manage participant lists and notification preferences
- **Feedback Collection** - Gather and analyze customer satisfaction data
- **File Management** - Handle attachments and documentation for service requests
- **Workflow Automation** - Move requests through appropriate workflow states
- **Performance Analytics** - Monitor team performance and service quality metrics

### 📅 Implementation Status

**Phase 1 (v0.3.0) - ✅ COMPLETED:** Core request management (create, status, comments)  
**Phase 2 (v0.3.1) - ✅ COMPLETED:** Approval workflows and participant management  
**Phase 3 (v0.3.2) - 🚧 PLANNED:** SLA monitoring, attachments, and feedback systems
