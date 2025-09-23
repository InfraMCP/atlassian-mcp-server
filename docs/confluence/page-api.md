# Confluence Page API

## Overview
The Page API provides comprehensive operations for managing pages in Confluence. This is the core content API that enables creating, reading, updating, and deleting pages, along with managing their properties, versions, and relationships.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:page:confluence` - Read page content and metadata
  - `write:page:confluence` - Create and update pages
  - `delete:page:confluence` - Delete pages

## Core Endpoints

### Get All Pages
Retrieve pages with filtering and pagination.

**Endpoint:** `GET /wiki/api/v2/pages`

**Parameters:**
- `id` (array[integer], optional) - Filter by page IDs (max 250)
- `space-id` (array[integer], optional) - Filter by space IDs (max 100)
- `sort` (PageSortOrder, optional) - Sort order for results
- `status` (array[string], optional) - Filter by status: `current`, `archived`, `deleted`, `trashed` (default: `current`, `archived`)
- `title` (string, optional) - Filter by page title
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field
- `subtype` (string, optional) - Filter by subtype: `live`, `page`
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

### Create Page
Create a new page in a space.

**Endpoint:** `POST /wiki/api/v2/pages`

**Parameters:**
- `embedded` (boolean, default: false) - Create as embedded content in NCS
- `private` (boolean, default: false) - Create private page (creator-only access)
- `root-level` (boolean, default: false) - Create at space root level (not under homepage)

**Request Body:** PageCreateRequest
- Must specify space and page content
- Title required for published pages
- Supports draft and published status

**Response:** 200 OK with created page details

**Size Limit:** Maximum 5 MB request size

### Get Page by ID
Retrieve a specific page with optional metadata.

**Endpoint:** `GET /wiki/api/v2/pages/{id}`

**Parameters:**
- `id` (integer, required) - Page ID
- `body-format` (PrimaryBodyRepresentationSingle, optional) - Content format
- `get-draft` (boolean, default: false) - Retrieve draft version
- `status` (array[string], optional) - Filter by status: `current`, `archived`, `trashed`, `deleted`, `historical`, `draft`
- `version` (integer, optional) - Retrieve specific version
- `include-labels` (boolean, default: false) - Include labels (max 50)
- `include-properties` (boolean, default: false) - Include content properties (max 50)
- `include-operations` (boolean, default: false) - Include available operations (max 50)
- `include-likes` (boolean, default: false) - Include like information (max 50)
- `include-versions` (boolean, default: false) - Include version history (max 50)
- `include-version` (boolean, default: true) - Include current version
- `include-favorited-by-current-user-status` (boolean, default: false) - Include favorite status
- `include-webresources` (boolean, default: false) - Include web resources for rendering
- `include-collaborators` (boolean, default: false) - Include collaborators
- `include-direct-children` (boolean, default: false) - Include direct children

### Update Page
Update an existing page.

**Endpoint:** `PUT /wiki/api/v2/pages/{id}`

**Request Body:** PageUpdateRequest
- Update page content, title, and metadata
- Maintains version history

**Response:** 200 OK with updated page details

### Delete Page
Delete a page (moves to trash, can be restored).

**Endpoint:** `DELETE /wiki/api/v2/pages/{id}`

**Response:** 204 No Content (page moved to trash)

## Specialized Endpoints

### Update Page Title
Update only the page title.

**Endpoint:** `PUT /wiki/api/v2/pages/{id}/title`

**Request Body:** New title information

### Redact Page Content
Redact sensitive content from a page.

**Endpoint:** `POST /wiki/api/v2/pages/{id}/redact`

**Request Body:** Redaction parameters and content

## Related Endpoints

### Page Properties
- `GET /wiki/api/v2/pages/{page-id}/properties` - Get page properties
- `POST /wiki/api/v2/pages/{page-id}/properties` - Create property
- `GET /wiki/api/v2/pages/{page-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/pages/{page-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/pages/{page-id}/properties/{property-id}` - Delete property

### Page Versions
- `GET /wiki/api/v2/pages/{id}/versions` - Get version history
- `GET /wiki/api/v2/pages/{page-id}/versions/{version-number}` - Get specific version

### Page Hierarchy
- `GET /wiki/api/v2/pages/{id}/children` - Get child pages
- `GET /wiki/api/v2/pages/{id}/direct-children` - Get direct children
- `GET /wiki/api/v2/pages/{id}/ancestors` - Get ancestor pages
- `GET /wiki/api/v2/pages/{id}/descendants` - Get all descendants

### Page Associations
- `GET /wiki/api/v2/pages/{id}/attachments` - Get page attachments
- `GET /wiki/api/v2/pages/{id}/custom-content` - Get custom content
- `GET /wiki/api/v2/pages/{id}/labels` - Get page labels
- `GET /wiki/api/v2/pages/{id}/footer-comments` - Get footer comments
- `GET /wiki/api/v2/pages/{id}/inline-comments` - Get inline comments

### Page Engagement
- `GET /wiki/api/v2/pages/{id}/likes/count` - Get like count
- `GET /wiki/api/v2/pages/{id}/likes/users` - Get users who liked
- `GET /wiki/api/v2/pages/{id}/operations` - Get permitted operations

### Page Classification
- `GET /wiki/api/v2/pages/{id}/classification-level` - Get classification level
- `PUT /wiki/api/v2/pages/{id}/classification-level` - Set classification level
- `POST /wiki/api/v2/pages/{id}/classification-level/reset` - Reset classification

## Example Usage

### Create Page
```http
POST /wiki/api/v2/pages?private=false&root-level=false
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "spaceId": "123456789",
  "status": "current",
  "title": "API Integration Guide",
  "body": {
    "representation": "storage",
    "value": "<p>This guide covers API integration best practices...</p>"
  },
  "parentId": "987654321"
}
```

### Get Page with Metadata
```http
GET /wiki/api/v2/pages/555666777?include-properties=true&include-labels=true&include-versions=true
Authorization: Bearer {access_token}
```

### Update Page
```http
PUT /wiki/api/v2/pages/555666777
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "id": "555666777",
  "status": "current",
  "title": "Updated API Integration Guide",
  "body": {
    "representation": "storage",
    "value": "<p>This updated guide covers advanced API integration...</p>"
  },
  "version": {
    "number": 2
  }
}
```

### Get Page Hierarchy
```http
GET /wiki/api/v2/pages/555666777/children?limit=50
Authorization: Bearer {access_token}
```

## Use Cases

### Content Management
- **Documentation:** Create and maintain technical documentation
- **Knowledge Base:** Build comprehensive knowledge repositories
- **Process Documentation:** Document procedures and workflows
- **Project Pages:** Create project-specific information hubs

### Content Publishing
- **Blog-Style Content:** Create informational and educational content
- **Announcements:** Publish company or team announcements
- **Release Notes:** Document software releases and updates
- **Training Materials:** Create educational and training content

### Collaboration
- **Team Workspaces:** Create collaborative work areas
- **Meeting Notes:** Document meeting outcomes and decisions
- **Brainstorming:** Capture ideas and collaborative thinking
- **Review Processes:** Enable content review and approval workflows

### Integration Scenarios
- **Content Migration:** Import content from external systems
- **Automated Publishing:** Generate pages from templates or data
- **Workflow Integration:** Connect pages to business processes
- **Analytics Integration:** Track page usage and engagement

## Page Features
- **Rich Content:** Support for storage format with macros and formatting
- **Version History:** Complete version tracking and rollback capability
- **Hierarchical Structure:** Parent-child relationships for organization
- **Draft Support:** Work-in-progress drafts before publishing
- **Privacy Control:** Private pages for individual use
- **Classification:** Security classification and data governance
- **Properties:** Custom metadata attachment
- **Social Features:** Likes, comments, and collaboration tracking

## Content Formats
- **Storage Format:** Confluence's native format with macros and rich content
- **Atlas Document Format (ADF):** Structured document format for rich editing
- **View Format:** Rendered HTML for display purposes

## Page Status Types
- **`current`** - Published and active pages
- **`archived`** - Archived but accessible pages
- **`draft`** - Unpublished draft pages
- **`trashed`** - Deleted pages in trash (recoverable)
- **`deleted`** - Permanently deleted pages
- **`historical`** - Previous versions of pages

## Permissions
- **View Page:** Permission to view the page and its space
- **Create Page:** Permission to create pages in the space
- **Edit Page:** Permission to modify page content and properties
- **Delete Page:** Permission to delete pages in the space
- **Manage Properties:** Permission to manage page properties and metadata

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Error Handling
- **400 Bad Request:** Invalid page configuration, parameters, or content
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for page operations
- **404 Not Found:** Page or space not found
- **413 Payload Too Large:** Request exceeds 5 MB size limit
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Titles:** Choose clear, searchable page titles
- **Structure Content:** Use proper heading hierarchy and formatting
- **Manage Versions:** Include meaningful version comments for updates
- **Handle Permissions:** Ensure proper space and page permissions
- **Optimize Content:** Use appropriate content formats for use case
- **Regular Maintenance:** Review and update page content regularly
- **Leverage Hierarchy:** Use parent-child relationships for organization
- **Include Metadata:** Use properties and labels for better organization
