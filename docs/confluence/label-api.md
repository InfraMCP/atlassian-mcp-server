# Confluence Label API

## Overview
The Label API provides read-only operations for retrieving labels and their associations with content in Confluence. Labels are tags that help categorize and organize content, making it easier to find and group related items across spaces.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:label:confluence` - Read labels
  - `read:page:confluence` - Read page labels (content-specific endpoints)

## Core Endpoints

### Get All Labels
Retrieve all labels with filtering and pagination.

**Endpoint:** `GET /wiki/api/v2/labels`

**Parameters:**
- `label-id` (array[integer], optional) - Filter by label IDs (comma-separated)
- `prefix` (array[string], optional) - Filter by label prefixes (comma-separated)
- `sort` (LabelSortOrder, optional) - Sort order for results
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Permissions:** Global 'Can use' permission. Only returns labels user can view.

## Content-Specific Label Endpoints

### Get Labels for Content Types
Retrieve labels attached to specific content:

- `GET /wiki/api/v2/pages/{id}/labels` - Get page labels
- `GET /wiki/api/v2/blogposts/{id}/labels` - Get blog post labels
- `GET /wiki/api/v2/attachments/{id}/labels` - Get attachment labels
- `GET /wiki/api/v2/custom-content/{id}/labels` - Get custom content labels

**Common Parameters:**
- `prefix` (string, optional) - Filter by prefix: `my`, `team`, `global`, `system`
- `sort` (LabelSortOrder, optional) - Sort order
- `cursor` (string, optional) - Pagination cursor
- `limit` (integer, optional) - Results per page (1-250, default: 25)

### Get Content by Label
Retrieve content that has specific labels:

- `GET /wiki/api/v2/labels/{id}/pages` - Get pages with label
- `GET /wiki/api/v2/labels/{id}/blogposts` - Get blog posts with label
- `GET /wiki/api/v2/labels/{id}/attachments` - Get attachments with label

### Get Space Labels
Retrieve labels within specific spaces:

- `GET /wiki/api/v2/spaces/{id}/labels` - Get space labels
- `GET /wiki/api/v2/spaces/{id}/content/labels` - Get all content labels in space

## Label Types and Prefixes

### Label Prefixes
- **`my:`** - Personal labels created by individual users
- **`team:`** - Team-specific labels for group organization
- **`global:`** - Site-wide labels available to all users
- **`system:`** - System-generated labels (automatic categorization)

### Label Categories
- **Content Labels:** User-created tags for content organization
- **System Labels:** Automatically generated based on content analysis
- **Personal Labels:** Individual user's organizational system
- **Team Labels:** Shared labels for team or department use

## Example Usage

### Get All Labels with Filtering
```http
GET /wiki/api/v2/labels?prefix=team,global&limit=50&sort=name
Authorization: Bearer {access_token}
```

### Get Page Labels
```http
GET /wiki/api/v2/pages/123456789/labels?prefix=global
Authorization: Bearer {access_token}
```

### Get Pages with Specific Label
```http
GET /wiki/api/v2/labels/987654321/pages?limit=25
Authorization: Bearer {access_token}
```

### Get Space Content Labels
```http
GET /wiki/api/v2/spaces/123456789/content/labels?sort=usage-count
Authorization: Bearer {access_token}
```

## Example Response
```json
{
  "results": [
    {
      "id": "123456",
      "name": "documentation",
      "prefix": "global",
      "displayName": "Documentation",
      "createdAt": "2024-01-15T10:00:00.000Z",
      "createdBy": {
        "accountId": "user123",
        "displayName": "John Doe"
      },
      "_links": {
        "self": "/wiki/api/v2/labels/123456"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/labels?cursor=next_page_token"
  }
}
```

## Use Cases

### Content Discovery
- **Topic Browsing:** Find content by subject or theme
- **Related Content:** Discover related pages and resources
- **Content Exploration:** Browse content by categories and tags
- **Search Enhancement:** Use labels to refine search results

### Content Organization
- **Categorization:** Understand how content is organized
- **Taxonomy Analysis:** Analyze content classification systems
- **Content Audit:** Review labeling consistency across spaces
- **Metadata Extraction:** Extract organizational metadata from labels

### Integration Scenarios
- **Content Migration:** Preserve labeling during content transfers
- **Analytics:** Analyze content usage patterns by labels
- **Automated Tagging:** Suggest labels based on existing patterns
- **Reporting:** Generate reports on content organization

### Team Collaboration
- **Project Tracking:** Find content related to specific projects
- **Department Organization:** Browse content by department or team
- **Process Documentation:** Locate process-related content
- **Knowledge Management:** Navigate organizational knowledge by topics

## Label Management Features
- **Hierarchical Organization:** Labels can represent hierarchical categories
- **Usage Tracking:** Monitor label usage across content
- **Permission-Based:** Only shows labels user has permission to view
- **Multi-Content Support:** Labels work across all content types
- **Search Integration:** Labels enhance content discoverability

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Labels:** Global 'Can use' permission required
- **Content Labels:** Permission to view the labeled content required
- **Space Labels:** Permission to view the space required
- **System Labels:** Generally visible to all users with basic permissions

## Error Handling
- **400 Bad Request:** Invalid parameters or malformed request
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions to view labels or content
- **404 Not Found:** Content or label not found
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Filter by Prefix:** Use prefix filtering to focus on relevant label types
- **Implement Pagination:** Handle large label sets with proper pagination
- **Cache Label Data:** Cache frequently accessed labels to reduce API calls
- **Respect Permissions:** Only access labels for content user can view
- **Use for Discovery:** Leverage labels for content discovery and navigation
- **Monitor Usage:** Track label usage patterns for content organization insights
