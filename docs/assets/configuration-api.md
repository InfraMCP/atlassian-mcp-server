# Assets Configuration API (v1)

The Assets Configuration API provides management capabilities for system configuration, status types, icons, and global settings within Assets workspaces.

## Base URL Structure

All Assets API endpoints follow this pattern:
```
https://api.atlassian.com/jsm/assets/workspace/{workspaceId}/v1/{endpoint}
```

## OAuth 2.0 Scopes Required

### Configuration Operations
- **`read:cmdb-schema:jira`** - Read configuration settings
- **`write:cmdb-schema:jira`** - Modify configuration settings
- **`manage:cmdb-schema:jira`** - Full configuration management

## Status Type Configuration

### List Status Types

**GET** `/config/statustype`

Retrieve all available status types for objects in the workspace.

**Response Example:**
```json
{
  "values": [
    {
      "id": "1",
      "name": "Active",
      "description": "Object is currently active and in use",
      "category": "ACTIVE",
      "color": "#36B37E"
    },
    {
      "id": "2", 
      "name": "Inactive",
      "description": "Object is not currently in use",
      "category": "INACTIVE",
      "color": "#FF5630"
    }
  ]
}
```

### Get Status Type

**GET** `/config/statustype/{id}`

Retrieve details of a specific status type.

**Parameters:**
- `id` (path, required): The status type ID

**Response Example:**
```json
{
  "id": "1",
  "name": "Active",
  "description": "Object is currently active and in use",
  "category": "ACTIVE",
  "color": "#36B37E",
  "created": "2021-02-16T18:04:31.284Z",
  "updated": "2021-02-16T18:04:31.288Z"
}
```

## Icon Management

### List Global Icons

**GET** `/icon/global`

Retrieve all available global icons that can be used for object types.

**Response Example:**
```json
{
  "values": [
    {
      "id": "1",
      "name": "Computer",
      "url16": "https://api.atlassian.com/.../icon.png?size=16",
      "url48": "https://api.atlassian.com/.../icon.png?size=48"
    },
    {
      "id": "2",
      "name": "Server",
      "url16": "https://api.atlassian.com/.../icon.png?size=16",
      "url48": "https://api.atlassian.com/.../icon.png?size=48"
    }
  ]
}
```

### Get Icon

**GET** `/icon/{id}`

Retrieve details of a specific icon.

**Parameters:**
- `id` (path, required): The icon ID

### Get Icon Image

**GET** `/icon/{id}/icon.png`

Retrieve the actual icon image file.

**Parameters:**
- `id` (path, required): The icon ID

**Query Parameters:**
- `size` (integer): Icon size (16, 48, 72, 144, 288)

## Global Configuration

### Get Schema Properties

**GET** `/global/config/objectschema/{id}/property`

Retrieve global configuration properties for a specific object schema.

**Parameters:**
- `id` (path, required): The object schema ID

**Response Example:**
```json
{
  "properties": [
    {
      "key": "jira.integration.enabled",
      "value": "true",
      "description": "Enable Jira integration for this schema"
    },
    {
      "key": "auto.numbering.enabled", 
      "value": "false",
      "description": "Enable automatic object key numbering"
    }
  ]
}
```

## Status Type Categories

Status types are organized into predefined categories:

- **`ACTIVE`** - Objects that are currently in use
- **`INACTIVE`** - Objects that are not currently active
- **`MAINTENANCE`** - Objects undergoing maintenance
- **`RETIRED`** - Objects that have been retired
- **`PENDING`** - Objects awaiting activation or approval
- **`ERROR`** - Objects with error conditions

## Icon Sizes

Icons are available in multiple sizes:

- **16x16** - Small icons for lists and compact views
- **48x48** - Medium icons for cards and detailed views  
- **72x72** - Large icons for headers
- **144x144** - Extra large icons for detailed displays
- **288x288** - Maximum size for high-resolution displays

## Configuration Properties

Common schema configuration properties:

### Jira Integration
- `jira.integration.enabled` - Enable/disable Jira integration
- `jira.project.key` - Default Jira project for linked issues
- `jira.issue.type` - Default issue type for created tickets

### Object Management
- `auto.numbering.enabled` - Enable automatic object key generation
- `auto.numbering.pattern` - Pattern for generated object keys
- `duplicate.detection.enabled` - Enable duplicate object detection

### Display Settings
- `default.view.mode` - Default view mode (list, card, tree)
- `show.empty.attributes` - Show attributes with no values
- `attribute.grouping.enabled` - Group attributes by category

### Security Settings
- `public.access.enabled` - Allow public access to schema
- `external.sharing.enabled` - Allow sharing with external users
- `audit.logging.enabled` - Enable detailed audit logging

## Response Codes

- **200** - Success
- **400** - Bad Request - Invalid parameters
- **401** - Unauthorized - Authentication required
- **403** - Forbidden - Insufficient permissions
- **404** - Not Found - Configuration item not found
- **500** - Internal Server Error

## Implementation Notes

- **Status Types** are workspace-wide and shared across all schemas
- **Icons** can be global (system-provided) or custom (user-uploaded)
- **Configuration Properties** are schema-specific
- **Color Values** use standard hex color codes (#RRGGBB)
- **Icon URLs** include size parameters for responsive display
- **Property Keys** follow dot notation convention
- **Boolean Values** are stored as strings ("true"/"false")
- **Changes** to configuration may require schema refresh
- **Permissions** are required for modifying configuration settings
