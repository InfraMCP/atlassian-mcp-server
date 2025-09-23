# Confluence Version API

## Overview
The Version API provides read-only access to version history for various content types in Confluence. This API allows you to retrieve version information, track changes over time, and access historical content states for pages, blog posts, attachments, comments, and custom content.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:page:confluence` - Read page and blog post versions
  - `read:comment:confluence` - Read comment versions
  - `read:attachment:confluence` - Read attachment versions
  - `read:custom-content:confluence` - Read custom content versions

## Supported Content Types
The Version API supports version history for:
- **Pages** - `/pages/{id}/versions`
- **Blog Posts** - `/blogposts/{id}/versions`
- **Attachments** - `/attachments/{id}/versions`
- **Footer Comments** - `/footer-comments/{id}/versions`
- **Inline Comments** - `/inline-comments/{id}/versions`
- **Custom Content** - `/custom-content/{custom-content-id}/versions`

## Core Endpoints

### Get Content Versions
Retrieve version history for specific content.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{id}/versions`

**Parameters:**
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)
- `sort` (VersionSortOrder, optional) - Sort order for results

**Examples:**
- `GET /wiki/api/v2/pages/{id}/versions`
- `GET /wiki/api/v2/blogposts/{id}/versions`
- `GET /wiki/api/v2/footer-comments/{id}/versions`

**Response:** List of versions with metadata and optional content

### Get Specific Version Details
Retrieve detailed information for a specific version.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{content-id}/versions/{version-number}`

**Parameters:**
- `{content-id}` (integer, required) - Content ID
- `version-number` (integer, required) - Version number

**Examples:**
- `GET /wiki/api/v2/pages/{page-id}/versions/{version-number}`
- `GET /wiki/api/v2/blogposts/{blogpost-id}/versions/{version-number}`
- `GET /wiki/api/v2/attachments/{attachment-id}/versions/{version-number}`

**Response:** Detailed version information with full content and metadata

## Example Usage

### Get Page Version History
```http
GET /wiki/api/v2/pages/123456789/versions?limit=50&sort=version-number-desc
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "results": [
    {
      "number": 3,
      "authorId": "user123",
      "message": "Updated API examples and fixed typos",
      "createdAt": "2024-01-20T14:30:00.000Z",
      "minorEdit": false,
      "_links": {
        "self": "/wiki/api/v2/pages/123456789/versions/3"
      }
    },
    {
      "number": 2,
      "authorId": "user456",
      "message": "Added new section on authentication",
      "createdAt": "2024-01-18T10:15:00.000Z",
      "minorEdit": false,
      "_links": {
        "self": "/wiki/api/v2/pages/123456789/versions/2"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/pages/123456789/versions?cursor=next_page_token"
  }
}
```

### Get Specific Version Details
```http
GET /wiki/api/v2/pages/123456789/versions/2
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "number": 2,
  "authorId": "user456",
  "message": "Added new section on authentication",
  "createdAt": "2024-01-18T10:15:00.000Z",
  "minorEdit": false,
  "contentId": "123456789",
  "collaborators": [
    {
      "accountId": "user456",
      "displayName": "Jane Smith"
    }
  ],
  "_links": {
    "self": "/wiki/api/v2/pages/123456789/versions/2",
    "content": "/wiki/api/v2/pages/123456789"
  }
}
```

### Get Comment Version History
```http
GET /wiki/api/v2/footer-comments/987654321/versions?limit=10
Authorization: Bearer {access_token}
```

### Get Attachment Versions
```http
GET /wiki/api/v2/attachments/555666777/versions?sort=created-at-desc
Authorization: Bearer {access_token}
```

## Use Cases

### Content Auditing
- **Change Tracking:** Monitor who made changes and when
- **Compliance:** Maintain audit trails for regulatory requirements
- **Content History:** Understand content evolution over time
- **Author Analysis:** Track contributor patterns and activity

### Version Management
- **Rollback Planning:** Identify versions for potential rollback
- **Change Analysis:** Compare versions to understand modifications
- **Content Recovery:** Access previous versions for content recovery
- **Version Comparison:** Analyze differences between versions

### Collaboration Insights
- **Contributor Tracking:** Identify active contributors and editors
- **Edit Patterns:** Analyze editing frequency and patterns
- **Collaboration Analysis:** Understand team collaboration dynamics
- **Content Ownership:** Track content ownership and responsibility

### Integration Scenarios
- **Backup Systems:** Create versioned backups of content
- **Change Notifications:** Alert on content changes and updates
- **Workflow Integration:** Integrate version data into approval workflows
- **Analytics:** Analyze content change patterns and trends

## Version Properties

### Version Metadata
- **Number:** Sequential version number (starts at 1)
- **Author ID:** Account ID of the user who created the version
- **Message:** Optional comment describing the changes
- **Created At:** Timestamp when the version was created
- **Minor Edit:** Boolean indicating if this was a minor edit
- **Content ID:** ID of the content this version belongs to

### Detailed Version Information
- **Collaborators:** Users who contributed to this version
- **Content:** Full content of the version (when requested)
- **Links:** Navigation links to related resources

### Version Types
- **Major Edit:** Significant changes that increment the version number
- **Minor Edit:** Small changes (typos, formatting) marked as minor
- **System Updates:** Automatic updates from system operations

## Sorting Options
- **Version Number:** Sort by version number (ascending/descending)
- **Created At:** Sort by creation timestamp (ascending/descending)
- **Author:** Sort by author information

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Versions:** Same permissions as viewing the parent content
- **Content-Specific:** Permissions vary by content type
- **Version Access:** All versions inherit permissions from current content

## Error Handling
- **400 Bad Request:** Invalid parameters or malformed request
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions to view content or versions
- **404 Not Found:** Content, version, or version number not found
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Pagination:** Handle large version histories with proper pagination
- **Filter Appropriately:** Use sorting and limits to get relevant versions
- **Cache Version Data:** Cache frequently accessed version information
- **Respect Permissions:** Only access versions for content user can view
- **Monitor Changes:** Track version creation for change notifications
- **Efficient Queries:** Request only necessary version information
- **Handle Missing Versions:** Account for deleted or inaccessible versions

## Integration Patterns

### Version History Dashboard
```javascript
// Get recent versions for a page
const versions = await getPageVersions(pageId, {
  limit: 10,
  sort: 'created-at-desc'
});

// Display version history
versions.forEach(version => {
  console.log(`Version ${version.number} by ${version.authorId} at ${version.createdAt}`);
  console.log(`Message: ${version.message || 'No message'}`);
});
```

### Change Tracking
```javascript
// Get all versions since a specific date
const since = new Date('2024-01-01').getTime();
const recentVersions = await getPageVersions(pageId, {
  limit: 250
});

const changesAfterDate = recentVersions.filter(v => 
  new Date(v.createdAt).getTime() > since
);

// Analyze change frequency
const changeFrequency = changesAfterDate.length;
const uniqueAuthors = [...new Set(changesAfterDate.map(v => v.authorId))];
```

### Content Recovery
```javascript
// Get specific version for recovery
const targetVersion = await getPageVersionDetails(pageId, versionNumber);

// Use version data for recovery process
if (targetVersion) {
  console.log(`Recovering to version ${targetVersion.number}`);
  console.log(`Created by: ${targetVersion.authorId}`);
  console.log(`Message: ${targetVersion.message}`);
}
```

### Audit Trail
```javascript
// Generate audit report for content
const allVersions = await getAllPageVersions(pageId);

const auditReport = {
  contentId: pageId,
  totalVersions: allVersions.length,
  firstVersion: allVersions[0],
  latestVersion: allVersions[allVersions.length - 1],
  contributors: [...new Set(allVersions.map(v => v.authorId))],
  majorEdits: allVersions.filter(v => !v.minorEdit).length,
  minorEdits: allVersions.filter(v => v.minorEdit).length
};
```

## Important Notes
- **Read-Only API:** Version API is read-only; cannot create, update, or delete versions
- **Version Numbers:** Sequential integers starting from 1
- **Content Dependency:** Versions are tied to their parent content's permissions
- **Historical Data:** Provides access to historical states of content
- **No Version Restoration:** API does not support restoring to previous versions
