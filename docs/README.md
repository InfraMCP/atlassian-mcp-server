# Atlassian MCP Server API Documentation

This directory contains comprehensive API documentation for all Atlassian Cloud APIs for use in developing the Atlassian MCP server.  

## Documentation Structure

```
docs/
├── README.md                           # This file
├── api-specs/                          # OpenAPI specifications
│   ├── confluence-v2-swagger.json      # Confluence API v2 spec
│   ├── jira-platform-swagger.json      # Jira Platform API v3 spec
│   └── jira-service-desk-swagger.v3.json # Jira Service Management API spec
├── confluence/                         # Confluence API v2 documentation
│   ├── ancestors-api.md                # Content hierarchy navigation
│   ├── attachment-api.md               # File attachments management
│   ├── blog-post-api.md               # Blog posts lifecycle
│   ├── comment-api.md                 # Comments (footer & inline)
│   ├── content-api.md                 # Content type utilities
│   ├── content-properties-api.md      # Custom metadata management
│   ├── custom-content-api.md          # Custom content types
│   ├── database-api.md                # Structured data tables
│   ├── folder-api.md                  # Content organization
│   ├── label-api.md                   # Content labeling/tagging
│   ├── like-api.md                    # Social engagement
│   ├── operation-api.md               # Permission discovery
│   ├── page-api.md                    # Core page management
│   ├── smart-link-api.md              # External content embedding
│   ├── space-api.md                   # Space management
│   ├── space-permissions-api.md       # Access control auditing
│   ├── space-properties-api.md        # Space configuration
│   ├── space-roles-api.md             # Role-based permissions (EAP)
│   ├── task-api.md                    # Task management
│   ├── version-api.md                 # Content version history
│   └── whiteboard-api.md              # Visual collaboration
├── jira/                              # Jira Platform API documentation
│   ├── attachments-api.md              # File attachments management
│   ├── comments-api.md                 # Comments and threading
│   ├── dashboards-api.md               # Dashboards and gadgets management
│   ├── fields-api.md                   # Custom fields and contexts
│   ├── issues-api.md                   # Issues API (search, CRUD, comments)
│   ├── projects-api.md                 # Project management and discovery
│   ├── search-api.md                   # JQL search and autocomplete
│   ├── security-api.md                 # Issue security schemes and levels
│   └── users-api.md                    # User management and search
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

### Confluence API v2 (Complete Coverage)
- **Page API** - Core page lifecycle management with full CRUD operations
- **Blog Post API** - Blog post creation and management
- **Comment API** - Footer and inline comments with threading
- **Attachment API** - File upload, download, and management
- **Space API** - Space discovery, creation (EAP), and management
- **Content Properties API** - Custom metadata for all content types
- **Space Properties API** - Space-level configuration and metadata
- **Label API** - Content labeling and categorization
- **Like API** - Social engagement and interaction tracking
- **Task API** - Task management within content
- **Version API** - Complete version history and change tracking
- **Operation API** - Permission discovery and capability checking
- **Ancestors API** - Content hierarchy navigation
- **Custom Content API** - Extensible content types
- **Database API** - Structured data tables
- **Folder API** - Content organization and structure
- **Smart Link API** - External content embedding
- **Whiteboard API** - Visual collaboration tools
- **Space Permissions API** - Access control auditing
- **Space Roles API** - Role-based permissions (EAP)
- **Content API** - Content type utilities

### Jira Platform API v3
- **Issues API** - Comprehensive issue management
  - JQL-based search with advanced filtering
  - Get detailed issue information
  - Create issues with custom fields
  - Update issue fields and metadata
  - Add comments with rich formatting
  - Project integration for context
- **Projects API** - Project management and discovery
  - Project search and filtering capabilities
  - Project details and metadata access
  - Component and version management
  - Project roles and permissions
- **Search API** - JQL search and autocomplete
  - Advanced JQL query execution
  - Search autocomplete and suggestions
  - Query parsing and validation
  - Result pagination and filtering
- **Users API** - User management and search
  - User search and discovery
  - User profile information
  - Assignable user queries
  - Permission-based user filtering
- **Comments API** - Comments and threading
  - Comment CRUD operations
  - Comment properties and metadata
  - Bulk comment operations
  - Comment visibility and permissions
- **Attachments API** - File attachments management
  - File upload and download
  - Attachment metadata and properties
  - Attachment search and filtering
  - File type validation and limits
- **Fields API** - Custom fields and contexts
  - Custom field management
  - Field contexts and configurations
  - Field options and values
  - Field schema definitions
- **Dashboards API** - Dashboard and gadget management
  - Dashboard CRUD operations with sharing permissions
  - Gadget management and positioning
  - Dashboard search and bulk operations
  - Dashboard item properties for custom configuration
- **Security API** - Issue security schemes and levels
  - Security scheme management and configuration
  - Security level creation and member management
  - Project security associations
  - User, group, and role-based security controls

### Jira Service Management API (Complete Coverage)
- **Assets API** - Assets workspace access and management
- **Customer API** - Customer lifecycle and profile management
- **Info API** - Instance information and configuration
- **Knowledgebase API** - Knowledge base article search and access
- **Organization API** - Organization management with custom properties
- **Request API** - Complete service request lifecycle management
- **Requesttype API** - Request type configuration and custom fields
- **Servicedesk API** - Service desk discovery and configuration

## MCP Server Enhancement Opportunities

Based on the comprehensive API documentation, here are suggested enhancements to add valuable features to the Atlassian MCP Server:

### High-Priority Enhancements

#### 1. Enhanced Content Management
**APIs to Implement:**
- **Attachment API** - Enable file upload/download capabilities
- **Content Properties API** - Store custom metadata and configuration
- **Version API** - Access content history and track changes
- **Label API** - Implement content tagging and categorization

**Value:** Provides complete content lifecycle management with file handling, metadata, and organization.

#### 2. Advanced Search and Discovery
**APIs to Implement:**
- **Space API** - Discover and filter spaces by type and criteria
- **Ancestors API** - Navigate content hierarchies and relationships
- **Operation API** - Check user permissions before operations

**Value:** Enables intelligent content discovery and permission-aware operations.

#### 3. Collaboration Features
**APIs to Implement:**
- **Comment API** - Add threaded discussions to content
- **Like API** - Track engagement and social interactions
- **Task API** - Manage actionable items within content

**Value:** Enhances collaborative workflows and team engagement tracking.

#### 4. Service Management Integration
**APIs to Implement:**
- **Service Desk Request API** - Create and manage support tickets
- **Customer API** - Manage customer profiles and organizations
- **Knowledge Base API** - Access support documentation

**Value:** Provides comprehensive service management capabilities for support workflows.

### Medium-Priority Enhancements

#### 5. Advanced Organization
**APIs to Implement:**
- **Folder API** - Organize content in hierarchical structures
- **Database API** - Manage structured data tables
- **Custom Content API** - Support extensible content types

**Value:** Enables advanced content organization and structured data management.

#### 6. Visual Collaboration
**APIs to Implement:**
- **Whiteboard API** - Create and manage visual collaboration spaces
- **Smart Link API** - Embed external content and resources

**Value:** Supports modern visual collaboration and external content integration.

#### 7. Advanced Permissions
**APIs to Implement:**
- **Space Permissions API** - Audit and analyze access control
- **Space Roles API** - Implement role-based permission management (EAP)

**Value:** Provides enterprise-grade permission management and compliance capabilities.

### Implementation Priority Matrix

| Feature Category | Business Value | Implementation Complexity | Priority |
|------------------|----------------|---------------------------|----------|
| File Attachments | High | Medium | 🔴 High |
| Content Properties | High | Low | 🔴 High |
| Comments & Tasks | High | Medium | 🔴 High |
| Service Requests | High | Medium | 🔴 High |
| Advanced Search | Medium | Low | 🟡 Medium |
| Visual Collaboration | Medium | High | 🟡 Medium |
| Permission Management | Low | High | 🟢 Low |

### Suggested Implementation Phases

#### Phase 1: Core Content Enhancement
- Attachment API for file management
- Content Properties API for metadata
- Version API for change tracking
- Comment API for collaboration

#### Phase 2: Service Management
- Service Desk Request API
- Customer API
- Knowledge Base API
- Task API integration

#### Phase 3: Advanced Features
- Whiteboard API for visual collaboration
- Database API for structured data
- Advanced permission management
- Custom content types

### OAuth Scope Requirements

#### Additional Scopes Needed:
```
# Confluence Enhancements
read:attachment:confluence          # File access
write:attachment:confluence         # File upload
read:comment:confluence            # Comment access
write:comment:confluence           # Comment creation
read:task:confluence              # Task management
write:task:confluence             # Task updates
read:label:confluence             # Label access
read:whiteboard:confluence        # Whiteboard access
write:whiteboard:confluence       # Whiteboard creation

# Service Management
read:servicedesk-request          # Request access
write:servicedesk-request         # Request creation
manage:servicedesk-customer       # Customer management
```

## OAuth 2.0 Scopes

### Current Minimal Scopes (9 total)
The MCP Server currently uses minimal OAuth scopes for enhanced security:

#### Confluence (3 scopes)
- `read:page:confluence` - Read page content and metadata
- `read:space:confluence` - Read space information  
- `write:page:confluence` - Create and update pages

#### Jira Platform (3 scopes)
- `read:jira-work` - Read issues, projects, and search
- `read:jira-user` - Read user information
- `write:jira-work` - Create and update issues

#### Service Management (1 scope)
- `read:servicedesk-request` - Read service desk requests

#### Core (2 scopes)
- `read:me` - User profile information
- `offline_access` - Token refresh capability

### Enhanced Scopes for Full API Coverage
To support all documented APIs, additional scopes would be needed:

#### Confluence Enhancements
```
read:attachment:confluence          # File attachments
write:attachment:confluence         # File upload
read:comment:confluence            # Comments access
write:comment:confluence           # Comment creation
delete:comment:confluence          # Comment deletion
read:task:confluence              # Task management
write:task:confluence             # Task updates
read:label:confluence             # Content labels
read:whiteboard:confluence        # Whiteboards
write:whiteboard:confluence       # Whiteboard creation
delete:whiteboard:confluence      # Whiteboard deletion
read:custom-content:confluence    # Custom content
write:custom-content:confluence   # Custom content creation
delete:custom-content:confluence  # Custom content deletion
read:database:confluence          # Database access
write:database:confluence         # Database creation
delete:database:confluence        # Database deletion
read:folder:confluence            # Folder access
write:folder:confluence           # Folder creation
delete:folder:confluence          # Folder deletion
read:embed:confluence             # Smart links
write:embed:confluence            # Smart link creation
delete:embed:confluence           # Smart link deletion
read:space.permission:confluence  # Permission auditing
write:space.permission:confluence # Permission management
write:space:confluence            # Space creation (EAP)
write:configuration:confluence    # Role management (admin)
```

#### Service Management Enhancements
```
write:servicedesk-request         # Request creation
manage:servicedesk-customer       # Customer management
```

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

### Current Confluence Operations
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

### Potential Enhanced Operations
```python
# File attachment management
attachment = await confluence_upload_attachment(
    page_id="123456",
    file_path="./document.pdf",
    comment="Updated specification document"
)

# Content collaboration
comment = await confluence_add_comment(
    page_id="123456",
    comment="Great documentation! One suggestion..."
)

# Task management
task = await confluence_create_task(
    page_id="123456",
    assignee="user@company.com",
    description="Review and update API examples",
    due_date="2024-02-15"
)

# Content organization
await confluence_add_labels(
    page_id="123456",
    labels=["api-docs", "v2", "reviewed"]
)

# Service management integration
ticket = await servicedesk_create_request(
    service_desk_id="1",
    request_type_id="10",
    summary="API documentation update needed",
    description="Please update the authentication section"
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
