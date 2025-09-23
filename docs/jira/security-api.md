# Security API

## Overview
The Security API manages Jira issue security schemes and security levels. Issue security schemes control who can view issues by defining security levels with specific members (users, groups, roles). This API enables programmatic management of security configurations for projects.

## OAuth 2.0 Scopes

### Current Scopes (Stable)
- `manage:jira-project` - Read issue security schemes and levels
- `manage:jira-configuration` - Create and modify security schemes (admin only)

### Beta Scopes (Granular)
- `read:issue-security-scheme:jira` - Read security scheme details
- `read:issue-security-level:jira` - Read security level information
- `write:issue-security-scheme:jira` - Create and modify security schemes
- `write:issue-security-level:jira` - Manage security levels and members

## Endpoints

### Security Scheme Management

#### GET /rest/api/3/issuesecurityschemes
**Description**: Returns all issue security schemes
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-scheme:jira`
**Permissions**: Administer Jira global permission required

**Response**:
```json
{
  "issueSecuritySchemes": [
    {
      "id": 10000,
      "name": "Default Issue Security Scheme",
      "description": "Description for the default issue security scheme",
      "defaultSecurityLevelId": 10021,
      "self": "https://your-domain.atlassian.net/rest/api/3/issuesecurityschemes/10000"
    }
  ]
}
```

#### POST /rest/api/3/issuesecurityschemes
**Description**: Creates a new issue security scheme with levels and members
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-scheme:jira`
**Permissions**: Administer Jira global permission required

**Request Body**:
```json
{
  "name": "New security scheme",
  "description": "Newly created issue security scheme",
  "levels": [
    {
      "name": "New level",
      "description": "Newly created level",
      "isDefault": true,
      "members": [
        {
          "type": "group",
          "parameter": "administrators"
        }
      ]
    }
  ]
}
```

**Response**:
```json
{
  "id": "10001"
}
```

#### GET /rest/api/3/issuesecurityschemes/{id}
**Description**: Returns details of a specific issue security scheme
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-scheme:jira`
**Parameters**:
- `id` (path, required): Security scheme ID

#### PUT /rest/api/3/issuesecurityschemes/{id}
**Description**: Updates an issue security scheme
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-scheme:jira`
**Parameters**:
- `id` (path, required): Security scheme ID

#### DELETE /rest/api/3/issuesecurityschemes/{id}
**Description**: Deletes an issue security scheme
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-scheme:jira`
**Parameters**:
- `id` (path, required): Security scheme ID

### Security Scheme Search

#### GET /rest/api/3/issuesecurityschemes/search
**Description**: Search for issue security schemes
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-scheme:jira`
**Parameters**:
- `startAt` (query, optional): Page offset (default: 0)
- `maxResults` (query, optional): Items per page (default: 50, max: 100)
- `id` (query, optional): Filter by scheme IDs
- `projectId` (query, optional): Filter by project IDs

**Response**:
```json
{
  "values": [
    {
      "id": 10000,
      "name": "Default Issue Security Scheme",
      "description": "Default security scheme",
      "defaultSecurityLevelId": 10021,
      "levels": [
        {
          "id": "10021",
          "name": "Administrators",
          "description": "Only administrators can see this issue"
        }
      ]
    }
  ],
  "startAt": 0,
  "maxResults": 50,
  "total": 1
}
```

### Security Level Management

#### GET /rest/api/3/issuesecurityschemes/level
**Description**: Returns all security levels across all schemes
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`
**Parameters**:
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page
- `id` (query, optional): Filter by level IDs
- `schemeId` (query, optional): Filter by scheme IDs
- `onlyDefault` (query, optional): Only return default levels

#### POST /rest/api/3/issuesecurityschemes/level
**Description**: Creates security levels for multiple schemes
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`

**Request Body**:
```json
[
  {
    "schemeId": "10000",
    "name": "New Security Level",
    "description": "Level for sensitive issues",
    "members": [
      {
        "type": "user",
        "parameter": "5b10a2844c20165700ede21g"
      }
    ]
  }
]
```

#### GET /rest/api/3/issuesecurityschemes/level/default
**Description**: Returns default security levels for schemes
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`

#### PUT /rest/api/3/issuesecurityschemes/level/default
**Description**: Sets default security levels for schemes
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`

### Scheme-Specific Security Levels

#### GET /rest/api/3/issuesecurityschemes/{schemeId}/level
**Description**: Returns security levels for a specific scheme
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page

#### POST /rest/api/3/issuesecurityschemes/{schemeId}/level
**Description**: Adds security levels to a scheme
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID

#### GET /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}
**Description**: Returns details of a specific security level
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `levelId` (path, required): Security level ID

#### PUT /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}
**Description**: Updates a security level
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `levelId` (path, required): Security level ID

#### DELETE /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}
**Description**: Deletes a security level
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `levelId` (path, required): Security level ID

### Security Level Members

#### GET /rest/api/3/issuesecurityschemes/level/member
**Description**: Returns security level members across all schemes
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`
**Parameters**:
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page
- `id` (query, optional): Filter by member IDs
- `schemeId` (query, optional): Filter by scheme IDs
- `levelId` (query, optional): Filter by level IDs

#### POST /rest/api/3/issuesecurityschemes/level/member
**Description**: Adds members to security levels
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`

**Request Body**:
```json
[
  {
    "levelId": "10021",
    "members": [
      {
        "type": "user",
        "parameter": "5b10a2844c20165700ede21g"
      },
      {
        "type": "group",
        "parameter": "jira-developers"
      }
    ]
  }
]
```

#### GET /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member
**Description**: Returns members of a specific security level
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `levelId` (path, required): Security level ID
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page

#### POST /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member
**Description**: Adds members to a security level
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `levelId` (path, required): Security level ID

#### DELETE /rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member/{memberId}
**Description**: Removes a member from a security level
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-level:jira`
**Parameters**:
- `schemeId` (path, required): Security scheme ID
- `levelId` (path, required): Security level ID
- `memberId` (path, required): Member ID

### Project Security Associations

#### GET /rest/api/3/issuesecurityschemes/project
**Description**: Returns projects using issue security schemes
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-scheme:jira`
**Parameters**:
- `projectId` (query, optional): Filter by project IDs
- `schemeId` (query, optional): Filter by scheme IDs
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page

#### PUT /rest/api/3/issuesecurityschemes/project
**Description**: Associates security schemes with projects
**OAuth Scopes**: `manage:jira-configuration` or `write:issue-security-scheme:jira`

**Request Body**:
```json
{
  "oldToNewSecurityLevelMappings": [
    {
      "oldLevelId": "10020",
      "newLevelId": "10021"
    }
  ],
  "projectIds": ["10001", "10002"],
  "schemeId": "10000"
}
```

### Security Level Details

#### GET /rest/api/3/securitylevel/{id}
**Description**: Returns details of a specific security level
**OAuth Scopes**: `manage:jira-project` or `read:issue-security-level:jira`
**Parameters**:
- `id` (path, required): Security level ID

**Response**:
```json
{
  "id": "10021",
  "name": "Administrators",
  "description": "Only administrators can see this issue",
  "self": "https://your-domain.atlassian.net/rest/api/3/securitylevel/10021"
}
```

## Use Cases

### Security Scheme Discovery
```javascript
// Get all security schemes
const schemes = await fetch('/rest/api/3/issuesecurityschemes', {
  headers: { 'Authorization': 'Bearer ' + accessToken }
});

// Search for specific schemes
const searchResults = await fetch('/rest/api/3/issuesecurityschemes/search?projectId=10001', {
  headers: { 'Authorization': 'Bearer ' + accessToken }
});
```

### Creating Security Configurations
```javascript
// Create a new security scheme with multiple levels
const newScheme = await fetch('/rest/api/3/issuesecurityschemes', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Project Alpha Security',
    description: 'Security scheme for sensitive project data',
    levels: [
      {
        name: 'Public',
        description: 'Visible to all project members',
        isDefault: true,
        members: [
          { type: 'projectRole', parameter: '10002' }
        ]
      },
      {
        name: 'Confidential',
        description: 'Visible to managers only',
        members: [
          { type: 'group', parameter: 'project-managers' }
        ]
      }
    ]
  })
});
```

### Managing Security Level Members
```javascript
// Add users to a security level
await fetch('/rest/api/3/issuesecurityschemes/10000/level/10021/member', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify([
    {
      type: 'user',
      parameter: '5b10a2844c20165700ede21g'
    },
    {
      type: 'group',
      parameter: 'security-team'
    }
  ])
});

// Get current members of a security level
const members = await fetch('/rest/api/3/issuesecurityschemes/10000/level/10021/member', {
  headers: { 'Authorization': 'Bearer ' + accessToken }
});
```

### Project Security Association
```javascript
// Associate security scheme with projects
await fetch('/rest/api/3/issuesecurityschemes/project', {
  method: 'PUT',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    schemeId: '10000',
    projectIds: ['10001', '10002'],
    oldToNewSecurityLevelMappings: [
      {
        oldLevelId: '10020',
        newLevelId: '10021'
      }
    ]
  })
});
```

## Best Practices

### Security Scheme Design
- Use descriptive names that indicate access level
- Create minimal necessary security levels
- Document security level purposes clearly
- Plan member types (users, groups, roles) strategically

### Member Management
- Prefer groups over individual users for maintainability
- Use project roles for project-specific access
- Regularly audit security level memberships
- Remove unused security levels and members

### Project Integration
- Test security schemes before applying to production projects
- Plan security level migrations carefully
- Document security requirements for each project
- Monitor security level usage across projects

### Performance Considerations
- Use pagination for large result sets
- Cache security scheme data when possible
- Batch member operations when adding multiple users
- Limit concurrent security scheme modifications

## Error Codes

### Common HTTP Status Codes
- **200 OK**: Successful request
- **201 Created**: Security scheme or level created
- **204 No Content**: Successful deletion
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions (requires Administer Jira)
- **404 Not Found**: Security scheme or level not found

### Security-Specific Errors
- Security scheme name already exists
- Invalid member type or parameter
- Cannot delete scheme in use by projects
- Security level limit exceeded (100 per scheme)
- Default security level cannot be deleted

## Related APIs
- [Projects API](projects-api.md) - For associating security schemes with projects
- [Users API](users-api.md) - For managing user-based security members
- [Issues API](issues-api.md) - For applying security levels to issues
- [Permissions API](permissions-api.md) - For checking security-related permissions
