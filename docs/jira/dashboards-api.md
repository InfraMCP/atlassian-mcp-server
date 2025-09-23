# Dashboards API

## Overview
The Dashboards API enables management of Jira dashboards and their gadgets. Dashboards provide customizable views of project data through configurable gadgets that display charts, filters, and other information.

## OAuth 2.0 Scopes

### Current Scopes (Stable)
- `read:jira-work` - Read dashboard information and properties
- `write:jira-work` - Create, update, and delete dashboards and gadgets

### Beta Scopes (Granular)
- `read:dashboard:jira` - Read dashboard details and configurations
- `write:dashboard:jira` - Create, update, and delete dashboards
- `read:dashboard.property:jira` - Read dashboard item properties
- `write:dashboard.property:jira` - Manage dashboard item properties
- `delete:dashboard.property:jira` - Delete dashboard item properties

## Endpoints

### Dashboard Management

#### GET /rest/api/3/dashboard
**Description**: Returns a list of dashboards owned by or shared with the user
**OAuth Scopes**: `read:jira-work` or `read:dashboard:jira`
**Parameters**:
- `filter` (query, optional): Filter dashboards (`my`, `favourite`)
- `startAt` (query, optional): Page offset (default: 0)
- `maxResults` (query, optional): Items per page (default: 20)

**Response**:
```json
{
  "dashboards": [
    {
      "id": "10000",
      "name": "System Dashboard",
      "isFavourite": false,
      "popularity": 1,
      "owner": {
        "accountId": "5b10a2844c20165700ede21g",
        "displayName": "Mia Krystof"
      },
      "sharePermissions": [
        {
          "type": "global"
        }
      ],
      "self": "https://your-domain.atlassian.net/rest/api/3/dashboard/10000",
      "view": "https://your-domain.atlassian.net/secure/Dashboard.jspa?selectPageId=10000"
    }
  ],
  "startAt": 0,
  "maxResults": 20,
  "total": 143
}
```

**Example**:
```bash
curl -X GET \
  'https://your-domain.atlassian.net/rest/api/3/dashboard?filter=my&maxResults=10' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

#### POST /rest/api/3/dashboard
**Description**: Creates a new dashboard
**OAuth Scopes**: `write:jira-work` or `write:dashboard:jira`
**Parameters**:
- `extendAdminPermissions` (query, optional): Use admin permissions (default: false)

**Request Body**:
```json
{
  "name": "Auditors dashboard",
  "description": "A dashboard to help auditors identify sample of issues to check.",
  "sharePermissions": [
    {
      "type": "global"
    }
  ],
  "editPermissions": []
}
```

**Response**: Returns created dashboard object (same format as GET)

#### GET /rest/api/3/dashboard/{id}
**Description**: Returns details of a specific dashboard
**OAuth Scopes**: `read:jira-work` or `read:dashboard:jira`
**Parameters**:
- `id` (path, required): Dashboard ID

**Response**: Returns dashboard object (same format as GET /dashboard)

#### PUT /rest/api/3/dashboard/{id}
**Description**: Updates a dashboard, replacing all details
**OAuth Scopes**: `write:jira-work` or `write:dashboard:jira`
**Parameters**:
- `id` (path, required): Dashboard ID to update
- `extendAdminPermissions` (query, optional): Use admin permissions (default: false)

**Request Body**: Same format as POST /dashboard

#### DELETE /rest/api/3/dashboard/{id}
**Description**: Deletes a dashboard (must be owned by user)
**OAuth Scopes**: `write:jira-work` or `delete:dashboard:jira`
**Parameters**:
- `id` (path, required): Dashboard ID

**Response**: 204 No Content on success

#### POST /rest/api/3/dashboard/{id}/copy
**Description**: Copies a dashboard with optional modifications
**OAuth Scopes**: `write:jira-work` or `write:dashboard:jira`
**Parameters**:
- `id` (path, required): Dashboard ID to copy
- `extendAdminPermissions` (query, optional): Use admin permissions (default: false)

**Request Body**: Dashboard details to override in the copy

### Dashboard Search

#### GET /rest/api/3/dashboard/search
**Description**: Search for dashboards using filters and text queries
**OAuth Scopes**: `read:jira-work` or `read:dashboard:jira`
**Parameters**:
- `dashboardName` (query, optional): Dashboard name filter
- `accountId` (query, optional): Owner account ID
- `owner` (query, optional): Owner username
- `groupname` (query, optional): Group with access
- `projectId` (query, optional): Project ID
- `orderBy` (query, optional): Sort field (`name`, `favourite_count`, `id`, `is_favourite`, `owner`)
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page
- `expand` (query, optional): Additional fields to include

### Bulk Operations

#### PUT /rest/api/3/dashboard/bulk/edit
**Description**: Bulk edit multiple dashboards
**OAuth Scopes**: `write:jira-work` or `write:dashboard:jira`
**Request Body**:
```json
{
  "entityIds": ["10000", "10001"],
  "changeOwnerDetails": {
    "newOwner": "5b10a2844c20165700ede21g"
  }
}
```

### Gadget Management

#### GET /rest/api/3/dashboard/gadgets
**Description**: Returns available gadgets that can be added to dashboards
**OAuth Scopes**: `read:jira-work` or `read:dashboard:jira`
**Parameters**:
- `dashboardId` (query, optional): Filter gadgets for specific dashboard

#### GET /rest/api/3/dashboard/{dashboardId}/gadget
**Description**: Returns gadgets on a specific dashboard
**OAuth Scopes**: `read:jira-work` or `read:dashboard:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `moduleKey` (query, optional): Filter by gadget module key
- `uri` (query, optional): Filter by gadget URI
- `gadgetId` (query, optional): Filter by specific gadget ID

#### POST /rest/api/3/dashboard/{dashboardId}/gadget
**Description**: Adds a gadget to a dashboard
**OAuth Scopes**: `write:jira-work` or `write:dashboard:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID

**Request Body**:
```json
{
  "title": "My new gadget title",
  "color": "red",
  "position": {
    "row": 1,
    "column": 1
  },
  "moduleKey": "com.atlassian.jira.gadgets:assigned-to-me-gadget"
}
```

#### PUT /rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}
**Description**: Updates a gadget on a dashboard
**OAuth Scopes**: `write:jira-work` or `write:dashboard:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `gadgetId` (path, required): Gadget ID

**Request Body**: Same format as POST gadget

#### DELETE /rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}
**Description**: Removes a gadget from a dashboard
**OAuth Scopes**: `write:jira-work` or `delete:dashboard:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `gadgetId` (path, required): Gadget ID

### Dashboard Item Properties

#### GET /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties
**Description**: Returns property keys for a dashboard item
**OAuth Scopes**: `read:jira-work` or `read:dashboard.property:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `itemId` (path, required): Dashboard item ID

#### GET /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
**Description**: Returns a specific dashboard item property
**OAuth Scopes**: `read:jira-work` or `read:dashboard.property:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `itemId` (path, required): Dashboard item ID
- `propertyKey` (path, required): Property key

**Response**:
```json
{
  "key": "issue.support",
  "value": {
    "system.conversation.id": "b1bf38be-5e94-4b40-a3b8-9278735ee1e6",
    "system.support.time": "1m"
  }
}
```

#### PUT /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
**Description**: Sets a dashboard item property value
**OAuth Scopes**: `write:jira-work` or `write:dashboard.property:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `itemId` (path, required): Dashboard item ID
- `propertyKey` (path, required): Property key (max 255 characters)

**Request Body**: JSON value (max 32768 bytes)
```json
{
  "number": 5,
  "string": "string-value"
}
```

#### DELETE /rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
**Description**: Deletes a dashboard item property
**OAuth Scopes**: `write:jira-work` or `delete:dashboard.property:jira`
**Parameters**:
- `dashboardId` (path, required): Dashboard ID
- `itemId` (path, required): Dashboard item ID
- `propertyKey` (path, required): Property key

## Use Cases

### Dashboard Discovery
```javascript
// Get user's favorite dashboards
const favorites = await fetch('/rest/api/3/dashboard?filter=favourite', {
  headers: { 'Authorization': 'Bearer ' + accessToken }
});

// Search for dashboards by name
const searchResults = await fetch('/rest/api/3/dashboard/search?dashboardName=audit', {
  headers: { 'Authorization': 'Bearer ' + accessToken }
});
```

### Dashboard Management
```javascript
// Create a project-specific dashboard
const newDashboard = await fetch('/rest/api/3/dashboard', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Project Alpha Dashboard',
    description: 'Dashboard for tracking Project Alpha progress',
    sharePermissions: [
      { type: 'project', project: { id: '10001' } }
    ]
  })
});

// Copy existing dashboard with modifications
const copiedDashboard = await fetch('/rest/api/3/dashboard/10000/copy', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Project Beta Dashboard',
    sharePermissions: [
      { type: 'project', project: { id: '10002' } }
    ]
  })
});
```

### Gadget Configuration
```javascript
// Add an assigned issues gadget
const gadget = await fetch('/rest/api/3/dashboard/10000/gadget', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'My Assigned Issues',
    moduleKey: 'com.atlassian.jira.gadgets:assigned-to-me-gadget',
    position: { row: 1, column: 1 },
    color: 'blue'
  })
});

// Store gadget configuration
await fetch(`/rest/api/3/dashboard/10000/items/${gadget.id}/properties/config`, {
  method: 'PUT',
  headers: {
    'Authorization': 'Bearer ' + accessToken,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    projectId: '10001',
    maxResults: 20,
    showSubtasks: true
  })
});
```

## Best Practices

### Dashboard Organization
- Use descriptive names that indicate purpose and audience
- Set appropriate share permissions to control access
- Organize gadgets logically with consistent positioning
- Limit dashboard count to avoid clutter

### Permission Management
- Use `extendAdminPermissions=true` only when necessary
- Prefer project-specific sharing over global sharing
- Regularly audit dashboard permissions
- Consider group-based sharing for team dashboards

### Gadget Configuration
- Store complex gadget settings in dashboard item properties
- Use consistent property key naming conventions
- Validate property values before storing
- Handle property size limits (32KB max)

### Performance Considerations
- Use pagination for dashboard lists
- Filter searches to reduce response size
- Cache dashboard metadata when possible
- Avoid frequent bulk operations

## Error Codes

### Common HTTP Status Codes
- **200 OK**: Successful request
- **201 Created**: Dashboard or gadget created successfully
- **204 No Content**: Successful deletion
- **400 Bad Request**: Invalid request parameters or body
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions (not dashboard owner)
- **404 Not Found**: Dashboard, gadget, or property not found

### Dashboard-Specific Errors
- Dashboard name already exists
- Invalid share permission configuration
- Gadget position conflicts
- Property key too long (>255 characters)
- Property value too large (>32KB)

## Related APIs
- [Issues API](issues-api.md) - For gadgets displaying issue data
- [Projects API](projects-api.md) - For project-specific dashboards
- [Filters API](filters-api.md) - For filter-based gadgets
- [Users API](users-api.md) - For user-specific dashboard sharing
