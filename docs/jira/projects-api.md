# Jira Projects API (v3)

The Jira Projects API v3 provides comprehensive project management capabilities including discovery, creation, updates, and configuration. This documentation covers the endpoints used in the Atlassian MCP Server.

## Base URL Structure

All Jira v3 API endpoints follow this pattern:
```
https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/{endpoint}
```

## OAuth 2.0 Scopes Required

### Granular Scopes (Recommended)
- **`read:jira-work`** - Read projects and basic information
- **`write:jira-work`** - Create and update projects (limited)
- **`manage:jira-project`** - Full project management capabilities
- **`manage:jira-configuration`** - Administrative project operations

### Classic Scopes (Legacy)
- **`read:jira-work`** - Read access to projects
- **`write:jira-work`** - Write access to projects
- **`manage:jira-project`** - Project management
- **`manage:jira-configuration`** - Administrative access

## Core Project Operations

### Search Projects (Recommended)

**GET** `/project/search`

Search for projects with comprehensive filtering, pagination, and sorting capabilities. This is the recommended method for project discovery.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `startAt` | integer | Starting index for pagination (default: 0) |
| `maxResults` | integer | Maximum results per page (default: 50, max: 100) |
| `orderBy` | string | Sort field: `key`, `name`, `category`, `owner`, `issueCount`, `lastIssueUpdatedDate` |
| `id` | array | Filter by project IDs (up to 50) |
| `keys` | array | Filter by project keys (up to 50) |
| `query` | string | Search by project name or key (case insensitive) |
| `typeKey` | string | Filter by project type: `business`, `service_desk`, `software` |
| `categoryId` | integer | Filter by project category ID |
| `action` | string | Permission filter: `view`, `browse`, `edit`, `create` (default: `view`) |
| `expand` | string | Additional data: `description`, `projectKeys`, `lead`, `issueTypes`, `url`, `insight` |
| `status` | array | Project status: `live`, `archived`, `deleted` |

#### Request Example
```
GET /project/search?query=web&typeKey=software&maxResults=20&orderBy=name&expand=description,lead
```

#### Response Example
```json
{
  "startAt": 0,
  "maxResults": 20,
  "total": 2,
  "isLast": true,
  "values": [
    {
      "id": "10000",
      "key": "WEB",
      "name": "Web Application",
      "description": "Main web application project",
      "projectTypeKey": "software",
      "simplified": false,
      "style": "classic",
      "lead": {
        "accountId": "5b10a2844c20165700ede21g",
        "displayName": "John Smith",
        "active": true
      },
      "avatarUrls": {
        "48x48": "https://your-domain.atlassian.net/secure/projectavatar?size=large&pid=10000"
      },
      "projectCategory": {
        "id": "10000",
        "name": "Development",
        "description": "Development projects"
      },
      "insight": {
        "totalIssueCount": 150,
        "lastIssueUpdateTime": "2024-01-15T10:30:00.000+0000"
      }
    }
  ]
}
```

### Get Project Details

**GET** `/project/{projectIdOrKey}`

Retrieve detailed information about a specific project including components, versions, and issue types.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectIdOrKey` | string | Project ID or project key (case sensitive) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | string | Additional data: `description`, `issueTypes`, `lead`, `projectKeys`, `issueTypeHierarchy` |
| `properties` | array | Project properties to include |

#### Request Example
```
GET /project/WEB?expand=description,issueTypes,lead
```

#### Response Example
```json
{
  "id": "10000",
  "key": "WEB",
  "name": "Web Application",
  "description": "Main web application project",
  "lead": {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "John Smith",
    "emailAddress": "john.smith@company.com",
    "active": true
  },
  "components": [
    {
      "id": "10100",
      "name": "Frontend",
      "description": "React frontend components"
    }
  ],
  "issueTypes": [
    {
      "id": "10001",
      "name": "Story",
      "description": "User story",
      "subtask": false
    },
    {
      "id": "10002", 
      "name": "Bug",
      "description": "Software defect",
      "subtask": false
    }
  ],
  "versions": [],
  "roles": {
    "Developers": "https://your-domain.atlassian.net/rest/api/3/project/WEB/role/10000"
  },
  "projectTypeKey": "software",
  "simplified": false,
  "style": "classic",
  "assigneeType": "PROJECT_LEAD"
}
```

### Create Project

**POST** `/project`

Create a new project based on a project template. Requires administrative permissions.

**OAuth 2.0 Scopes**: `manage:jira-configuration`

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | Yes | Project key (2-10 uppercase characters) |
| `name` | string | Yes | Project name |
| `projectTypeKey` | string | Yes | Project type: `business`, `service_desk`, `software` |
| `projectTemplateKey` | string | Yes | Template key for project type |
| `description` | string | No | Project description |
| `leadAccountId` | string | No | Project lead account ID |
| `url` | string | No | Project URL |
| `assigneeType` | string | No | Default assignee: `PROJECT_LEAD`, `UNASSIGNED` |
| `avatarId` | integer | No | Avatar ID |
| `categoryId` | integer | No | Project category ID |
| `permissionScheme` | integer | No | Permission scheme ID |
| `notificationScheme` | integer | No | Notification scheme ID |
| `issueSecurityScheme` | integer | No | Issue security scheme ID |

#### Request Example
```json
{
  "key": "MOBILE",
  "name": "Mobile Application",
  "projectTypeKey": "software",
  "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",
  "description": "Mobile app development project",
  "leadAccountId": "5b10a2844c20165700ede21g",
  "assigneeType": "PROJECT_LEAD"
}
```

#### Response Example
```json
{
  "id": 10001,
  "key": "MOBILE",
  "self": "https://your-domain.atlassian.net/rest/api/3/project/10001"
}
```

### Update Project

**PUT** `/project/{projectIdOrKey}`

Update project details. All parameters are optional - only included fields will be updated.

**OAuth 2.0 Scopes**: `manage:jira-project` (basic updates) or `manage:jira-configuration` (scheme changes)

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectIdOrKey` | string | Project ID or project key (case sensitive) |

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project name |
| `description` | string | Project description |
| `leadAccountId` | string | Project lead account ID |
| `url` | string | Project URL |
| `assigneeType` | string | Default assignee type |
| `avatarId` | integer | Avatar ID |
| `categoryId` | integer | Project category ID |
| `permissionScheme` | integer | Permission scheme ID (requires admin) |
| `notificationScheme` | integer | Notification scheme ID (requires admin) |
| `issueSecurityScheme` | integer | Issue security scheme ID (requires admin) |

#### Request Example
```json
{
  "name": "Mobile App - Updated",
  "description": "Updated mobile application project",
  "url": "https://mobile.company.com"
}
```

### Delete Project

**DELETE** `/project/{projectIdOrKey}`

Delete a project. Projects are moved to recycle bin by default for recovery.

**OAuth 2.0 Scopes**: `manage:jira-configuration`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectIdOrKey` | string | Project ID or project key (case sensitive) |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `enableUndo` | boolean | Move to recycle bin for recovery (default: true) |

#### Request Example
```
DELETE /project/MOBILE?enableUndo=true
```

## Project Discovery Operations

### Get All Projects (Deprecated)

**GET** `/project`

**⚠️ Deprecated**: Use `/project/search` instead for better performance and pagination.

Returns all visible projects. Limited functionality compared to search endpoint.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | string | Additional data to include |
| `recent` | integer | Number of recent projects (max: 20) |
| `properties` | array | Project properties to include |

### Get Recent Projects

**GET** `/project/recent`

Get recently accessed projects for the current user.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | string | Additional data to include |
| `properties` | array | Project properties to include |

## Project Type Operations

### Get Project Types

**GET** `/project/type`

Get all available project types in the Jira instance.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Response Example
```json
[
  {
    "key": "software",
    "formattedKey": "Software",
    "descriptionI18nKey": "jira.project.type.software.description",
    "icon": "software.png",
    "color": "#0052CC"
  },
  {
    "key": "business", 
    "formattedKey": "Business",
    "descriptionI18nKey": "jira.project.type.business.description",
    "icon": "business.png",
    "color": "#FF5630"
  }
]
```

### Get Accessible Project Types

**GET** `/project/type/accessible`

Get project types accessible to the current user for project creation.

**OAuth 2.0 Scopes**: `read:jira-work`

### Get Project Type Details

**GET** `/project/type/{projectTypeKey}`

Get details for a specific project type.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `projectTypeKey` | string | Project type key: `business`, `service_desk`, `software` |

## Project Categories

### Get All Project Categories

**GET** `/projectCategory`

Get all project categories available in the Jira instance.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Response Example
```json
[
  {
    "id": "10000",
    "name": "Development",
    "description": "Software development projects",
    "self": "https://your-domain.atlassian.net/rest/api/3/projectCategory/10000"
  },
  {
    "id": "10001",
    "name": "Marketing", 
    "description": "Marketing and campaigns",
    "self": "https://your-domain.atlassian.net/rest/api/3/projectCategory/10001"
  }
]
```

### Get Project Category

**GET** `/projectCategory/{id}`

Get details for a specific project category.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Project category ID |

## Project Validation

### Validate Project Key

**GET** `/projectvalidate/key`

Validate if a project key is available and follows naming rules.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | string | Project key to validate |

#### Response Example
```json
{
  "errorMessages": [],
  "errors": {}
}
```

### Validate Project Name

**GET** `/projectvalidate/validProjectName`

Validate if a project name is acceptable.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Project name to validate |

## Use Cases

### Project Discovery and Selection
```javascript
// Search for software projects
const projects = await searchProjects({
  typeKey: 'software',
  action: 'browse',
  expand: 'description,lead,insight',
  maxResults: 50
});

// Get specific project details
const project = await getProject('WEB', {
  expand: 'issueTypes,components,versions'
});
```

### Project Creation Workflow
```javascript
// Validate project key first
await validateProjectKey('NEWPROJ');

// Create project with template
const newProject = await createProject({
  key: 'NEWPROJ',
  name: 'New Project',
  projectTypeKey: 'software',
  projectTemplateKey: 'com.pyxis.greenhopper.jira:gh-simplified-agility-scrum',
  description: 'New software project',
  leadAccountId: 'user-account-id'
});
```

### Project Management
```javascript
// Update project details
await updateProject('PROJ', {
  name: 'Updated Project Name',
  description: 'Updated description',
  url: 'https://project.company.com'
});

// Archive project (soft delete)
await deleteProject('PROJ', { enableUndo: true });
```

## Best Practices

### Project Discovery
- **Use search endpoint**: Prefer `/project/search` over deprecated `/project` endpoint
- **Filter appropriately**: Use `action` parameter to filter by user permissions
- **Paginate results**: Use `startAt` and `maxResults` for large result sets
- **Expand selectively**: Only request additional data you need via `expand`

### Project Creation
- **Validate first**: Always validate project key and name before creation
- **Choose appropriate template**: Select template matching your project workflow
- **Set proper permissions**: Configure permission schemes during creation
- **Use meaningful keys**: Project keys should be short but descriptive

### Performance Optimization
- **Cache project lists**: Project data changes infrequently
- **Use specific filters**: Reduce API calls with targeted queries
- **Batch operations**: Group related project operations when possible
- **Monitor rate limits**: Respect API rate limiting for bulk operations

### Security Considerations
- **Scope appropriately**: Use minimal required OAuth scopes
- **Validate permissions**: Check user permissions before project operations
- **Audit changes**: Log project creation and modification activities
- **Protect sensitive data**: Be careful with project properties and metadata

## Error Handling

### Common HTTP Status Codes

| Status | Description | Common Causes |
|--------|-------------|---------------|
| `200` | Success | Request completed successfully |
| `201` | Created | Project created successfully |
| `204` | No Content | Project deleted successfully |
| `400` | Bad Request | Invalid project data or parameters |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Insufficient permissions for operation |
| `404` | Not Found | Project not found or no access |
| `409` | Conflict | Project key already exists |

### Error Response Example
```json
{
  "errorMessages": [
    "A project with that name already exists."
  ],
  "errors": {
    "projectKey": "Project key 'TEST' already exists."
  }
}
```

## Related APIs

- **[Issues API](issues-api.md)** - Create and manage issues within projects
- **[Search API](search-api.md)** - Search for issues across projects
- **[Users API](users-api.md)** - Manage project leads and assignees
- **[Components API](components-api.md)** - Manage project components
- **[Versions API](versions-api.md)** - Manage project versions
- **[Permissions API](permissions-api.md)** - Check project permissions

## Project Templates Reference

### Software Projects
- `com.pyxis.greenhopper.jira:gh-simplified-agility-kanban` - Kanban board
- `com.pyxis.greenhopper.jira:gh-simplified-agility-scrum` - Scrum board
- `com.pyxis.greenhopper.jira:gh-simplified-basic` - Basic software project

### Business Projects  
- `com.atlassian.jira-core-project-templates:jira-core-simplified-content-management` - Content management
- `com.atlassian.jira-core-project-templates:jira-core-simplified-project-management` - Project management
- `com.atlassian.jira-core-project-templates:jira-core-simplified-task-tracking` - Task tracking

### Service Desk Projects
- `com.atlassian.servicedesk:simplified-it-service-management` - IT service desk
- `com.atlassian.servicedesk:simplified-hr-service-desk` - HR service desk
- `com.atlassian.servicedesk:simplified-general-service-desk-it` - General IT support
