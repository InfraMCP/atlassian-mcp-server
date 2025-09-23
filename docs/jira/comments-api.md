# Jira Comments API (v3)

The Jira Comments API v3 provides comprehensive comment management capabilities including creation, retrieval, updates, deletion, and property management. This documentation covers the comment endpoints used in the Atlassian MCP Server.

## Base URL Structure

All Jira v3 API endpoints follow this pattern:
```
https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/{endpoint}
```

## OAuth 2.0 Scopes Required

### Granular Scopes (Recommended)
- **`read:jira-work`** - Read comments and comment properties
- **`write:jira-work`** - Create, update, and delete comments

### Classic Scopes (Legacy)
- **`read:jira-work`** - Read access to comments
- **`write:jira-work`** - Write access to comments

## Core Comment Operations

### Get Issue Comments

**GET** `/issue/{issueIdOrKey}/comment`

Retrieve all comments for a specific issue with pagination and sorting options.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `issueIdOrKey` | string | Issue ID or key (required) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 100) |
| `orderBy` | string | Sort order: `created`, `-created`, `+created` |
| `expand` | string | Additional data: `renderedBody` (HTML-rendered content) |

#### Request Example
```
GET /issue/WEB-123/comment?orderBy=created&maxResults=50&expand=renderedBody
```

#### Response Example
```json
{
  "startAt": 0,
  "maxResults": 50,
  "total": 3,
  "comments": [
    {
      "id": "10000",
      "author": {
        "accountId": "5b10a2844c20165700ede21g",
        "displayName": "John Smith",
        "active": true,
        "avatarUrls": {
          "48x48": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=48&s=48"
        }
      },
      "body": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "This issue needs immediate attention. The login flow is completely broken."
              }
            ]
          }
        ]
      },
      "updateAuthor": {
        "accountId": "5b10a2844c20165700ede21g",
        "displayName": "John Smith",
        "active": true
      },
      "created": "2024-01-15T10:30:00.000+0000",
      "updated": "2024-01-15T10:35:00.000+0000",
      "visibility": {
        "type": "role",
        "value": "Developers",
        "identifier": "developers"
      },
      "self": "https://your-domain.atlassian.net/rest/api/3/issue/WEB-123/comment/10000"
    }
  ]
}
```

### Get Single Comment

**GET** `/issue/{issueIdOrKey}/comment/{id}`

Retrieve a specific comment by its ID.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `issueIdOrKey` | string | Issue ID or key (required) |
| `id` | string | Comment ID (required) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | string | Additional data: `renderedBody` |

#### Request Example
```
GET /issue/WEB-123/comment/10000?expand=renderedBody
```

#### Response Example
```json
{
  "id": "10000",
  "author": {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "John Smith",
    "active": true
  },
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "This issue needs immediate attention."
          }
        ]
      }
    ]
  },
  "renderedBody": "<p>This issue needs immediate attention.</p>",
  "created": "2024-01-15T10:30:00.000+0000",
  "updated": "2024-01-15T10:35:00.000+0000"
}
```

### Add Comment

**POST** `/issue/{issueIdOrKey}/comment`

Add a new comment to an issue with optional visibility restrictions.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `issueIdOrKey` | string | Issue ID or key (required) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | string | Additional data: `renderedBody` |

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `body` | object | Comment content in Atlassian Document Format (required) |
| `visibility` | object | Visibility restrictions (optional) |

#### Request Example
```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "I've investigated this issue and found the root cause. The authentication service is returning invalid tokens."
          }
        ]
      }
    ]
  },
  "visibility": {
    "type": "role",
    "value": "Developers"
  }
}
```

#### Response Example
```json
{
  "id": "10001",
  "author": {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "John Smith",
    "active": true
  },
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "I've investigated this issue and found the root cause."
          }
        ]
      }
    ]
  },
  "created": "2024-01-15T14:20:00.000+0000",
  "updated": "2024-01-15T14:20:00.000+0000",
  "visibility": {
    "type": "role",
    "value": "Developers"
  }
}
```

### Update Comment

**PUT** `/issue/{issueIdOrKey}/comment/{id}`

Update an existing comment's content or visibility.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `issueIdOrKey` | string | Issue ID or key (required) |
| `id` | string | Comment ID (required) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `notifyUsers` | boolean | Send notifications to users (default: true) |
| `overrideEditableFlag` | boolean | Override edit restrictions (admin only, default: false) |
| `expand` | string | Additional data: `renderedBody` |

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `body` | object | Updated comment content (required) |
| `visibility` | object | Updated visibility restrictions (optional) |

#### Request Example
```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "type": "text",
            "text": "Updated: I've investigated this issue and found the root cause. The authentication service is returning invalid tokens. Fix deployed to staging."
          }
        ]
      }
    ]
  }
}
```

### Delete Comment

**DELETE** `/issue/{issueIdOrKey}/comment/{id}`

Delete a comment from an issue.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `issueIdOrKey` | string | Issue ID or key (required) |
| `id` | string | Comment ID (required) |

#### Request Example
```
DELETE /issue/WEB-123/comment/10000
```

#### Response
Returns `204 No Content` on successful deletion.

## Comment Properties Operations

### Get Comment Properties

**GET** `/comment/{commentId}/properties`

Get all property keys for a comment.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `commentId` | string | Comment ID (required) |

#### Request Example
```
GET /comment/10000/properties
```

#### Response Example
```json
{
  "keys": [
    {
      "key": "priority",
      "self": "https://your-domain.atlassian.net/rest/api/3/comment/10000/properties/priority"
    },
    {
      "key": "category",
      "self": "https://your-domain.atlassian.net/rest/api/3/comment/10000/properties/category"
    }
  ]
}
```

### Get Comment Property

**GET** `/comment/{commentId}/properties/{propertyKey}`

Get a specific comment property value.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `commentId` | string | Comment ID (required) |
| `propertyKey` | string | Property key (required) |

#### Request Example
```
GET /comment/10000/properties/priority
```

#### Response Example
```json
{
  "key": "priority",
  "value": "high"
}
```

### Set Comment Property

**PUT** `/comment/{commentId}/properties/{propertyKey}`

Set or update a comment property value.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `commentId` | string | Comment ID (required) |
| `propertyKey` | string | Property key (required) |

#### Request Body
Any valid JSON value for the property.

#### Request Example
```json
{
  "priority": "high",
  "category": "technical",
  "reviewed": true
}
```

### Delete Comment Property

**DELETE** `/comment/{commentId}/properties/{propertyKey}`

Delete a comment property.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `commentId` | string | Comment ID (required) |
| `propertyKey` | string | Property key (required) |

## Bulk Comment Operations

### Get Comments by IDs

**POST** `/comment/list`

Retrieve multiple comments by their IDs in a single request.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `ids` | array | Comment IDs to retrieve (required) |
| `expand` | string | Additional data: `renderedBody` |

#### Request Example
```json
{
  "ids": ["10000", "10001", "10002"],
  "expand": "renderedBody"
}
```

#### Response Example
```json
{
  "comments": [
    {
      "id": "10000",
      "author": {
        "displayName": "John Smith"
      },
      "body": {
        "type": "doc",
        "version": 1,
        "content": [...]
      },
      "created": "2024-01-15T10:30:00.000+0000"
    }
  ]
}
```

## Comment Visibility and Security

### Visibility Types

Comments can have visibility restrictions:

#### Role-based Visibility
```json
{
  "visibility": {
    "type": "role",
    "value": "Developers"
  }
}
```

#### Group-based Visibility
```json
{
  "visibility": {
    "type": "group",
    "value": "jira-developers"
  }
}
```

#### Public Comments
```json
{
  // No visibility field = public comment
}
```

### Permission Requirements

| Operation | Required Permissions |
|-----------|---------------------|
| **Read Comments** | Browse Projects + Issue View Permission |
| **Add Comments** | Browse Projects + Add Comments |
| **Edit Own Comments** | Browse Projects + Edit Own Comments |
| **Edit All Comments** | Browse Projects + Edit All Comments |
| **Delete Own Comments** | Browse Projects + Delete Own Comments |
| **Delete All Comments** | Browse Projects + Delete All Comments |

## Use Cases

### Basic Comment Management
```javascript
// Get all comments for an issue
const comments = await getIssueComments('WEB-123', {
  orderBy: 'created',
  maxResults: 50,
  expand: 'renderedBody'
});

// Add a new comment
const newComment = await addComment('WEB-123', {
  body: {
    type: 'doc',
    version: 1,
    content: [
      {
        type: 'paragraph',
        content: [
          {
            type: 'text',
            text: 'Issue has been resolved and deployed to production.'
          }
        ]
      }
    ]
  }
});

// Update existing comment
await updateComment('WEB-123', '10000', {
  body: {
    type: 'doc',
    version: 1,
    content: [
      {
        type: 'paragraph',
        content: [
          {
            type: 'text',
            text: 'Updated: Issue has been resolved and deployed to production. Monitoring for 24 hours.'
          }
        ]
      }
    ]
  }
});
```

### Comment Visibility Management
```javascript
// Add comment visible only to developers
const restrictedComment = await addComment('WEB-123', {
  body: {
    type: 'doc',
    version: 1,
    content: [
      {
        type: 'paragraph',
        content: [
          {
            type: 'text',
            text: 'Internal note: This requires database migration.'
          }
        ]
      }
    ]
  },
  visibility: {
    type: 'role',
    value: 'Developers'
  }
});

// Add comment visible to specific group
const groupComment = await addComment('WEB-123', {
  body: {
    type: 'doc',
    version: 1,
    content: [
      {
        type: 'paragraph',
        content: [
          {
            type: 'text',
            text: 'Security team review required.'
          }
        ]
      }
    ]
  },
  visibility: {
    type: 'group',
    value: 'security-team'
  }
});
```

### Comment Properties and Metadata
```javascript
// Set comment properties for categorization
await setCommentProperty('10000', 'category', 'technical');
await setCommentProperty('10000', 'priority', 'high');
await setCommentProperty('10000', 'reviewed', true);

// Get comment properties
const properties = await getCommentProperties('10000');
const priority = await getCommentProperty('10000', 'priority');

// Bulk retrieve comments with properties
const bulkComments = await getBulkComments({
  ids: ['10000', '10001', '10002'],
  expand: 'renderedBody'
});
```

### Comment Threading and Conversations
```javascript
// Get comments in chronological order
const conversation = await getIssueComments('WEB-123', {
  orderBy: 'created',
  maxResults: 100
});

// Add follow-up comment
const followUp = await addComment('WEB-123', {
  body: {
    type: 'doc',
    version: 1,
    content: [
      {
        type: 'paragraph',
        content: [
          {
            type: 'text',
            text: '@john.smith Thanks for the investigation. Can you provide the timeline for the fix?'
          }
        ]
      }
    ]
  }
});
```

## Best Practices

### Content Management
- **Use Atlassian Document Format**: Always use ADF for rich text content
- **Validate content**: Ensure ADF structure is valid before submission
- **Handle mentions**: Use proper user account IDs for @mentions
- **Rich formatting**: Leverage ADF for code blocks, links, and formatting

### Visibility and Security
- **Principle of least privilege**: Only make comments visible to necessary users
- **Consistent visibility**: Maintain consistent visibility patterns within projects
- **Document restrictions**: Clearly communicate visibility restrictions to users
- **Audit access**: Monitor who can access restricted comments

### Performance Optimization
- **Paginate comments**: Use pagination for issues with many comments
- **Selective expansion**: Only expand renderedBody when needed for display
- **Bulk operations**: Use bulk endpoints for multiple comment operations
- **Cache rendered content**: Cache HTML-rendered content for display

### User Experience
- **Real-time updates**: Implement real-time comment updates in UI
- **Notification management**: Respect user notification preferences
- **Edit history**: Track comment edit history for transparency
- **Threaded discussions**: Organize comments in logical conversation threads

## Error Handling

### Common HTTP Status Codes

| Status | Description | Common Causes |
|--------|-------------|---------------|
| `200` | Success | Request completed successfully |
| `201` | Created | Comment created successfully |
| `204` | No Content | Comment deleted successfully |
| `400` | Bad Request | Invalid ADF content or visibility settings |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Insufficient permissions for comment operation |
| `404` | Not Found | Issue or comment not found |
| `413` | Payload Too Large | Comment exceeds size limits |

### Comment-Specific Errors

| Error Type | Description | Solution |
|------------|-------------|----------|
| **Invalid ADF** | Comment body format is invalid | Validate ADF structure before submission |
| **Visibility Error** | Invalid visibility configuration | Check role/group exists and user has access |
| **Permission Denied** | User lacks comment permissions | Verify user has required project permissions |
| **Size Limit** | Comment exceeds maximum size | Reduce comment content or split into multiple comments |

### Error Response Example
```json
{
  "errorMessages": [
    "Comment body contains invalid Atlassian Document Format."
  ],
  "errors": {
    "body": "The document structure is not valid. Please check the ADF format."
  }
}
```

## Related APIs

- **[Issues API](issues-api.md)** - Manage issues that contain comments
- **[Users API](users-api.md)** - Get comment authors and manage user mentions
- **[Search API](search-api.md)** - Search for issues by comment content
- **[Projects API](projects-api.md)** - Understand project-level comment permissions

## Atlassian Document Format (ADF)

### Basic Text Structure
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Simple text content"
        }
      ]
    }
  ]
}
```

### Rich Text Examples
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This is ",
          "marks": []
        },
        {
          "type": "text",
          "text": "bold text",
          "marks": [
            {
              "type": "strong"
            }
          ]
        },
        {
          "type": "text",
          "text": " and this is ",
          "marks": []
        },
        {
          "type": "text",
          "text": "italic text",
          "marks": [
            {
              "type": "em"
            }
          ]
        }
      ]
    }
  ]
}
```

### Code Blocks
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "codeBlock",
      "attrs": {
        "language": "javascript"
      },
      "content": [
        {
          "type": "text",
          "text": "const result = await api.getComments('WEB-123');"
        }
      ]
    }
  ]
}
```

### User Mentions
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "mention",
          "attrs": {
            "id": "5b10a2844c20165700ede21g",
            "text": "@john.smith"
          }
        },
        {
          "type": "text",
          "text": " please review this issue."
        }
      ]
    }
  ]
}
```
