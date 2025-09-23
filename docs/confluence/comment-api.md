# Confluence Comment API

## Overview
The Comment API provides comprehensive operations for managing comments in Confluence. It supports both footer comments (attached to pages/blog posts) and inline comments (attached to specific content within pages), with full CRUD operations, versioning, and social features like likes.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:comment:confluence` - Read comments and their metadata
  - `write:comment:confluence` - Create and update comments
  - `delete:comment:confluence` - Delete comments

## Comment Types

### Footer Comments
Comments attached to the bottom of pages, blog posts, attachments, or custom content. These are the traditional "page comments" visible in the Confluence UI.

### Inline Comments
Comments attached to specific content within pages, allowing for contextual discussions about particular sections or elements.

## Core Endpoints

### Get All Footer Comments
Retrieve all footer comments with filtering and pagination.

**Endpoint:** `GET /wiki/api/v2/footer-comments`

**Parameters:**
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field
- `sort` (CommentSortOrder, optional) - Sort order for results
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

### Create Footer Comment
Create a new footer comment on pages, blog posts, attachments, or as replies.

**Endpoint:** `POST /wiki/api/v2/footer-comments`

**Request Body:** CreateFooterCommentModel
- Can target: pages (pageId), blog posts (blogPostId), attachments, custom content
- Can be replies (parentCommentId)
- Requires comment body content

**Response:** 201 Created with comment details and location header

### Get Footer Comment by ID
Retrieve a specific footer comment with optional metadata.

**Endpoint:** `GET /wiki/api/v2/footer-comments/{comment-id}`

**Parameters:**
- `comment-id` (integer, required) - Comment ID
- `body-format` (PrimaryBodyRepresentationSingle, optional) - Content format
- `version` (integer, optional) - Retrieve specific version
- `include-properties` (boolean, default: false) - Include content properties
- `include-operations` (boolean, default: false) - Include available operations
- `include-likes` (boolean, default: false) - Include like information
- `include-versions` (boolean, default: false) - Include version history
- `include-version` (boolean, default: true) - Include current version

### Update Footer Comment
Update an existing footer comment's content.

**Endpoint:** `PUT /wiki/api/v2/footer-comments/{comment-id}`

**Request Body:** UpdateFooterCommentModel
- Update comment body text
- Maintains version history

**Response:** 200 OK with updated comment details

### Delete Footer Comment
Permanently delete a footer comment.

**Endpoint:** `DELETE /wiki/api/v2/footer-comments/{comment-id}`

**Response:** 204 No Content (permanent deletion, cannot be reverted)

## Content-Specific Comment Endpoints

### Get Comments for Specific Content
Retrieve comments attached to specific content types:

- `GET /wiki/api/v2/pages/{id}/footer-comments` - Page footer comments
- `GET /wiki/api/v2/pages/{id}/inline-comments` - Page inline comments
- `GET /wiki/api/v2/blogposts/{id}/footer-comments` - Blog post footer comments
- `GET /wiki/api/v2/blogposts/{id}/inline-comments` - Blog post inline comments
- `GET /wiki/api/v2/attachments/{id}/footer-comments` - Attachment comments
- `GET /wiki/api/v2/custom-content/{id}/footer-comments` - Custom content comments

## Inline Comments
Similar operations available for inline comments:

- `GET /wiki/api/v2/inline-comments` - Get all inline comments
- `POST /wiki/api/v2/inline-comments` - Create inline comment
- `GET /wiki/api/v2/inline-comments/{comment-id}` - Get specific inline comment
- `PUT /wiki/api/v2/inline-comments/{comment-id}` - Update inline comment
- `DELETE /wiki/api/v2/inline-comments/{comment-id}` - Delete inline comment

## Social Features

### Comment Likes
- `GET /wiki/api/v2/footer-comments/{id}/likes/count` - Get like count
- `GET /wiki/api/v2/footer-comments/{id}/likes/users` - Get users who liked
- `GET /wiki/api/v2/inline-comments/{id}/likes/count` - Inline comment like count
- `GET /wiki/api/v2/inline-comments/{id}/likes/users` - Inline comment like users

### Comment Hierarchies
- `GET /wiki/api/v2/footer-comments/{id}/children` - Get comment replies
- `GET /wiki/api/v2/inline-comments/{id}/children` - Get inline comment replies

## Versioning & History

### Comment Versions
- `GET /wiki/api/v2/footer-comments/{id}/versions` - Get version history
- `GET /wiki/api/v2/footer-comments/{id}/versions/{version-number}` - Get specific version
- `GET /wiki/api/v2/inline-comments/{id}/versions` - Inline comment versions
- `GET /wiki/api/v2/inline-comments/{id}/versions/{version-number}` - Specific inline version

### Operations
- `GET /wiki/api/v2/footer-comments/{id}/operations` - Available operations
- `GET /wiki/api/v2/inline-comments/{id}/operations` - Inline comment operations

## Comment Properties
Manage custom properties attached to comments:

- `GET /wiki/api/v2/comments/{comment-id}/properties` - Get comment properties
- `POST /wiki/api/v2/comments/{comment-id}/properties` - Create property
- `GET /wiki/api/v2/comments/{comment-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/comments/{comment-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/comments/{comment-id}/properties/{property-id}` - Delete property

## Example Usage

### Create Page Comment
```http
POST /wiki/api/v2/footer-comments
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "pageId": "123456789",
  "body": {
    "representation": "storage",
    "value": "<p>Great article! This section on API integration is particularly helpful.</p>"
  }
}
```

### Reply to Comment
```http
POST /wiki/api/v2/footer-comments
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "parentCommentId": "987654321",
  "body": {
    "representation": "storage", 
    "value": "<p>Thanks for the feedback! I'll add more examples in the next update.</p>"
  }
}
```

### Get Page Comments
```http
GET /wiki/api/v2/pages/123456789/footer-comments?limit=50&include-likes=true
Authorization: Bearer {access_token}
```

## Use Cases

### Collaboration & Feedback
- **Document Review:** Add comments during content review processes
- **Feedback Collection:** Gather input on pages and blog posts
- **Discussion Threads:** Enable threaded conversations on content
- **Approval Workflows:** Use comments for approval and sign-off processes

### Integration Scenarios
- **Automated Notifications:** Create comments from external systems
- **Review Automation:** Generate comments from code reviews or CI/CD
- **Content Moderation:** Manage and moderate user-generated comments
- **Analytics Integration:** Track comment engagement and sentiment

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Comments:** Permission to view the content and its space
- **Create Comments:** Permission to create comments in the space
- **Update Comments:** Permission to create comments + ownership or admin rights
- **Delete Comments:** Permission to delete comments in space + ownership or admin rights

## Error Handling
- **400 Bad Request:** Invalid parameters or malformed request body
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for comment operations
- **404 Not Found:** Comment, page, or parent content not found
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- Use appropriate comment type (footer vs inline) based on context
- Include relevant metadata with `include-*` parameters when needed
- Implement proper pagination for large comment threads
- Handle comment hierarchies (replies) appropriately in UI
- Cache comment data when appropriate to reduce API calls
- Use content-specific endpoints when working with particular pages/posts
