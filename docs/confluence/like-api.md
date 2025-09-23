# Confluence Like API

## Overview
The Like API provides read-only operations for retrieving like counts and user information for content in Confluence. This API allows you to access engagement metrics and understand which users have liked specific content items.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:page:confluence` - Read page likes
  - `read:comment:confluence` - Read comment likes

## Supported Content Types
The Like API supports the following content types:
- **Pages** - `/pages/{id}/likes/`
- **Blog Posts** - `/blogposts/{id}/likes/`
- **Footer Comments** - `/footer-comments/{id}/likes/`
- **Inline Comments** - `/inline-comments/{id}/likes/`

## Core Endpoints

### Get Like Count
Retrieve the total number of likes for specific content.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{id}/likes/count`

**Examples:**
- `GET /wiki/api/v2/pages/{id}/likes/count`
- `GET /wiki/api/v2/blogposts/{id}/likes/count`
- `GET /wiki/api/v2/footer-comments/{id}/likes/count`
- `GET /wiki/api/v2/inline-comments/{id}/likes/count`

**Response:**
```json
{
  "count": 42
}
```

### Get Like Users
Retrieve account IDs of users who liked specific content.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{id}/likes/users`

**Parameters:**
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (0-250, default: 25)

**Examples:**
- `GET /wiki/api/v2/pages/{id}/likes/users`
- `GET /wiki/api/v2/blogposts/{id}/likes/users`
- `GET /wiki/api/v2/footer-comments/{id}/likes/users`
- `GET /wiki/api/v2/inline-comments/{id}/likes/users`

**Response:**
```json
{
  "results": [
    {
      "accountId": "user123",
      "likedAt": "2024-01-15T10:00:00.000Z"
    },
    {
      "accountId": "user456", 
      "likedAt": "2024-01-15T11:30:00.000Z"
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/pages/123/likes/users?cursor=next_page_token"
  }
}
```

## Example Usage

### Get Page Like Count
```http
GET /wiki/api/v2/pages/123456789/likes/count
Authorization: Bearer {access_token}
```

### Get Page Like Users with Pagination
```http
GET /wiki/api/v2/pages/123456789/likes/users?limit=50
Authorization: Bearer {access_token}
```

### Get Comment Like Information
```http
GET /wiki/api/v2/footer-comments/987654321/likes/count
Authorization: Bearer {access_token}
```

```http
GET /wiki/api/v2/footer-comments/987654321/likes/users?limit=25
Authorization: Bearer {access_token}
```

### Get Blog Post Engagement
```http
GET /wiki/api/v2/blogposts/555666777/likes/count
Authorization: Bearer {access_token}
```

## Use Cases

### Engagement Analytics
- **Content Performance:** Measure content engagement and popularity
- **User Engagement:** Track which users are most active in liking content
- **Trending Content:** Identify highly-liked content for promotion
- **Engagement Metrics:** Generate reports on content interaction levels

### Social Features
- **Like Displays:** Show like counts and user lists in custom interfaces
- **User Activity:** Track user engagement patterns across content
- **Social Proof:** Display engagement metrics to encourage interaction
- **Recognition:** Identify popular contributors and content creators

### Content Optimization
- **Content Analysis:** Understand what content resonates with users
- **Feedback Loops:** Use like data to improve content strategy
- **A/B Testing:** Compare engagement across different content approaches
- **Quality Metrics:** Use likes as one indicator of content quality

### Integration Scenarios
- **Dashboard Creation:** Build engagement dashboards and reports
- **Notification Systems:** Alert on high engagement or milestone likes
- **Gamification:** Create engagement-based rewards or recognition systems
- **Content Curation:** Automatically promote highly-liked content

## Data Structure

### Like Count Response
```json
{
  "count": 15
}
```

### Like Users Response
```json
{
  "results": [
    {
      "accountId": "5d5f9fbf-2d5b-4b5a-8b1a-1234567890ab",
      "likedAt": "2024-01-15T10:00:00.000Z"
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/pages/123/likes/users?cursor=abc123"
  }
}
```

## Pagination
Uses cursor-based pagination for user lists:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request
- Minimum 0 results per request (useful for count-only queries)

## Permissions
- **View Content:** Permission to view the content and its space required
- **Like Information:** Same permissions as viewing the content
- **User Privacy:** Only returns account IDs, not detailed user information

## Error Handling
- **400 Bad Request:** Invalid parameters or malformed request
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions to view content
- **404 Not Found:** Content not found or no permission to view
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Cache Like Counts:** Cache frequently accessed like counts to reduce API calls
- **Batch Requests:** Combine like data retrieval with content fetching when possible
- **Handle Permissions:** Only request like data for content user can access
- **Respect Privacy:** Use account IDs appropriately and respect user privacy
- **Monitor Trends:** Track like patterns over time for content insights
- **Pagination Handling:** Implement proper pagination for content with many likes
- **Performance Optimization:** Consider like count vs. user list based on use case needs
