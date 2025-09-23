# Confluence Operation API

## Overview
The Operation API provides read-only access to permitted operations for various content types in Confluence. This API allows you to determine what actions the current user can perform on specific content items, enabling dynamic UI behavior and permission-aware integrations.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:page:confluence` - Read page operations
  - `read:space:confluence` - Read space operations
  - `read:comment:confluence` - Read comment operations
  - `read:custom-content:confluence` - Read custom content operations

## Supported Content Types
The Operation API supports the following content types:
- **Pages** - `/pages/{id}/operations`
- **Blog Posts** - `/blogposts/{id}/operations`
- **Spaces** - `/spaces/{id}/operations`
- **Attachments** - `/attachments/{id}/operations`
- **Custom Content** - `/custom-content/{id}/operations`
- **Footer Comments** - `/footer-comments/{id}/operations`
- **Inline Comments** - `/inline-comments/{id}/operations`
- **Whiteboards** - `/whiteboards/{id}/operations`
- **Databases** - `/databases/{id}/operations`
- **Embeds** - `/embeds/{id}/operations`
- **Folders** - `/folders/{id}/operations`

## Core Endpoint

### Get Permitted Operations
Retrieve the list of operations the current user can perform on specific content.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{id}/operations`

**Examples:**
- `GET /wiki/api/v2/pages/{id}/operations`
- `GET /wiki/api/v2/spaces/{id}/operations`
- `GET /wiki/api/v2/blogposts/{id}/operations`
- `GET /wiki/api/v2/footer-comments/{id}/operations`

**Response:** PermittedOperationsResponse with list of allowed operations

## Common Operations

### Content Operations
- **`read`** - View content
- **`update`** - Edit content
- **`delete`** - Delete content
- **`create`** - Create new content (context-dependent)
- **`move`** - Move content to different location
- **`copy`** - Copy content
- **`export`** - Export content

### Permission Operations
- **`administer`** - Full administrative access
- **`restrict_update`** - Manage update restrictions
- **`restrict_read`** - Manage read restrictions

### Social Operations
- **`like`** - Like/unlike content
- **`comment`** - Add comments to content
- **`watch`** - Watch content for changes

### Advanced Operations
- **`restore`** - Restore from trash
- **`purge`** - Permanently delete
- **`use_as_template`** - Use content as template

## Example Usage

### Get Page Operations
```http
GET /wiki/api/v2/pages/123456789/operations
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "operations": [
    {
      "operation": "read",
      "targetType": "page"
    },
    {
      "operation": "update", 
      "targetType": "page"
    },
    {
      "operation": "delete",
      "targetType": "page"
    },
    {
      "operation": "comment",
      "targetType": "page"
    },
    {
      "operation": "like",
      "targetType": "page"
    }
  ]
}
```

### Get Space Operations
```http
GET /wiki/api/v2/spaces/987654321/operations
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "operations": [
    {
      "operation": "read",
      "targetType": "space"
    },
    {
      "operation": "create",
      "targetType": "page"
    },
    {
      "operation": "create",
      "targetType": "blogpost"
    },
    {
      "operation": "administer",
      "targetType": "space"
    }
  ]
}
```

### Get Comment Operations
```http
GET /wiki/api/v2/footer-comments/555666777/operations
Authorization: Bearer {access_token}
```

## Use Cases

### Dynamic UI Behavior
- **Conditional Buttons:** Show/hide edit, delete, and action buttons based on permissions
- **Menu Options:** Display only available actions in context menus
- **Feature Availability:** Enable/disable features based on user permissions
- **Workflow Controls:** Show appropriate workflow actions for current user

### Permission-Aware Integrations
- **API Safety:** Check permissions before attempting operations
- **Error Prevention:** Avoid API calls that will fail due to permissions
- **User Experience:** Provide clear feedback about available actions
- **Security Compliance:** Respect Confluence permission model

### Administrative Tools
- **Permission Auditing:** Understand user capabilities across content
- **Access Management:** Review and analyze permission distributions
- **Compliance Reporting:** Generate reports on user access levels
- **Troubleshooting:** Diagnose permission-related issues

### Application Logic
- **Conditional Processing:** Execute different logic based on available operations
- **Feature Gating:** Enable advanced features only for users with appropriate permissions
- **Workflow Management:** Route content through appropriate approval processes
- **Integration Security:** Ensure integrations respect permission boundaries

## Data Structure

### Permitted Operations Response
```json
{
  "operations": [
    {
      "operation": "read",
      "targetType": "page",
      "description": "View page content"
    },
    {
      "operation": "update",
      "targetType": "page", 
      "description": "Edit page content"
    },
    {
      "operation": "delete",
      "targetType": "page",
      "description": "Delete page"
    }
  ]
}
```

### Operation Object
- **`operation`** - The operation name (e.g., "read", "update", "delete")
- **`targetType`** - The content type the operation applies to
- **`description`** - Human-readable description of the operation (optional)

## Permissions
- **View Content:** Permission to view the content and its space required
- **Operation Visibility:** Only returns operations the user can actually perform
- **Context-Aware:** Operations reflect current user's permissions and content state

## Error Handling
- **400 Bad Request:** Invalid content ID or malformed request
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions to view content
- **404 Not Found:** Content not found or no permission to view
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Check Before Acting:** Always check operations before attempting API calls
- **Cache Appropriately:** Cache operation results for frequently accessed content
- **Handle Permissions Gracefully:** Provide clear feedback when operations aren't available
- **Respect Boundaries:** Never attempt operations not listed in the response
- **Update Dynamically:** Refresh operations when content or permissions change
- **User Feedback:** Use operation information to provide helpful user guidance
- **Security First:** Treat operation results as authoritative for permission decisions

## Integration Patterns

### UI Component Pattern
```javascript
// Check if user can edit before showing edit button
const operations = await getPageOperations(pageId);
const canEdit = operations.some(op => op.operation === 'update');
if (canEdit) {
  showEditButton();
}
```

### API Safety Pattern
```javascript
// Verify permission before API call
const operations = await getPageOperations(pageId);
const canDelete = operations.some(op => op.operation === 'delete');
if (canDelete) {
  await deletePage(pageId);
} else {
  showPermissionError();
}
```

### Feature Gating Pattern
```javascript
// Enable advanced features based on permissions
const operations = await getSpaceOperations(spaceId);
const isAdmin = operations.some(op => op.operation === 'administer');
if (isAdmin) {
  enableAdvancedFeatures();
}
```
