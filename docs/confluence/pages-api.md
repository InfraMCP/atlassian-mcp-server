# Confluence Pages API (v2)

The Confluence Pages API v2 provides comprehensive page management capabilities including search, retrieval, creation, and updates. This documentation covers the endpoints used in the Atlassian MCP Server.

## Base URL Structure

All Confluence v2 API endpoints follow this pattern:
```
https://api.atlassian.com/ex/confluence/{cloudId}/wiki/api/v2/{endpoint}
```

## OAuth 2.0 Scopes Required

### Granular Scopes (Recommended)
- **`read:page:confluence`** - Read page content and metadata
- **`read:space:confluence`** - Read space information  
- **`write:page:confluence`** - Create and update pages

### Classic Scopes (Legacy)
- **`read:confluence-content.all`** - Read all content (deprecated)
- **`write:confluence-content`** - Write content (deprecated)

## Core Page Operations

### Search Pages

**GET** `/pages`

Returns a list of pages in the Confluence instance, with optional filtering and search capabilities.

**OAuth 2.0 Scopes**: `read:page:confluence`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | string | Filter pages by title (exact match or contains) |
| `space-id` | array | Filter by space IDs |
| `space-key` | array | Filter by space keys |
| `status` | array | Filter by page status: `current`, `trashed`, `historical`, `draft` |
| `body-format` | string | Format for page body: `storage`, `atlas_doc_format`, `view` |
| `include-labels` | boolean | Include page labels in response |
| `sort` | string | Sort field: `id`, `created-date`, `modified-date`, `title` |
| `cursor` | string | Pagination cursor for next page |
| `limit` | integer | Maximum results per page (default: 25, max: 250) |

#### Response

**200 - Success**
```json
{
  "results": [
    {
      "id": "123456",
      "status": "current",
      "title": "Page Title",
      "spaceId": "789012",
      "parentId": "345678",
      "authorId": "user123",
      "createdAt": "2023-01-01T12:00:00.000Z",
      "version": {
        "number": 1,
        "message": "Initial version",
        "minorEdit": false,
        "authorId": "user123",
        "createdAt": "2023-01-01T12:00:00.000Z"
      },
      "body": {
        "storage": {
          "value": "<p>Page content in storage format</p>",
          "representation": "storage"
        }
      },
      "_links": {
        "webui": "/spaces/SPACE/pages/123456/Page+Title"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/pages?cursor=next_cursor"
  }
}
```

#### Implementation Notes
- Use `title` parameter for search functionality
- Pagination uses cursor-based approach (not offset-based)
- Default body format is `storage` (Confluence's internal format)
- Results are ordered by relevance when searching, or by ID when listing

---

### Get Page by ID

**GET** `/pages/{id}`

Returns a specific page by its ID with full content and metadata.

**OAuth 2.0 Scopes**: `read:page:confluence`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The page ID |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `body-format` | string | Format for page body: `storage`, `atlas_doc_format`, `view` |
| `get-draft` | boolean | Get draft version if available |
| `version` | integer | Get specific version number |
| `include-labels` | boolean | Include page labels |

#### Response

**200 - Success**
```json
{
  "id": "123456",
  "status": "current",
  "title": "Page Title",
  "spaceId": "789012",
  "parentId": "345678",
  "authorId": "user123",
  "createdAt": "2023-01-01T12:00:00.000Z",
  "version": {
    "number": 3,
    "message": "Updated content",
    "minorEdit": false,
    "authorId": "user456",
    "createdAt": "2023-01-03T12:00:00.000Z"
  },
  "body": {
    "storage": {
      "value": "<p>Full page content in storage format</p>",
      "representation": "storage"
    }
  },
  "space": {
    "id": "789012",
    "key": "SPACE",
    "name": "Space Name",
    "type": "global"
  },
  "_links": {
    "webui": "/spaces/SPACE/pages/123456/Page+Title",
    "editui": "/pages/resumedraft.action?draftId=123456",
    "tinyui": "/x/AAABBg"
  }
}
```

**404 - Not Found**
Page does not exist or user lacks permission.

---

### Create Page

**POST** `/pages`

Creates a new page in a Confluence space.

**OAuth 2.0 Scopes**: `write:page:confluence`

#### Request Body

```json
{
  "spaceId": "789012",
  "status": "current",
  "title": "New Page Title",
  "parentId": "345678",
  "body": {
    "representation": "storage",
    "value": "<p>Page content in storage format</p>"
  }
}
```

#### Required Fields
- **`spaceId`** - The space where the page will be created
- **`title`** - The page title (must be unique within the space)
- **`body.representation`** - Content format (`storage` recommended)
- **`body.value`** - The page content

#### Optional Fields
- **`parentId`** - Parent page ID (creates page as child)
- **`status`** - Page status (`current` or `draft`)

#### Response

**200 - Success**
Returns the created page with full details including assigned ID and version information.

**400 - Bad Request**
Invalid request data (e.g., missing required fields, invalid space ID).

**403 - Forbidden**
User lacks permission to create pages in the specified space.

**409 - Conflict**
Page with the same title already exists in the space.

#### Implementation Notes
- Page titles must be unique within a space
- Storage format is Confluence's internal XHTML-based format
- Parent-child relationships create page hierarchies
- New pages start at version 1

---

### Update Page

**PUT** `/pages/{id}`

Updates an existing page with new content and/or metadata.

**OAuth 2.0 Scopes**: `write:page:confluence`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | The page ID to update |

#### Request Body

```json
{
  "id": "123456",
  "status": "current",
  "title": "Updated Page Title",
  "body": {
    "representation": "storage",
    "value": "<p>Updated page content</p>"
  },
  "version": {
    "number": 4,
    "message": "Updated via API"
  }
}
```

#### Required Fields
- **`id`** - Must match the page ID in the URL
- **`version.number`** - Must be current version + 1
- **`body.representation`** - Content format
- **`body.value`** - Updated content

#### Optional Fields
- **`title`** - New page title
- **`version.message`** - Version comment
- **`status`** - Page status

#### Response

**200 - Success**
Returns the updated page with new version information.

**400 - Bad Request**
Invalid request data or version conflict.

**403 - Forbidden**
User lacks permission to update the page.

**404 - Not Found**
Page does not exist.

**409 - Conflict**
Version number conflict (page was updated by another user).

#### Implementation Notes
- Version numbers must be sequential (current + 1)
- Concurrent updates will result in 409 conflicts
- Always fetch current version before updating
- Title changes must maintain uniqueness within space

## Spaces Integration

### Get Spaces

**GET** `/spaces`

Returns available spaces for page creation and organization.

**OAuth 2.0 Scopes**: `read:space:confluence`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `keys` | array | Filter by space keys |
| `type` | string | Filter by space type: `global`, `personal` |
| `status` | string | Filter by status: `current`, `archived` |
| `sort` | string | Sort by: `key`, `name`, `created-date` |
| `cursor` | string | Pagination cursor |
| `limit` | integer | Results per page (max: 250) |

#### Response

**200 - Success**
```json
{
  "results": [
    {
      "id": "789012",
      "key": "SPACE",
      "name": "Space Name",
      "type": "global",
      "status": "current",
      "authorId": "user123",
      "createdAt": "2023-01-01T12:00:00.000Z",
      "homepageId": "123456",
      "_links": {
        "webui": "/spaces/SPACE"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/spaces?cursor=next_cursor"
  }
}
```

## Error Handling

### Common Error Responses

**400 - Bad Request**
```json
{
  "statusCode": 400,
  "message": "Invalid request",
  "reason": "INVALID_REQUEST_DATA"
}
```

**401 - Unauthorized**
```json
{
  "statusCode": 401,
  "message": "Unauthorized",
  "reason": "AUTHENTICATION_REQUIRED"
}
```

**403 - Forbidden**
```json
{
  "statusCode": 403,
  "message": "Forbidden",
  "reason": "INSUFFICIENT_PERMISSIONS"
}
```

**404 - Not Found**
```json
{
  "statusCode": 404,
  "message": "Page not found",
  "reason": "RESOURCE_NOT_FOUND"
}
```

**409 - Conflict**
```json
{
  "statusCode": 409,
  "message": "Version conflict",
  "reason": "VERSION_CONFLICT"
}
```

## Content Formats

### Storage Format
Confluence's internal XHTML-based format:
```html
<p>Simple paragraph</p>
<h1>Heading</h1>
<ul>
  <li>List item</li>
</ul>
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p>Info macro content</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Atlas Document Format (ADF)
JSON-based format for rich content:
```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Simple paragraph"
        }
      ]
    }
  ]
}
```

## Best Practices

### Performance
- Use cursor-based pagination for large result sets
- Limit search results with appropriate `limit` values
- Cache space information to avoid repeated lookups

### Content Management
- Always check current version before updates
- Use meaningful version messages for change tracking
- Validate content format before submission

### Error Handling
- Handle version conflicts gracefully with retry logic
- Check permissions before attempting operations
- Provide user-friendly error messages

### Security
- Use granular scopes for minimal required permissions
- Validate user input before creating/updating content
- Respect space permissions and access controls
