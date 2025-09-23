# Jira Issues API (v3)

The Jira Issues API v3 provides comprehensive issue management capabilities including search, retrieval, creation, updates, and commenting. This documentation covers the endpoints used in the Atlassian MCP Server.

## Base URL Structure

All Jira v3 API endpoints follow this pattern:
```
https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/{endpoint}
```

## OAuth 2.0 Scopes Required

### Granular Scopes (Recommended)
- **`read:jira-work`** - Read issues, projects, and search
- **`read:jira-user`** - Read user information
- **`write:jira-work`** - Create and update issues

### Classic Scopes (Legacy)
- **`read:jira-work`** - Read access to Jira work items
- **`write:jira-work`** - Write access to Jira work items

## Core Issue Operations

### Search Issues

**GET** `/search`

Search for issues using JQL (Jira Query Language) with comprehensive filtering and field selection.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `jql` | string | JQL query string (required) |
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50, max: 100) |
| `fields` | array | Fields to include in response |
| `expand` | array | Additional data to expand |
| `properties` | array | Issue properties to include |
| `fieldsByKeys` | boolean | Reference fields by keys instead of IDs |

#### Request Example
```
GET /search?jql=assignee=currentUser()&maxResults=50&fields=summary,status,assignee
```

#### Response

**200 - Success**
```json
{
  "expand": "names,schema",
  "startAt": 0,
  "maxResults": 50,
  "total": 123,
  "issues": [
    {
      "expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields",
      "id": "10001",
      "self": "https://your-domain.atlassian.net/rest/api/3/issue/10001",
      "key": "PROJ-1",
      "fields": {
        "summary": "Issue summary",
        "status": {
          "self": "https://your-domain.atlassian.net/rest/api/3/status/10001",
          "description": "Issue is open",
          "iconUrl": "https://your-domain.atlassian.net/images/icons/statuses/open.png",
          "name": "Open",
          "id": "10001",
          "statusCategory": {
            "self": "https://your-domain.atlassian.net/rest/api/3/statuscategory/2",
            "id": 2,
            "key": "new",
            "colorName": "blue-gray",
            "name": "To Do"
          }
        },
        "assignee": {
          "self": "https://your-domain.atlassian.net/rest/api/3/user?accountId=user123",
          "accountId": "user123",
          "displayName": "John Doe",
          "emailAddress": "john@example.com",
          "active": true
        },
        "project": {
          "self": "https://your-domain.atlassian.net/rest/api/3/project/10000",
          "id": "10000",
          "key": "PROJ",
          "name": "Project Name"
        },
        "issuetype": {
          "self": "https://your-domain.atlassian.net/rest/api/3/issuetype/10001",
          "id": "10001",
          "description": "A task that needs to be done",
          "iconUrl": "https://your-domain.atlassian.net/images/icons/issuetypes/task.png",
          "name": "Task"
        }
      }
    }
  ]
}
```

#### JQL Examples
```jql
# Issues assigned to current user
assignee = currentUser()

# Issues in specific project
project = "PROJ"

# Issues created in last 7 days
created >= -7d

# Complex query
project = "PROJ" AND status != Done AND assignee = currentUser() ORDER BY created DESC
```

---

### Get Issue

**GET** `/issue/{issueIdOrKey}`

Returns detailed information about a specific issue.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issueIdOrKey` | string | Yes | Issue ID or key (e.g., "PROJ-123") |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fields` | array | Fields to include in response |
| `expand` | array | Additional data to expand: `renderedFields`, `names`, `schema`, `operations`, `editmeta`, `changelog`, `versionedRepresentations` |
| `properties` | array | Issue properties to include |
| `fieldsByKeys` | boolean | Reference fields by keys instead of IDs |
| `updateHistory` | boolean | Include update history |

#### Response

**200 - Success**
```json
{
  "expand": "renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations",
  "id": "10001",
  "self": "https://your-domain.atlassian.net/rest/api/3/issue/10001",
  "key": "PROJ-1",
  "fields": {
    "summary": "Issue summary",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Issue description in ADF format"
            }
          ]
        }
      ]
    },
    "status": {
      "name": "Open",
      "id": "10001",
      "statusCategory": {
        "id": 2,
        "key": "new",
        "colorName": "blue-gray",
        "name": "To Do"
      }
    },
    "priority": {
      "self": "https://your-domain.atlassian.net/rest/api/3/priority/3",
      "iconUrl": "https://your-domain.atlassian.net/images/icons/priorities/medium.svg",
      "name": "Medium",
      "id": "3"
    },
    "created": "2023-01-01T12:00:00.000+0000",
    "updated": "2023-01-02T12:00:00.000+0000"
  }
}
```

**404 - Not Found**
Issue does not exist or user lacks permission.

---

### Create Issue

**POST** `/issue`

Creates a new issue in a Jira project.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Request Body

```json
{
  "fields": {
    "project": {
      "key": "PROJ"
    },
    "summary": "Issue summary",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Issue description"
            }
          ]
        }
      ]
    },
    "issuetype": {
      "name": "Task"
    },
    "priority": {
      "name": "Medium"
    },
    "assignee": {
      "accountId": "user123"
    }
  }
}
```

#### Required Fields
- **`project`** - Project key or ID
- **`summary`** - Issue title
- **`issuetype`** - Issue type name or ID

#### Common Optional Fields
- **`description`** - Issue description (ADF format)
- **`priority`** - Priority name or ID
- **`assignee`** - User account ID
- **`labels`** - Array of label strings
- **`components`** - Array of component objects
- **`fixVersions`** - Array of version objects

#### Response

**201 - Created**
```json
{
  "id": "10001",
  "key": "PROJ-123",
  "self": "https://your-domain.atlassian.net/rest/api/3/issue/10001"
}
```

**400 - Bad Request**
Invalid field values or missing required fields.

**403 - Forbidden**
User lacks permission to create issues in the project.

---

### Update Issue

**PUT** `/issue/{issueIdOrKey}`

Updates an existing issue with new field values.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issueIdOrKey` | string | Yes | Issue ID or key |

#### Request Body

```json
{
  "fields": {
    "summary": "Updated summary",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Updated description"
            }
          ]
        }
      ]
    },
    "priority": {
      "name": "High"
    }
  }
}
```

#### Response

**204 - No Content**
Issue updated successfully.

**400 - Bad Request**
Invalid field values.

**403 - Forbidden**
User lacks permission to update the issue.

**404 - Not Found**
Issue does not exist.

---

### Add Comment

**POST** `/issue/{issueIdOrKey}/comment`

Adds a comment to an issue.

**OAuth 2.0 Scopes**: `write:jira-work`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issueIdOrKey` | string | Yes | Issue ID or key |

#### Request Body

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
            "text": "This is a comment"
          }
        ]
      }
    ]
  },
  "visibility": {
    "type": "role",
    "value": "Administrators"
  }
}
```

#### Required Fields
- **`body`** - Comment content in ADF format

#### Optional Fields
- **`visibility`** - Comment visibility restrictions

#### Response

**201 - Created**
```json
{
  "self": "https://your-domain.atlassian.net/rest/api/3/issue/10001/comment/10000",
  "id": "10000",
  "author": {
    "self": "https://your-domain.atlassian.net/rest/api/3/user?accountId=user123",
    "accountId": "user123",
    "displayName": "John Doe"
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
            "text": "This is a comment"
          }
        ]
      }
    ]
  },
  "created": "2023-01-01T12:00:00.000+0000",
  "updated": "2023-01-01T12:00:00.000+0000"
}
```

## Project Operations

### Get Project

**GET** `/project/{projectIdOrKey}`

Returns project information needed for issue creation.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Response

**200 - Success**
```json
{
  "expand": "description,lead,issueTypes,url,projectKeys,permissions,insight",
  "self": "https://your-domain.atlassian.net/rest/api/3/project/10000",
  "id": "10000",
  "key": "PROJ",
  "name": "Project Name",
  "projectTypeKey": "software",
  "simplified": false,
  "style": "next-gen",
  "isPrivate": false,
  "issueTypes": [
    {
      "self": "https://your-domain.atlassian.net/rest/api/3/issuetype/10001",
      "id": "10001",
      "description": "A task that needs to be done",
      "iconUrl": "https://your-domain.atlassian.net/images/icons/issuetypes/task.png",
      "name": "Task",
      "subtask": false
    }
  ]
}
```

## Content Formats

### Atlassian Document Format (ADF)
Jira uses ADF for rich text content in descriptions and comments:

#### Simple Text
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

#### Formatted Text
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
          "text": "Bold text",
          "marks": [
            {
              "type": "strong"
            }
          ]
        }
      ]
    }
  ]
}
```

#### Lists
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "List item 1"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Error Handling

### Common Error Responses

**400 - Bad Request**
```json
{
  "errorMessages": ["Field 'summary' is required"],
  "errors": {
    "summary": "Summary is required"
  }
}
```

**401 - Unauthorized**
```json
{
  "errorMessages": ["You do not have the permission to see the specified issue."],
  "errors": {}
}
```

**403 - Forbidden**
```json
{
  "errorMessages": ["You do not have permission to create issues in this project."],
  "errors": {}
}
```

**404 - Not Found**
```json
{
  "errorMessages": ["Issue does not exist or you do not have permission to see it."],
  "errors": {}
}
```

## JQL Reference

### Basic Operators
- `=` - Equals
- `!=` - Not equals
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `~` - Contains
- `!~` - Does not contain
- `IN` - In list
- `NOT IN` - Not in list
- `IS` - Is (for null values)
- `IS NOT` - Is not (for null values)

### Common Fields
- `project` - Project key or name
- `assignee` - Assigned user
- `reporter` - Issue creator
- `status` - Issue status
- `priority` - Issue priority
- `created` - Creation date
- `updated` - Last update date
- `summary` - Issue title
- `description` - Issue description
- `labels` - Issue labels

### Functions
- `currentUser()` - Current logged-in user
- `now()` - Current date/time
- `startOfDay()` - Start of current day
- `endOfDay()` - End of current day

### Date Formats
- Relative: `-1d`, `-1w`, `-1M`, `-1y`
- Absolute: `"2023-01-01"`, `"2023-01-01 12:00"`

## Best Practices

### Performance
- Use specific JQL queries to limit result sets
- Include only necessary fields in responses
- Use pagination for large result sets
- Cache project and issue type information

### Content Management
- Use ADF format for rich text content
- Validate field values before submission
- Handle required fields appropriately
- Use meaningful issue summaries and descriptions

### Error Handling
- Check project permissions before creating issues
- Validate issue keys before operations
- Handle field validation errors gracefully
- Provide user-friendly error messages

### Security
- Use minimal required OAuth scopes
- Validate user permissions for operations
- Sanitize user input in descriptions and comments
- Respect project and issue-level security settings
