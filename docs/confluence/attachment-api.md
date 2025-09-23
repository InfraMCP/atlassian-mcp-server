# Confluence Attachment API (v2)

The Confluence Attachment API v2 provides comprehensive attachment management capabilities including retrieval, deletion, and metadata management for files attached to pages, blog posts, and custom content.

## OAuth 2.0 Scopes Required

### Granular Scopes (Current)
- **`read:attachment:confluence`** - Read attachment content and metadata
- **`delete:attachment:confluence`** - Delete attachments

### Connect App Scopes
- **READ** - For reading attachments
- **DELETE** - For deleting attachments

## Core Attachment Operations

### Get All Attachments

**GET** `/attachments`

Returns all attachments in the Confluence instance with optional filtering and pagination.

**Permissions required**: Permission to view the container of the attachment.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `read:attachment:confluence`

**Connect app scope required**: READ

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sort` | string | Sort order: `created-date`, `modified-date`, `title` |
| `cursor` | string | Pagination cursor for next page |
| `status` | array | Filter by status: `current`, `archived`, `trashed` (default: `current`, `archived`) |
| `mediaType` | string | Filter by media type (e.g., `image/png`, `application/pdf`) |
| `filename` | string | Filter by filename |
| `limit` | integer | Maximum results per page (default: 50, max: 250) |

#### Response

**200 - Success**
```json
{
  "results": [
    {
      "id": "att123456",
      "status": "current",
      "title": "document.pdf",
      "createdAt": "2023-01-01T12:00:00.000Z",
      "fileId": "file123456",
      "fileSize": 1024000,
      "mediaType": "application/pdf",
      "mediaTypeDescription": "PDF Document",
      "comment": "Important document",
      "version": {
        "number": 1,
        "message": "Initial upload",
        "createdAt": "2023-01-01T12:00:00.000Z",
        "authorId": "user123"
      },
      "_links": {
        "download": "/wiki/download/attachments/123456/document.pdf",
        "webui": "/pages/viewpage.action?pageId=123456"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/attachments?cursor=next_cursor",
    "base": "https://your-domain.atlassian.net/wiki"
  }
}
```

**Headers**
- **Link**: Contains pagination URLs with `rel="next"` for additional results

**400 - Bad Request**
Invalid request parameters.

**401 - Unauthorized**
Authentication credentials are incorrect or missing.

#### Implementation Notes
- Uses cursor-based pagination (not offset-based)
- Default status filter includes `current` and `archived` but excludes `trashed`
- Results are limited to attachments the user has permission to view
- Sort order affects pagination cursor behavior

---

### Get Attachment by ID

**GET** `/attachments/{id}`

Returns detailed information about a specific attachment.

**Permissions required**: Permission to view the attachment's container.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `read:attachment:confluence`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Attachment ID (pattern: `(att)?[0-9]+`) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `version` | integer | Retrieve specific version number |
| `include-labels` | boolean | Include associated labels (default: false) |
| `include-properties` | boolean | Include content properties (default: false) |
| `include-operations` | boolean | Include available operations (default: false) |
| `include-versions` | boolean | Include version history (default: false) |
| `include-version` | boolean | Include current version info (default: true) |
| `include-collaborators` | boolean | Include collaborators (default: false) |

#### Response

**200 - Success**
```json
{
  "id": "att123456",
  "status": "current",
  "title": "document.pdf",
  "createdAt": "2023-01-01T12:00:00.000Z",
  "fileId": "file123456",
  "fileSize": 1024000,
  "mediaType": "application/pdf",
  "mediaTypeDescription": "PDF Document",
  "comment": "Important document",
  "parentId": "123456",
  "parentType": "page",
  "position": 0,
  "authorId": "user123",
  "version": {
    "number": 2,
    "message": "Updated version",
    "createdAt": "2023-01-02T12:00:00.000Z",
    "authorId": "user456",
    "minorEdit": false
  },
  "labels": {
    "results": [
      {
        "id": "label123",
        "name": "important",
        "prefix": "global"
      }
    ],
    "meta": {
      "hasMore": false,
      "cursor": "label_cursor"
    },
    "_links": {
      "next": "/wiki/api/v2/attachments/att123456/labels?cursor=label_cursor"
    }
  },
  "properties": {
    "results": [
      {
        "id": "prop123",
        "key": "custom-property",
        "value": "property-value"
      }
    ],
    "meta": {
      "hasMore": false
    }
  },
  "operations": [
    {
      "operation": "read",
      "targetType": "attachment"
    },
    {
      "operation": "delete",
      "targetType": "attachment"
    }
  ],
  "versions": {
    "results": [
      {
        "number": 1,
        "message": "Initial upload",
        "createdAt": "2023-01-01T12:00:00.000Z",
        "authorId": "user123"
      },
      {
        "number": 2,
        "message": "Updated version",
        "createdAt": "2023-01-02T12:00:00.000Z",
        "authorId": "user456"
      }
    ],
    "meta": {
      "hasMore": false
    }
  },
  "_links": {
    "base": "https://your-domain.atlassian.net/wiki",
    "download": "/wiki/download/attachments/123456/document.pdf",
    "webui": "/pages/viewpage.action?pageId=123456"
  }
}
```

**400 - Bad Request**
Invalid request parameters.

**401 - Unauthorized**
Authentication credentials are incorrect or missing.

**404 - Not Found**
Attachment does not exist or user lacks permission to view it.

#### Implementation Notes
- Attachment IDs can be prefixed with "att" or just be numeric
- Version parameter allows retrieval of historical versions
- Include parameters control response size and detail level
- Labels, properties, and versions have their own pagination

---

### Delete Attachment

**DELETE** `/attachments/{id}`

Deletes an attachment by moving it to trash or permanently purging it.

**Permissions required**: 
- Permission to view the container of the attachment
- Permission to delete attachments in the space
- Permission to administer the space (if attempting to purge)

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `delete:attachment:confluence`

**Connect app scope required**: DELETE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Attachment ID to delete |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `purge` | boolean | Permanently delete (purge) the attachment (default: false) |

#### Response

**204 - No Content**
Attachment was successfully deleted.

**400 - Bad Request**
Invalid request parameters.

**401 - Unauthorized**
Authentication credentials are incorrect or missing.

**404 - Not Found**
- Attachment does not exist
- User lacks permission to view the container
- User lacks permission to delete attachments in the space

#### Implementation Notes
- Default behavior moves attachment to trash (recoverable)
- `purge=true` permanently deletes the attachment (non-recoverable)
- Purging requires space administrator permissions
- Purge can only be performed on already trashed attachments

---

### Get Page Attachments

**GET** `/pages/{id}/attachments`

Returns all attachments for a specific page with filtering and pagination.

**Permissions required**: Permission to view the content of the page and its corresponding space.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `read:attachment:confluence`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Page ID to get attachments for |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sort` | string | Sort order: `created-date`, `modified-date`, `title` |
| `cursor` | string | Pagination cursor for next page |
| `status` | array | Filter by status: `current`, `archived`, `trashed` |
| `mediaType` | string | Filter by media type |
| `filename` | string | Filter by filename |
| `limit` | integer | Maximum results per page (default: 50, max: 250) |

#### Response

**200 - Success**
Same structure as Get All Attachments, but filtered to the specific page.

**Headers**
- **Link**: Contains pagination URLs for page-specific attachment results

**400 - Bad Request**
Invalid request parameters.

**401 - Unauthorized**
Authentication credentials are incorrect or missing.

**404 - Not Found**
Page does not exist or user lacks permission to view it.

## Additional Attachment Endpoints

### Get Attachment Versions

**GET** `/attachments/{id}/versions`

Returns version history for a specific attachment.

**OAuth 2.0 Scopes**: `read:attachment:confluence`

#### Response
```json
{
  "results": [
    {
      "number": 1,
      "message": "Initial upload",
      "createdAt": "2023-01-01T12:00:00.000Z",
      "authorId": "user123",
      "minorEdit": false,
      "fileSize": 1024000
    },
    {
      "number": 2,
      "message": "Updated document",
      "createdAt": "2023-01-02T12:00:00.000Z",
      "authorId": "user456",
      "minorEdit": false,
      "fileSize": 1048576
    }
  ],
  "_links": {
    "base": "https://your-domain.atlassian.net/wiki"
  }
}
```

---

### Get Attachment Version

**GET** `/attachments/{attachment-id}/versions/{version-number}`

Returns details of a specific attachment version.

**OAuth 2.0 Scopes**: `read:attachment:confluence`

---

### Get Attachment Labels

**GET** `/attachments/{id}/labels`

Returns labels associated with an attachment.

**OAuth 2.0 Scopes**: `read:attachment:confluence`

---

### Get Attachment Properties

**GET** `/attachments/{attachment-id}/properties`

Returns custom properties associated with an attachment.

**OAuth 2.0 Scopes**: `read:attachment:confluence`

---

### Get Attachment Property

**GET** `/attachments/{attachment-id}/properties/{property-id}`

Returns a specific custom property value.

**OAuth 2.0 Scopes**: `read:attachment:confluence`

---

### Get Attachment Operations

**GET** `/attachments/{id}/operations`

Returns available operations for an attachment based on user permissions.

**OAuth 2.0 Scopes**: `read:attachment:confluence`

#### Response
```json
[
  {
    "operation": "read",
    "targetType": "attachment"
  },
  {
    "operation": "delete",
    "targetType": "attachment"
  },
  {
    "operation": "update",
    "targetType": "attachment"
  }
]
```

## Content Type Support

### Supported Media Types
- **Documents**: `application/pdf`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- **Spreadsheets**: `application/vnd.ms-excel`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Presentations**: `application/vnd.ms-powerpoint`, `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- **Images**: `image/jpeg`, `image/png`, `image/gif`, `image/svg+xml`
- **Archives**: `application/zip`, `application/x-rar-compressed`
- **Text**: `text/plain`, `text/csv`

### File Size Limits
- Maximum file size varies by Confluence instance configuration
- Typical limits range from 10MB to 100MB per attachment
- Check instance settings for specific limits

## Error Handling

### Common Error Responses

**400 - Bad Request**
```json
{
  "statusCode": 400,
  "message": "Invalid request parameters",
  "reason": "INVALID_PARAMETER"
}
```

**401 - Unauthorized**
```json
{
  "statusCode": 401,
  "message": "Authentication required",
  "reason": "AUTHENTICATION_FAILED"
}
```

**403 - Forbidden**
```json
{
  "statusCode": 403,
  "message": "Insufficient permissions",
  "reason": "INSUFFICIENT_PERMISSIONS"
}
```

**404 - Not Found**
```json
{
  "statusCode": 404,
  "message": "Attachment not found",
  "reason": "ATTACHMENT_NOT_FOUND"
}
```

## Pagination

### Cursor-Based Pagination
The Attachment API uses cursor-based pagination:

1. **Initial Request**: Make request without cursor parameter
2. **Check Link Header**: Look for `Link` header with `rel="next"`
3. **Follow Next URL**: Use the relative URL from the Link header
4. **Continue**: Repeat until no more `next` link is provided

#### Example Link Header
```
Link: </wiki/api/v2/attachments?cursor=eyJjcmVhdGVkQXQiOiIyMDIzLTA...>; rel="next", <https://your-domain.atlassian.net/wiki>; rel="base"
```

## Best Practices

### Performance
- Use appropriate `limit` values to balance performance and data needs
- Include only necessary data with `include-*` parameters
- Cache attachment metadata when possible
- Use specific filtering to reduce result sets

### Security
- Always verify user permissions before displaying attachment information
- Respect attachment visibility and space permissions
- Validate attachment IDs before making API calls
- Handle authentication errors gracefully

### Content Management
- Check file size limits before upload operations
- Validate media types for security
- Use meaningful version messages for tracking changes
- Consider attachment lifecycle (current → archived → trashed → purged)

### Error Handling
- Handle 404 errors for missing or inaccessible attachments
- Implement retry logic for transient failures
- Provide user-friendly error messages
- Log errors for debugging and monitoring

## Integration Patterns

### Attachment Discovery
1. **List All Attachments**: Use global endpoint with filtering
2. **Page-Specific Attachments**: Use page endpoint for context
3. **Search by Properties**: Filter by media type, filename, or status
4. **Version Management**: Track attachment versions and changes

### Content Operations
1. **Read Attachment Metadata**: Get attachment details and properties
2. **Download Content**: Use download links from response
3. **Version History**: Track changes and author information
4. **Label Management**: Organize attachments with labels

### Lifecycle Management
1. **Active Attachments**: Work with `current` status attachments
2. **Archive Management**: Handle `archived` attachments
3. **Trash Operations**: Manage `trashed` attachments
4. **Purge Operations**: Permanently delete when necessary
