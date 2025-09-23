# Fields API

## Overview
The Fields API provides comprehensive management of Jira fields, including system fields, custom fields, field contexts, and field options. This API enables OAuth 2.0 applications to discover available fields, create custom fields, manage field contexts, and configure field behavior across projects and issue types.

## OAuth 2.0 Scopes

### Required Scopes
- **`read:jira-work`** - Read field information and search fields
- **`manage:jira-configuration`** - Create, update, and manage custom fields and contexts

### Beta Scopes (Alternative)
- **`read:field:jira`** - Read field metadata and configurations
- **`write:field:jira`** - Create and update custom fields
- **`read:custom-field-contextual-configuration:jira`** - Read field context configurations

## Endpoints

### Field Discovery

#### GET /rest/api/3/field
**Description**: Get all system and custom fields visible to the user  
**OAuth Scopes**: `read:jira-work`  
**Parameters**: None

**Response**: Array of field details
```json
[
  {
    "id": "description",
    "name": "Description",
    "custom": false,
    "orderable": true,
    "navigable": true,
    "searchable": true,
    "clauseNames": ["description"],
    "schema": {
      "type": "string",
      "system": "description"
    }
  },
  {
    "id": "customfield_10101",
    "key": "customfield_10101",
    "name": "New custom field",
    "custom": true,
    "orderable": true,
    "navigable": true,
    "searchable": true,
    "clauseNames": ["cf[10101]", "New custom field"],
    "schema": {
      "type": "project",
      "custom": "com.atlassian.jira.plugin.system.customfieldtypes:project",
      "customId": 10101
    }
  }
]
```

**Use Case**: Discover all available fields for issue creation forms or search interfaces

#### GET /rest/api/3/field/search
**Description**: Search and paginate through fields with filtering options  
**OAuth Scopes**: `read:jira-work`  
**Parameters**:
- `startAt` (query, optional): Page offset (default: 0)
- `maxResults` (query, optional): Items per page (default: 50)
- `type` (query, optional): Field types to include (`custom`, `system`)
- `id` (query, optional): Specific field IDs to return
- `query` (query, optional): Search term for field names/descriptions
- `orderBy` (query, optional): Sort order (`name`, `contextsCount`, `lastUsed`, `screensCount`)
- `expand` (query, optional): Additional data (`key`, `lastUsed`, `contextsCount`, `screensCount`)
- `projectIds` (query, optional): Filter by project access

**Response**: Paginated field results
```json
{
  "startAt": 0,
  "maxResults": 50,
  "total": 2,
  "isLast": false,
  "values": [
    {
      "id": "customfield_10000",
      "name": "Approvers",
      "description": "Contains users needed for approval",
      "key": "customfield_10000",
      "stableId": "sfid:approvers",
      "isLocked": true,
      "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:userpickergroupsearcher",
      "schema": {
        "type": "array",
        "items": "user",
        "custom": "com.atlassian.jira.plugin.system.customfieldtypes:multiuserpicker",
        "customId": 10000
      },
      "screensCount": 2,
      "contextsCount": 2,
      "lastUsed": {
        "type": "TRACKED",
        "value": "2021-01-28T07:37:40.000+0000"
      }
    }
  ]
}
```

**Example**:
```bash
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/field/search?type=custom&query=approval&expand=contextsCount,lastUsed" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Custom Field Management

#### POST /rest/api/3/field
**Description**: Create a new custom field  
**OAuth Scopes**: `manage:jira-configuration`  
**Parameters**: None

**Request Body**:
```json
{
  "name": "New custom field",
  "description": "Custom field for picking groups",
  "type": "com.atlassian.jira.plugin.system.customfieldtypes:grouppicker",
  "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:grouppickersearcher"
}
```

**Response**: Created field details
```json
{
  "id": "customfield_10101",
  "key": "customfield_10101",
  "name": "New custom field",
  "custom": true,
  "orderable": true,
  "navigable": true,
  "searchable": true,
  "clauseNames": ["cf[10101]", "New custom field"],
  "schema": {
    "type": "project",
    "custom": "com.atlassian.jira.plugin.system.customfieldtypes:project",
    "customId": 10101
  },
  "untranslatedName": "New custom field"
}
```

**Error Codes**:
- `400` - Invalid field type, missing required properties, or insufficient permissions

**Common Field Types**:
- `com.atlassian.jira.plugin.system.customfieldtypes:textfield` - Single line text
- `com.atlassian.jira.plugin.system.customfieldtypes:textarea` - Multi-line text
- `com.atlassian.jira.plugin.system.customfieldtypes:select` - Single select dropdown
- `com.atlassian.jira.plugin.system.customfieldtypes:multiselect` - Multi-select dropdown
- `com.atlassian.jira.plugin.system.customfieldtypes:userpicker` - User picker
- `com.atlassian.jira.plugin.system.customfieldtypes:datepicker` - Date picker
- `com.atlassian.jira.plugin.system.customfieldtypes:float` - Number field

#### PUT /rest/api/3/field/{fieldId}
**Description**: Update an existing custom field  
**OAuth Scopes**: `manage:jira-configuration`  
**Parameters**:
- `fieldId` (path, required): Custom field ID

**Request Body**:
```json
{
  "name": "Updated field name",
  "description": "Updated field description",
  "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:cascadingselectsearcher"
}
```

**Response**: 204 No Content on success

**Error Codes**:
- `400` - Invalid searcher key for field type
- `403` - Insufficient permissions (requires Jira admin)
- `404` - Custom field not found

### Field Context Management

#### GET /rest/api/3/field/{fieldId}/context
**Description**: Get contexts for a custom field with filtering options  
**OAuth Scopes**: `manage:jira-configuration`  
**Parameters**:
- `fieldId` (path, required): Custom field ID
- `isAnyIssueType` (query, optional): Filter by issue type scope
- `isGlobalContext` (query, optional): Filter by project scope
- `contextId` (query, optional): Specific context IDs
- `startAt` (query, optional): Page offset
- `maxResults` (query, optional): Items per page

**Response**: Paginated context list
```json
{
  "startAt": 0,
  "maxResults": 100,
  "total": 2,
  "isLast": true,
  "values": [
    {
      "id": "10025",
      "name": "Bug fields context",
      "description": "A context used to define the custom field options for bugs.",
      "isGlobalContext": true,
      "isAnyIssueType": false
    },
    {
      "id": "10026",
      "name": "Task fields context",
      "description": "A context used to define the custom field options for tasks.",
      "isGlobalContext": false,
      "isAnyIssueType": false
    }
  ]
}
```

#### POST /rest/api/3/field/{fieldId}/context
**Description**: Create a new context for a custom field  
**OAuth Scopes**: `manage:jira-configuration`  
**Parameters**:
- `fieldId` (path, required): Custom field ID

**Request Body**:
```json
{
  "name": "Bug fields context",
  "description": "A context used to define the custom field options for bugs.",
  "projectIds": [],
  "issueTypeIds": ["10010"]
}
```

**Response**: Created context details
```json
{
  "id": "10025",
  "name": "Bug fields context",
  "description": "A context used to define the custom field options for bugs.",
  "projectIds": [],
  "issueTypeIds": ["10010"]
}
```

**Context Scope Rules**:
- **Global Context**: Empty `projectIds` array applies to all projects
- **Project-Specific**: Specific project IDs limit scope to those projects
- **All Issue Types**: Empty `issueTypeIds` array applies to all issue types
- **Issue Type-Specific**: Specific issue type IDs limit scope

**Error Codes**:
- `400` - Invalid request parameters
- `404` - Field, project, or issue type not found
- `409` - Issue type is sub-task but sub-tasks are disabled

## Use Cases

### Field Discovery for Forms
```javascript
// Get all fields for issue creation form
const fields = await fetch('/rest/api/3/field', {
  headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json());

// Separate system and custom fields
const systemFields = fields.filter(f => !f.custom);
const customFields = fields.filter(f => f.custom);

// Build form based on field types
customFields.forEach(field => {
  if (field.schema.type === 'string') {
    // Create text input
  } else if (field.schema.type === 'option') {
    // Create dropdown - need to fetch options
  }
});
```

### Custom Field Creation Workflow
```javascript
// 1. Create custom field
const newField = await fetch('/rest/api/3/field', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Priority Level',
    description: 'Custom priority classification',
    type: 'com.atlassian.jira.plugin.system.customfieldtypes:select',
    searcherKey: 'com.atlassian.jira.plugin.system.customfieldtypes:multiselectsearcher'
  })
}).then(r => r.json());

// 2. Create context for specific projects
const context = await fetch(`/rest/api/3/field/${newField.id}/context`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Development Projects Context',
    description: 'Priority levels for development projects',
    projectIds: ['10001', '10002'],
    issueTypeIds: ['10004', '10005'] // Bug, Task
  })
}).then(r => r.json());

console.log(`Created field ${newField.id} with context ${context.id}`);
```

### Field Search and Analysis
```javascript
// Search for unused custom fields
const searchResults = await fetch('/rest/api/3/field/search?type=custom&expand=lastUsed,contextsCount&orderBy=lastUsed', {
  headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json());

// Find fields that haven't been used recently
const unusedFields = searchResults.values.filter(field => 
  field.lastUsed?.type === 'NOT_TRACKED' || 
  !field.lastUsed?.value ||
  new Date(field.lastUsed.value) < new Date('2023-01-01')
);

console.log(`Found ${unusedFields.length} potentially unused fields`);
```

## Best Practices

### Field Management
- **Use descriptive names**: Field names appear in UI and JQL queries
- **Set appropriate searchers**: Match searcher to field type for optimal search experience
- **Plan contexts carefully**: Contexts determine where fields appear and their configuration
- **Monitor field usage**: Use `lastUsed` data to identify unused fields

### Context Design
- **Start with global contexts**: Easier to manage, apply to all projects
- **Use project-specific contexts**: When field behavior differs between projects
- **Group related issue types**: Create contexts for logical issue type groupings
- **Avoid context proliferation**: Too many contexts become difficult to manage

### Performance Considerations
- **Use pagination**: Field search can return many results
- **Filter by project**: Reduce results to relevant fields only
- **Expand selectively**: Only request additional data when needed
- **Cache field metadata**: Field definitions change infrequently

### Permission Handling
- **Check admin permissions**: Most field management requires Jira admin rights
- **Graceful degradation**: Handle permission errors appropriately
- **Validate field access**: Users may not see all fields due to project permissions

## Error Handling

### Common Error Patterns
```javascript
async function createCustomField(fieldData) {
  try {
    const response = await fetch('/rest/api/3/field', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(fieldData)
    });
    
    if (response.status === 400) {
      const error = await response.json();
      throw new Error(`Invalid field configuration: ${error.errorMessages?.join(', ')}`);
    }
    
    if (response.status === 403) {
      throw new Error('Insufficient permissions - Jira admin required');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Field creation failed:', error.message);
    throw error;
  }
}
```

## Field Type Reference

### Common Custom Field Types
| Type | Description | Searcher |
|------|-------------|----------|
| `textfield` | Single line text | `textsearcher` |
| `textarea` | Multi-line text | `textsearcher` |
| `select` | Single select dropdown | `multiselectsearcher` |
| `multiselect` | Multi-select dropdown | `multiselectsearcher` |
| `radiobuttons` | Radio button group | `multiselectsearcher` |
| `checkboxes` | Checkbox group | `multiselectsearcher` |
| `userpicker` | Single user picker | `userpickergroupsearcher` |
| `multiuserpicker` | Multi-user picker | `userpickergroupsearcher` |
| `grouppicker` | Single group picker | `grouppickersearcher` |
| `multigrouppicker` | Multi-group picker | `grouppickersearcher` |
| `datepicker` | Date picker | `daterange` |
| `datetime` | Date and time picker | `datetimerange` |
| `float` | Number field | `exactnumber` |
| `url` | URL field | `exacttextsearcher` |

## Related APIs
- **[Issues API](issues-api.md)** - Field values in issue creation and updates
- **[Search API](search-api.md)** - JQL queries using field clause names
- **[Projects API](projects-api.md)** - Project-specific field contexts
- **[Screens API](screens-api.md)** - Field placement on issue screens
