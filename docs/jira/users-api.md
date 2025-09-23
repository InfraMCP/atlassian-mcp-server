# Jira Users API (v3)

The Jira Users API v3 provides comprehensive user management capabilities including user discovery, search, permissions, and profile information. This documentation covers the user endpoints used in the Atlassian MCP Server.

## Base URL Structure

All Jira v3 API endpoints follow this pattern:
```
https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/{endpoint}
```

## OAuth 2.0 Scopes Required

### Granular Scopes (Recommended)
- **`read:jira-user`** - Read user information and search users
- **`read:jira-work`** - Required for assignable user searches

### Classic Scopes (Legacy)
- **`read:jira-user`** - Read access to user information

## Core User Operations

### Get Current User

**GET** `/myself`

Get detailed information about the currently authenticated user.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | string | Additional data: `groups`, `applicationRoles` |

#### Request Example
```
GET /myself?expand=groups,applicationRoles
```

#### Response Example
```json
{
  "accountId": "5b10a2844c20165700ede21g",
  "accountType": "atlassian",
  "active": true,
  "displayName": "John Smith",
  "emailAddress": "john.smith@company.com",
  "timeZone": "America/New_York",
  "avatarUrls": {
    "16x16": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=16&s=16",
    "24x24": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=24&s=24",
    "32x32": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=32&s=32",
    "48x48": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=48&s=48"
  },
  "groups": {
    "size": 3,
    "items": [
      {
        "name": "jira-developers",
        "groupId": "276f955c-63d7-42c8-9520-92d01dca0625"
      }
    ]
  },
  "applicationRoles": {
    "size": 1,
    "items": [
      {
        "key": "jira-software",
        "name": "Jira Software"
      }
    ]
  }
}
```

### Search Users

**GET** `/user/search`

Search for users by display name, email address, or account ID with privacy controls applied.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term matching displayName or emailAddress (required unless accountId/property) |
| `accountId` | string | Exact account ID match (required unless query/property) |
| `property` | string | Property-based search (required unless query/accountId) |
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50) |

#### Request Example
```
GET /user/search?query=john&maxResults=20
```

#### Response Example
```json
[
  {
    "accountId": "5b10a2844c20165700ede21g",
    "accountType": "atlassian",
    "active": true,
    "displayName": "John Smith",
    "avatarUrls": {
      "48x48": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=48&s=48"
    }
  },
  {
    "accountId": "5b10ac8d82e05b22cc7d4ef5",
    "accountType": "atlassian", 
    "active": true,
    "displayName": "John Doe"
  }
]
```

### Find Assignable Users

**GET** `/user/assignable/search`

Find users who can be assigned to issues in a specific project or to a specific issue.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term (required unless accountId) |
| `accountId` | string | Specific account ID to check |
| `project` | string | Project key/ID (required unless issueKey/issueId) |
| `issueKey` | string | Issue key (required unless project/issueId) |
| `issueId` | string | Issue ID (required unless project/issueKey) |
| `actionDescriptorId` | integer | Transition ID for workflow-specific assignment |
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50) |
| `recommend` | boolean | Include recommended assignees (default: false) |

#### Request Example
```
GET /user/assignable/search?query=john&project=WEB&recommend=true
```

#### Response Example
```json
[
  {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "John Smith",
    "active": true,
    "emailAddress": "john.smith@company.com",
    "avatarUrls": {
      "48x48": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=48&s=48"
    }
  }
]
```

### Find Users with Issue View Permission

**GET** `/user/viewissue/search`

Find users who have permission to view a specific issue.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term (required unless accountId) |
| `accountId` | string | Specific account ID to check |
| `issueKey` | string | Issue key (required unless issueId) |
| `issueId` | string | Issue ID (required unless issueKey) |
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50) |

#### Request Example
```
GET /user/viewissue/search?query=john&issueKey=WEB-123
```

### Find Users with Permissions

**GET** `/user/permission/search`

Find users who have specific permissions in projects.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term (required unless accountId) |
| `accountId` | string | Specific account ID to check |
| `permissions` | string | Comma-separated permission keys |
| `issueKey` | string | Issue context for permission check |
| `projectKey` | string | Project context for permission check |
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50) |

#### Request Example
```
GET /user/permission/search?query=john&permissions=BROWSE_PROJECTS,CREATE_ISSUES&projectKey=WEB
```

## User Discovery Operations

### Get All Users

**GET** `/users/search`

Get all users in the Jira instance with comprehensive filtering options.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50, max: 1000) |

#### Request Example
```
GET /users/search?maxResults=100
```

### User Picker Search

**GET** `/user/picker`

Get user suggestions for picker components with enhanced search capabilities.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term for user picker |
| `maxResults` | integer | Maximum results (default: 50) |
| `showAvatar` | boolean | Include avatar URLs (default: false) |
| `exclude` | array | Account IDs to exclude from results |

#### Request Example
```
GET /user/picker?query=john&maxResults=10&showAvatar=true
```

#### Response Example
```json
{
  "users": [
    {
      "accountId": "5b10a2844c20165700ede21g",
      "name": "john.smith",
      "displayName": "John Smith",
      "avatarUrl": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/JS-5.png?size=48&s=48"
    }
  ],
  "total": 1,
  "header": "Showing 1 of 1 matching users"
}
```

## User Group Operations

### Get User Groups

**GET** `/user/groups`

Get groups that a user belongs to.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `accountId` | string | User account ID (required) |

#### Request Example
```
GET /user/groups?accountId=5b10a2844c20165700ede21g
```

#### Response Example
```json
[
  {
    "name": "jira-developers",
    "groupId": "276f955c-63d7-42c8-9520-92d01dca0625",
    "self": "https://your-domain.atlassian.net/rest/api/3/group?groupId=276f955c-63d7-42c8-9520-92d01dca0625"
  },
  {
    "name": "jira-administrators",
    "groupId": "5b10ac8d82e05b22cc7d4ef5"
  }
]
```

## User Properties Operations

### Get User Properties

**GET** `/user/properties`

Get all property keys for a user.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `accountId` | string | User account ID (required) |

#### Request Example
```
GET /user/properties?accountId=5b10a2844c20165700ede21g
```

### Get User Property

**GET** `/user/properties/{propertyKey}`

Get a specific user property value.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `propertyKey` | string | Property key |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `accountId` | string | User account ID (required) |

#### Request Example
```
GET /user/properties/theme?accountId=5b10a2844c20165700ede21g
```

## Bulk User Operations

### Get Users by Account IDs

**GET** `/user/bulk`

Get multiple users by their account IDs in a single request.

**OAuth 2.0 Scopes**: `read:jira-user`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `accountId` | array | Account IDs to retrieve (max: 1000) |

#### Request Example
```
GET /user/bulk?accountId=5b10a2844c20165700ede21g&accountId=5b10ac8d82e05b22cc7d4ef5
```

#### Response Example
```json
[
  {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "John Smith",
    "active": true
  },
  {
    "accountId": "5b10ac8d82e05b22cc7d4ef5", 
    "displayName": "Jane Doe",
    "active": true
  }
]
```

### Get User Email Addresses

**GET** `/user/email/bulk`

Get email addresses for multiple users (requires additional permissions).

**OAuth 2.0 Scopes**: `read:jira-user` + admin permissions

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `accountId` | array | Account IDs to get emails for |

## Use Cases

### User Authentication and Profile
```javascript
// Get current user information
const currentUser = await getCurrentUser({
  expand: 'groups,applicationRoles'
});

// Check user's groups and permissions
const userGroups = await getUserGroups(currentUser.accountId);
```

### User Search and Discovery
```javascript
// Search for users by name
const users = await searchUsers({
  query: 'john',
  maxResults: 20
});

// Find users by exact account ID
const specificUser = await searchUsers({
  accountId: '5b10a2844c20165700ede21g'
});

// User picker for UI components
const pickerResults = await getUserPicker({
  query: 'john',
  maxResults: 10,
  showAvatar: true
});
```

### Assignment and Permissions
```javascript
// Find users who can be assigned to a project
const assignableUsers = await findAssignableUsers({
  query: 'john',
  project: 'WEB',
  recommend: true
});

// Check if user can view specific issue
const viewableUsers = await findUsersWithViewPermission({
  query: 'john',
  issueKey: 'WEB-123'
});

// Find users with specific permissions
const permissionUsers = await findUsersWithPermissions({
  query: 'admin',
  permissions: 'ADMINISTER_PROJECTS,BROWSE_PROJECTS',
  projectKey: 'WEB'
});
```

### Bulk Operations
```javascript
// Get multiple users at once
const bulkUsers = await getBulkUsers([
  '5b10a2844c20165700ede21g',
  '5b10ac8d82e05b22cc7d4ef5'
]);

// Get all users for admin operations
const allUsers = await getAllUsers({
  maxResults: 1000
});
```

## Best Practices

### Privacy and Security
- **Respect privacy controls**: Email addresses may be hidden based on user preferences
- **Use account IDs**: Always use account IDs instead of usernames for API calls
- **Minimal data requests**: Only request user data you actually need
- **Cache user data**: User information changes infrequently, cache appropriately

### Search Optimization
- **Use specific searches**: Prefer assignable/permission searches over general user search
- **Implement pagination**: Use startAt/maxResults for large user bases
- **Rate limit awareness**: User search endpoints have collective rate limits
- **Debounce searches**: Implement debouncing for real-time user picker searches

### Performance Considerations
- **Bulk operations**: Use bulk endpoints when retrieving multiple users
- **Field selection**: Request only necessary user fields
- **Search scope**: Limit searches to relevant contexts (project, issue)
- **Caching strategy**: Cache user picker results and group memberships

### Error Handling
- **Handle rate limits**: Respect Retry-After headers for user search endpoints
- **Privacy fallbacks**: Handle cases where user data is restricted
- **Permission checks**: Verify user has required permissions before operations
- **Account validation**: Validate account IDs before making requests

## Error Handling

### Common HTTP Status Codes

| Status | Description | Common Causes |
|--------|-------------|---------------|
| `200` | Success | Request completed successfully |
| `400` | Bad Request | Missing required parameters or invalid account ID |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Insufficient permissions to access user data |
| `404` | Not Found | User account not found |
| `429` | Rate Limited | User search rate limit exceeded |

### Rate Limiting
User search endpoints share a collective rate limit per tenant:
- **Respect Retry-After**: Wait for the specified time before retrying
- **Implement backoff**: Use exponential backoff for repeated failures
- **Cache results**: Reduce API calls by caching user search results
- **Batch requests**: Use bulk endpoints when possible

### Privacy Controls
Users can control visibility of their information:
- **Email addresses**: May be hidden from API responses
- **Profile details**: Some fields may be restricted
- **Graceful handling**: Design UI to handle missing user data
- **Fallback display**: Use display names when email is unavailable

### Error Response Example
```json
{
  "errorMessages": [
    "Rate limit exceeded. Please wait before making more requests."
  ],
  "errors": {}
}
```

## Related APIs

- **[Issues API](issues-api.md)** - Assign users to issues and track user activity
- **[Projects API](projects-api.md)** - Manage project leads and user permissions
- **[Search API](search-api.md)** - Search for issues by assignee and user activity
- **[Comments API](comments-api.md)** - Track comment authors and user interactions
- **[Permissions API](permissions-api.md)** - Check user permissions and access levels

## User Account Migration

### Account ID Usage
- **Always use account IDs**: Usernames are deprecated and may not work
- **Account ID format**: Atlassian account IDs are typically 24-character strings
- **Migration support**: Use bulk migration endpoints for large-scale updates
- **Validation**: Validate account IDs before storing or using in operations

### Legacy Username Support
Some endpoints still accept usernames but this is deprecated:
- **Avoid usernames**: Use account IDs for all new integrations
- **Migration path**: Convert existing username references to account IDs
- **Bulk conversion**: Use bulk endpoints to convert usernames to account IDs

## Privacy and GDPR Compliance

### Profile Visibility
Users control what information is visible:
- **Email addresses**: May be hidden based on user privacy settings
- **Display names**: Always available for active users
- **Avatar URLs**: Available based on user preferences
- **Time zones**: Available for authenticated requests

### Data Handling
- **Minimal collection**: Only collect user data necessary for functionality
- **Secure storage**: Store user data securely and encrypt sensitive information
- **Data retention**: Implement appropriate data retention policies
- **User rights**: Support user requests for data access and deletion
