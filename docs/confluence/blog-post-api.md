# Confluence Blog Post API

## Overview
The Blog Post API provides operations for managing blog posts in Confluence spaces. Blog posts are time-based content that can be used for announcements, updates, and other chronological content.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:page:confluence` - Read blog post content
  - `write:page:confluence` - Create and update blog posts

## Endpoints

### Get Blog Posts
Retrieve blog posts with filtering and pagination support.

**Endpoint:** `GET /wiki/api/v2/blogposts`

**Parameters:**
- `id` (array[integer], optional) - Filter by blog post IDs (max 250)
- `space-id` (array[integer], optional) - Filter by space IDs (max 100)  
- `sort` (BlogPostSortOrder, optional) - Sort order for results
- `status` (array[string], optional) - Filter by status: `current`, `deleted`, `trashed` (default: `current`)
- `title` (string, optional) - Filter by blog post title
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Response:** Returns paginated list of blog posts with metadata and content.

**Permissions Required:**
- Permission to access Confluence site ('Can use' global permission)
- Only returns blog posts the user has permission to view

**Example Request:**
```http
GET /wiki/api/v2/blogposts?space-id=123456&limit=10&sort=created-date
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "results": [
    {
      "id": "789012",
      "status": "current",
      "title": "Weekly Update - January 2024",
      "spaceId": "123456",
      "authorId": "user123",
      "createdAt": "2024-01-15T10:00:00.000Z",
      "version": {
        "number": 1,
        "authorId": "user123",
        "createdAt": "2024-01-15T10:00:00.000Z"
      },
      "body": {
        "storage": {
          "value": "<p>This week's updates...</p>",
          "representation": "storage"
        }
      },
      "_links": {
        "webui": "/spaces/SPACE/blog/2024/01/15/789012"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/blogposts?cursor=next_page_token"
  }
}
```

## Use Cases

### Content Management
- **Blog Publishing:** Create and manage time-based content
- **Announcements:** Publish company or team updates
- **Documentation:** Time-stamped documentation updates
- **News Feed:** Maintain chronological content streams

### Integration Scenarios
- **Content Aggregation:** Collect blog posts across multiple spaces
- **Automated Publishing:** Create blog posts from external systems
- **Content Migration:** Transfer blog content between instances
- **Analytics:** Track blog post engagement and readership

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Error Handling
- **400 Bad Request:** Invalid parameters or malformed request
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for requested blog posts
- **404 Not Found:** Specified space or blog post not found
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- Use appropriate `limit` values to balance performance and data needs
- Filter by `space-id` when working with specific spaces
- Use `status=current` filter to exclude deleted/trashed content
- Implement proper pagination handling for large result sets
- Cache blog post content when appropriate to reduce API calls
