# Atlassian MCP Server API Documentation

This directory contains comprehensive API documentation for all Atlassian Cloud APIs used by the MCP Server.

## Documentation Structure

```
docs/
├── README.md                           # This file
├── CONFLUENCE_GRANULAR_SCOPES.md       # Confluence OAuth scope reference
├── JIRA_GRANULAR_SCOPES.md            # Jira OAuth scope reference
├── api-specs/                          # OpenAPI specifications
│   ├── confluence-v2-swagger.json      # Confluence API v2 spec
│   ├── jira-platform-swagger.json      # Jira Platform API v3 spec
│   └── jira-service-desk-swagger.v3.json # Jira Service Management API spec
├── confluence/                         # Confluence API documentation
│   └── pages-api.md                    # Pages API (search, CRUD operations)
├── jira/                              # Jira Platform API documentation
│   └── issues-api.md                   # Issues API (search, CRUD, comments)
└── service-desk/                      # Jira Service Management API documentation
    ├── assets-api.md                   # Assets workspace management
    ├── customer-api.md                 # Customer management
    ├── info-api.md                     # Instance information
    ├── knowledgebase-api.md           # Knowledge base articles
    ├── organization-api.md             # Organization management
    ├── request-api.md                  # Service requests lifecycle
    ├── requesttype-api.md             # Request type configuration
    └── servicedesk-api.md             # Service desk discovery
```

## API Coverage

### Confluence API v2
- **Pages API** - Complete page lifecycle management
  - Search pages with filtering and pagination
  - Get individual page details with content
  - Create new pages with rich content
  - Update existing pages with version control
  - Space integration for organization

### Jira Platform API v3
- **Issues API** - Comprehensive issue management
  - JQL-based search with advanced filtering
  - Get detailed issue information
  - Create issues with custom fields
  - Update issue fields and metadata
  - Add comments with rich formatting
  - Project integration for context

### Jira Service Management API
- **Assets API** - Assets workspace access
- **Customer API** - Customer lifecycle management
- **Info API** - Instance information retrieval
- **Knowledgebase API** - Article search and access
- **Organization API** - Organization management with properties
- **Request API** - Complete service request lifecycle
- **Requesttype API** - Request type configuration and fields
- **Servicedesk API** - Service desk discovery and details

## OAuth 2.0 Scopes

### Granular Scopes (Recommended)
The MCP Server uses granular OAuth scopes for enhanced security and compliance:

#### Confluence
- `read:page:confluence` - Read page content and metadata
- `read:space:confluence` - Read space information
- `write:page:confluence` - Create and update pages

#### Jira Platform
- `read:jira-work` - Read issues, projects, and search
- `read:jira-user` - Read user information
- `write:jira-work` - Create and update issues

#### Jira Service Management
- `read:servicedesk-request` - Read service desk requests
- `write:servicedesk-request` - Create and update requests
- `manage:servicedesk-customer` - Manage customers and organizations

### Classic Scopes (Legacy)
Legacy scopes are still supported but granular scopes are recommended for new implementations.

## Implementation Notes

### Authentication Flow
1. OAuth 2.0 PKCE flow with automatic browser authentication
2. Secure token storage with automatic refresh
3. Cloud ID resolution for multi-tenant support
4. Scope validation and permission checking

### API Patterns
- **Consistent Error Handling** - Standardized error responses across all APIs
- **Pagination Support** - Cursor-based (Confluence) and offset-based (Jira) pagination
- **Field Selection** - Optimize responses by selecting only needed fields
- **Content Formats** - Support for Storage (Confluence) and ADF (Jira) formats

### Performance Considerations
- **Caching** - Cache frequently accessed data like projects and spaces
- **Batch Operations** - Use bulk APIs where available
- **Rate Limiting** - Respect API rate limits with exponential backoff
- **Pagination** - Use appropriate page sizes for different use cases

### Security Best Practices
- **Minimal Scopes** - Request only required OAuth scopes
- **Input Validation** - Validate all user input before API calls
- **Permission Checks** - Verify user permissions before operations
- **Secure Storage** - Store credentials securely with proper file permissions

## Usage Examples

### Confluence Operations
```python
# Search for pages
pages = await confluence_search("API documentation", limit=10)

# Get page content
page = await confluence_get_page("123456")

# Create new page
new_page = await confluence_create_page(
    space_key="DOCS",
    title="New Documentation Page",
    content="<p>Page content in storage format</p>"
)

# Update existing page
updated_page = await confluence_update_page(
    page_id="123456",
    title="Updated Title",
    content="<p>Updated content</p>",
    version=2
)
```

### Jira Operations
```python
# Search for issues
issues = await jira_search("assignee = currentUser()", max_results=50)

# Get issue details
issue = await jira_get_issue("PROJ-123")

# Create new issue
new_issue = await jira_create_issue(
    project_key="PROJ",
    summary="New task",
    description="Task description",
    issue_type="Task"
)

# Update issue
await jira_update_issue(
    issue_key="PROJ-123",
    summary="Updated summary",
    description="Updated description"
)

# Add comment
await jira_add_comment("PROJ-123", "This is a comment")
```

## Error Handling

### Common HTTP Status Codes
- **200 OK** - Successful request
- **201 Created** - Resource created successfully
- **204 No Content** - Successful request with no response body
- **400 Bad Request** - Invalid request parameters or body
- **401 Unauthorized** - Authentication required or invalid
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found or inaccessible
- **409 Conflict** - Resource conflict (e.g., version mismatch)
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server-side error

### Error Response Format
```json
{
  "statusCode": 400,
  "message": "Invalid request",
  "errors": {
    "field": "Field-specific error message"
  }
}
```

## Development Workflow

### Adding New Endpoints
1. **Update OpenAPI Specs** - Download latest API specifications
2. **Document Endpoints** - Create comprehensive endpoint documentation
3. **Implement Functions** - Add MCP server functions
4. **Add OAuth Scopes** - Update required scopes in configuration
5. **Test Integration** - Verify functionality with test cases
6. **Update Documentation** - Keep documentation current

### Testing
- **OAuth Flow** - Test authentication and token refresh
- **API Endpoints** - Verify all implemented endpoints work correctly
- **Error Handling** - Test error scenarios and edge cases
- **Permissions** - Verify scope and permission requirements
- **Integration** - Test end-to-end workflows

## Troubleshooting

### Common Issues
1. **Authentication Failures** - Check OAuth configuration and scopes
2. **Permission Errors** - Verify user has required permissions
3. **API Errors** - Check request format and required fields
4. **Rate Limiting** - Implement proper retry logic with backoff
5. **Version Conflicts** - Handle concurrent updates appropriately

### Debug Resources
- **Log Files** - Check `~/.atlassian-mcp-debug.log` for detailed logs
- **API Documentation** - Reference official Atlassian API docs
- **OAuth Scopes** - Verify required scopes are configured
- **Test Scripts** - Use provided test scripts to verify functionality

## Contributing

When adding new API endpoints or updating existing ones:

1. **Follow Documentation Standards** - Use consistent formatting and structure
2. **Include Examples** - Provide request/response examples
3. **Document Scopes** - Clearly specify required OAuth scopes
4. **Add Error Handling** - Document common error scenarios
5. **Update Tests** - Add or update test cases
6. **Version Control** - Commit documentation with code changes

## References

- [Atlassian Cloud REST APIs](https://developer.atlassian.com/cloud/)
- [Confluence API v2](https://developer.atlassian.com/cloud/confluence/rest/v2/)
- [Jira Platform API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Jira Service Management API](https://developer.atlassian.com/cloud/jira/service-desk/rest/)
- [OAuth 2.0 for Atlassian Cloud](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/)
- [Granular Scopes](https://developer.atlassian.com/cloud/jira/platform/scopes-for-oauth-2-3LO-and-forge-apps/)
