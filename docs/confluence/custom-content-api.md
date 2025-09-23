# Confluence Custom Content API

## Overview
The Custom Content API allows you to create, manage, and interact with custom content types in Confluence. Custom content enables developers to extend Confluence with application-specific content that integrates seamlessly with the platform while maintaining its own structure and behavior.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:custom-content:confluence` - Read custom content
  - `write:custom-content:confluence` - Create and update custom content
  - `delete:custom-content:confluence` - Delete custom content

## Core Endpoints

### Get Custom Content by Type
Retrieve all custom content of a specific type with filtering and pagination.

**Endpoint:** `GET /wiki/api/v2/custom-content`

**Parameters:**
- `type` (string, required) - Custom content type identifier
- `id` (array[integer], optional) - Filter by custom content IDs (max 250)
- `space-id` (array[integer], optional) - Filter by space IDs (max 100)
- `sort` (CustomContentSortOrder, optional) - Sort order for results
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)
- `body-format` (CustomContentBodyRepresentation, optional) - Content format for body field

**Body Format Support:**
- If custom content body type is `storage`: supports `storage` and `atlas_doc_format`
- If custom content body type is `raw`: supports only `raw` format

### Create Custom Content
Create new custom content in a space, page, blog post, or other custom content.

**Endpoint:** `POST /wiki/api/v2/custom-content`

**Request Body:** CustomContentCreateRequest
- Requires one of: `spaceId`, `pageId`, `blogPostId`, or `customContentId`
- Must specify `type` and content body
- Supports both `storage` and `raw` body types

**Response:** 201 Created with custom content details and location header

### Get Custom Content by ID
Retrieve a specific custom content item with optional metadata.

**Endpoint:** `GET /wiki/api/v2/custom-content/{id}`

**Parameters:**
- `id` (integer, required) - Custom content ID
- `body-format` (CustomContentBodyRepresentationSingle, optional) - Content format
- `version` (integer, optional) - Retrieve specific version
- `include-labels` (boolean, default: false) - Include labels
- `include-properties` (boolean, default: false) - Include content properties
- `include-operations` (boolean, default: false) - Include available operations
- `include-versions` (boolean, default: false) - Include version history
- `include-version` (boolean, default: true) - Include current version
- `include-collaborators` (boolean, default: false) - Include collaborators

### Update Custom Content
Update an existing custom content item.

**Endpoint:** `PUT /wiki/api/v2/custom-content/{id}`

**Request Body:** CustomContentUpdateRequest
- At most one of: `spaceId`, `pageId`, `blogPostId`, or `customContentId`
- Cannot move custom content to different space
- Updates content body and metadata

**Response:** 200 OK with updated custom content details

### Delete Custom Content
Delete custom content (move to trash or permanently delete).

**Endpoint:** `DELETE /wiki/api/v2/custom-content/{id}`

**Parameters:**
- `id` (integer, required) - Custom content ID
- `purge` (boolean, default: false) - Permanently delete (requires space admin)

**Response:** 204 No Content

## Content-Specific Custom Content Endpoints

### Get Custom Content for Specific Content
Retrieve custom content attached to specific content types:

- `GET /wiki/api/v2/pages/{id}/custom-content` - Page custom content
- `GET /wiki/api/v2/blogposts/{id}/custom-content` - Blog post custom content
- `GET /wiki/api/v2/spaces/{id}/custom-content` - Space custom content

## Related Endpoints

### Custom Content Properties
- `GET /wiki/api/v2/custom-content/{custom-content-id}/properties` - Get properties
- `POST /wiki/api/v2/custom-content/{custom-content-id}/properties` - Create property
- `GET /wiki/api/v2/custom-content/{custom-content-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/custom-content/{custom-content-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/custom-content/{custom-content-id}/properties/{property-id}` - Delete property

### Custom Content Attachments
- `GET /wiki/api/v2/custom-content/{id}/attachments` - Get attachments

### Custom Content Comments
- `GET /wiki/api/v2/custom-content/{id}/footer-comments` - Get footer comments

### Custom Content Labels
- `GET /wiki/api/v2/custom-content/{id}/labels` - Get labels

### Custom Content Operations
- `GET /wiki/api/v2/custom-content/{id}/operations` - Get available operations

### Custom Content Versions
- `GET /wiki/api/v2/custom-content/{custom-content-id}/versions` - Get version history
- `GET /wiki/api/v2/custom-content/{custom-content-id}/versions/{version-number}` - Get specific version

### Custom Content Children
- `GET /wiki/api/v2/custom-content/{id}/children` - Get child content

## Example Usage

### Create Custom Content in Space
```http
POST /wiki/api/v2/custom-content
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "type": "ac:my-app:task-list",
  "status": "current",
  "spaceId": "123456789",
  "title": "Project Tasks",
  "body": {
    "representation": "storage",
    "value": "<ac:structured-macro ac:name=\"my-app-task-list\"><ac:parameter ac:name=\"project\">Website Redesign</ac:parameter></ac:structured-macro>"
  }
}
```

### Get Custom Content by Type
```http
GET /wiki/api/v2/custom-content?type=ac:my-app:task-list&space-id=123456789&limit=50
Authorization: Bearer {access_token}
```

### Update Custom Content
```http
PUT /wiki/api/v2/custom-content/987654321
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "id": "987654321",
  "type": "ac:my-app:task-list",
  "status": "current",
  "title": "Updated Project Tasks",
  "body": {
    "representation": "storage",
    "value": "<ac:structured-macro ac:name=\"my-app-task-list\"><ac:parameter ac:name=\"project\">Website Redesign v2</ac:parameter></ac:structured-macro>"
  },
  "version": {
    "number": 2
  }
}
```

## Use Cases

### Application Extensions
- **Custom Widgets:** Create app-specific content widgets and components
- **Data Visualization:** Build custom charts, dashboards, and reports
- **Form Builders:** Create custom forms and data collection interfaces
- **Integration Content:** Display data from external systems in custom formats

### Content Management
- **Structured Data:** Store and display structured information beyond standard pages
- **Templates:** Create reusable content templates and patterns
- **Workflows:** Build custom workflow and approval content types
- **Metadata Display:** Present complex metadata in custom formats

### Collaboration Tools
- **Task Management:** Create custom task lists and project tracking content
- **Decision Trees:** Build interactive decision-making tools
- **Surveys:** Create custom survey and feedback collection content
- **Knowledge Base:** Build specialized knowledge management content types

## Custom Content Types
Custom content types follow the pattern: `ac:{app-key}:{content-type}`

Examples:
- `ac:my-company:project-status`
- `ac:task-manager:task-list`
- `ac:survey-app:feedback-form`

## Body Formats
- **Storage Format:** Confluence storage format with macros and structured content
- **Raw Format:** Plain text or custom markup for specialized content
- **Atlas Document Format:** Rich document format for complex layouts

## Permissions
- **View Custom Content:** Permission to view the container and corresponding space
- **Create Custom Content:** Permission to create custom content in the space
- **Update Custom Content:** Permission to update custom content in the space
- **Delete Custom Content:** Permission to delete custom content in the space
- **Purge Custom Content:** Space administration permissions required

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Error Handling
- **400 Bad Request:** Invalid custom content type, parameters, or request body
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for custom content operations
- **404 Not Found:** Custom content type or item not found
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Types:** Choose meaningful custom content type identifiers
- **Follow Naming Conventions:** Use `ac:{app-key}:{content-type}` pattern
- **Handle Versioning:** Properly manage version numbers for updates
- **Implement Proper Permissions:** Check container and space permissions
- **Support Multiple Formats:** Handle both storage and raw body formats appropriately
- **Cache Appropriately:** Cache custom content data when suitable to reduce API calls
- **Clean Up:** Remove unused custom content to avoid clutter
