# Confluence Ancestors API (v2)

The Confluence Ancestors API v2 provides access to the hierarchical structure of content by retrieving ancestor information for pages, databases, embeds, folders, and whiteboards.

## OAuth 2.0 Scopes Required

### Granular Scopes (Current)
- **`read:content.metadata:confluence`** - Read content metadata including ancestor information

### Connect App Scopes
- **READ** - For reading ancestor information

## Core Ancestors Operations

### Get Page Ancestors

**GET** `/pages/{id}/ancestors`

Returns all ancestors for a given page by ID in top-to-bottom order (highest ancestor first). This provides the complete hierarchical path from the space root to the specified page.

**Permissions required**: Permission to access the Confluence site ('Can use' global permission).

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `read:content.metadata:confluence`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The ID of the page |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum ancestors per result (default: 25, max: 250) |

#### Response

**200 - Success**
```json
{
  "results": [
    {
      "id": "123456",
      "type": "page",
      "status": "current",
      "title": "Parent Page",
      "spaceId": "789012",
      "authorId": "user123",
      "createdAt": "2023-01-01T12:00:00.000Z",
      "_links": {
        "webui": "/spaces/SPACE/pages/123456/Parent+Page"
      }
    },
    {
      "id": "234567",
      "type": "page", 
      "status": "current",
      "title": "Grandparent Page",
      "spaceId": "789012",
      "authorId": "user456",
      "createdAt": "2022-12-01T12:00:00.000Z",
      "_links": {
        "webui": "/spaces/SPACE/pages/234567/Grandparent+Page"
      }
    }
  ],
  "_links": {
    "base": "https://your-domain.atlassian.net/wiki"
  }
}
```

**400 - Bad Request**
Invalid request parameters.

**401 - Unauthorized**
Authentication credentials are incorrect or missing.

**404 - Not Found**
Page does not exist or user lacks permission to view it.

#### Implementation Notes
- Results are ordered from immediate parent to highest ancestor
- Returns minimal information about each ancestor
- Use "Get page by id" endpoint for detailed ancestor information
- Pagination works by calling endpoint with highest ancestor's ID for next set
- Only returns ancestors the user has permission to view

---

### Get Database Ancestors

**GET** `/databases/{id}/ancestors`

Returns all ancestors for a given database by ID in hierarchical order.

**OAuth 2.0 Scopes**: `read:content.metadata:confluence`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The ID of the database |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum ancestors per result (default: 25, max: 250) |

---

### Get Embed Ancestors

**GET** `/embeds/{id}/ancestors`

Returns all ancestors for a given embed by ID in hierarchical order.

**OAuth 2.0 Scopes**: `read:content.metadata:confluence`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The ID of the embed |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum ancestors per result (default: 25, max: 250) |

---

### Get Folder Ancestors

**GET** `/folders/{id}/ancestors`

Returns all ancestors for a given folder by ID in hierarchical order.

**OAuth 2.0 Scopes**: `read:content.metadata:confluence`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The ID of the folder |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum ancestors per result (default: 25, max: 250) |

---

### Get Whiteboard Ancestors

**GET** `/whiteboards/{id}/ancestors`

Returns all ancestors for a given whiteboard by ID in hierarchical order.

**OAuth 2.0 Scopes**: `read:content.metadata:confluence`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | The ID of the whiteboard |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum ancestors per result (default: 25, max: 250) |

## Ancestor Object Structure

### Common Properties

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier of the ancestor |
| `type` | string | Content type: `page`, `database`, `embed`, `folder`, `whiteboard` |
| `status` | string | Content status: `current`, `archived`, `trashed` |
| `title` | string | Title of the ancestor content |
| `spaceId` | string | ID of the space containing the ancestor |
| `authorId` | string | ID of the content author |
| `createdAt` | string | Creation timestamp (ISO 8601) |
| `_links.webui` | string | Web UI link to view the ancestor |

## Hierarchical Structure

### Understanding Ancestor Order
```
Space Root
├── Grandparent Page (highest ancestor)
│   ├── Parent Page (immediate parent)
│   │   └── Current Page (target page)
│   └── Sibling Page
└── Other Top-Level Page
```

### API Response Order
The API returns ancestors in **top-to-bottom** order:
1. **First result**: Immediate parent
2. **Second result**: Grandparent
3. **Last result**: Highest ancestor (closest to space root)

## Pagination

### Ancestor Pagination
Unlike other APIs, ancestor pagination works differently:

1. **Initial Request**: Get first set of ancestors for target content
2. **Next Set**: Use the ID of the **first ancestor** (highest in hierarchy) from previous response
3. **Continue**: Repeat until no more ancestors exist

#### Example Pagination Flow
```
1. GET /pages/12345/ancestors?limit=2
   Returns: [Parent, Grandparent]

2. GET /pages/67890/ancestors?limit=2  (using Grandparent's ID)
   Returns: [Great-Grandparent, Great-Great-Grandparent]

3. Continue until empty results
```

## Use Cases

### Breadcrumb Navigation
```javascript
// Build breadcrumb trail for a page
const ancestors = await getPageAncestors(pageId);
const breadcrumbs = ancestors.results.reverse().map(ancestor => ({
  title: ancestor.title,
  url: ancestor._links.webui
}));
```

### Permission Inheritance
```javascript
// Check if user has access to page hierarchy
const ancestors = await getPageAncestors(pageId);
const accessiblePath = ancestors.results.filter(ancestor => 
  userHasPermission(ancestor.id)
);
```

### Content Organization
```javascript
// Analyze content depth and structure
const ancestors = await getPageAncestors(pageId);
const depth = ancestors.results.length;
const rootParent = ancestors.results[ancestors.results.length - 1];
```

### Site Navigation
```javascript
// Build hierarchical navigation menu
const buildNavigation = async (contentId) => {
  const ancestors = await getPageAncestors(contentId);
  return {
    current: contentId,
    path: ancestors.results.map(a => ({ id: a.id, title: a.title })),
    depth: ancestors.results.length
  };
};
```

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

**404 - Not Found**
```json
{
  "statusCode": 404,
  "message": "Page not found or access denied",
  "reason": "CONTENT_NOT_FOUND"
}
```

## Best Practices

### Performance
- Use appropriate `limit` values to balance performance and completeness
- Cache ancestor information for frequently accessed content
- Consider the depth of content hierarchy when setting limits
- Batch ancestor requests for multiple content items when possible

### Navigation
- Build breadcrumbs by reversing the ancestor order
- Handle cases where some ancestors may not be accessible
- Provide fallback navigation when ancestor chain is incomplete
- Consider space-level navigation as the ultimate fallback

### Permission Handling
- Check user permissions for each ancestor in the chain
- Handle cases where intermediate ancestors are not accessible
- Provide graceful degradation when parts of hierarchy are hidden
- Respect content visibility and space permissions

### Content Management
- Use ancestor information to understand content organization
- Track content depth for organizational policies
- Identify orphaned content with no ancestors
- Monitor content hierarchy for governance purposes

## Integration Patterns

### Breadcrumb Implementation
1. **Fetch Ancestors**: Get ancestor chain for current content
2. **Reverse Order**: Convert top-to-bottom to bottom-to-top
3. **Build Links**: Create navigation links with titles and URLs
4. **Handle Permissions**: Filter out inaccessible ancestors

### Content Discovery
1. **Start with Target**: Begin with specific content ID
2. **Walk Hierarchy**: Follow ancestor chain to understand context
3. **Identify Patterns**: Recognize organizational structures
4. **Build Relationships**: Map content relationships and dependencies

### Access Control
1. **Check Permissions**: Verify access to each ancestor
2. **Determine Scope**: Understand accessible content scope
3. **Filter Results**: Remove inaccessible ancestors from navigation
4. **Provide Context**: Show available hierarchy levels to user

## Limitations

### Content Types
- Only supports specific content types: pages, databases, embeds, folders, whiteboards
- Does not include space-level hierarchy information
- Blog posts may have different ancestor behavior

### Pagination
- Unique pagination model different from other APIs
- Requires understanding of hierarchical relationships
- May require multiple requests for deep hierarchies

### Permissions
- Ancestor visibility depends on user permissions
- Broken chains possible when intermediate ancestors are inaccessible
- No indication of hidden ancestors in the chain

### Data Completeness
- Returns minimal ancestor information
- Requires additional API calls for detailed ancestor data
- No bulk ancestor retrieval for multiple content items
