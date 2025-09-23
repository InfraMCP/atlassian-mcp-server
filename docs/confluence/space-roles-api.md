# Confluence Space Roles API (EAP)

## Overview
The Space Roles API provides operations for managing role-based access control in Confluence spaces. This API allows you to create custom roles, assign permissions to roles, and manage role assignments for users and groups. This is an Early Access Program (EAP) feature with experimental endpoints.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:space.permission:confluence` - Read space roles and assignments
  - `write:space.permission:confluence` - Create and manage role assignments
  - `write:configuration:confluence` - Create and manage space roles (admin only)

## Core Endpoints

### Get Available Space Roles (EAP)
Retrieve available space roles with filtering options.

**Endpoint:** `GET /wiki/api/v2/space-roles`

**Parameters:**
- `space-id` (string, optional) - Filter roles for specific space (if empty, returns all tenant roles)
- `role-type` (string, optional) - Filter by role type
- `principal-id` (string, optional) - Filter by principal ID (requires principal-type)
- `principal-type` (PrincipalType, optional) - Filter by principal type (requires principal-id)
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Permissions:** Permission to access Confluence site; for space-specific roles, permission to view the space

**Note:** This is an experimental EAP feature.

### Create Space Role
Create a new custom space role with specific permissions.

**Endpoint:** `POST /wiki/api/v2/space-roles`

**Request Body:**
- `name` (string, required) - Name of the space role
- `description` (string, required) - Description for the space role
- `spacePermissions` (array[string], required) - IDs of space permissions associated with the role

**Response:** 201 Created with role details

**Permissions:** User must be organization or site admin. Connect and Forge app users are not authorized.

**Note:** This is an experimental EAP feature.

### Get Space Role by ID
Retrieve a specific space role by its ID.

**Endpoint:** `GET /wiki/api/v2/space-roles/{id}`

**Parameters:**
- `id` (string, required) - Space role ID

**Response:** Space role details with permissions

### Update Space Role
Update an existing space role's properties and permissions.

**Endpoint:** `PUT /wiki/api/v2/space-roles/{id}`

**Parameters:**
- `id` (string, required) - Space role ID

**Request Body:** Updated role information and permissions

**Response:** 200 OK with updated role details

### Delete Space Role
Remove a space role from the system.

**Endpoint:** `DELETE /wiki/api/v2/space-roles/{id}`

**Parameters:**
- `id` (string, required) - Space role ID

**Response:** 204 No Content

## Role Assignment Endpoints

### Get Space Role Assignments (EAP)
Retrieve role assignments for a specific space.

**Endpoint:** `GET /wiki/api/v2/spaces/{id}/role-assignments`

**Parameters:**
- `id` (integer, required) - Space ID
- `role-id` (string, optional) - Filter by role ID
- `role-type` (string, optional) - Filter by role type
- `principal-id` (string, optional) - Filter by principal ID (requires principal-type)
- `principal-type` (PrincipalType, optional) - Filter by principal type (requires principal-id)
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Permissions:** Permission to view the space

**Note:** This is an experimental EAP feature.

### Set Space Role Assignments (EAP)
Create or update role assignments for a space.

**Endpoint:** `POST /wiki/api/v2/spaces/{id}/role-assignments`

**Parameters:**
- `id` (integer, required) - Space ID

**Request Body:** SetSpaceRoleAssignmentRequest with role assignments

**Response:** 200 OK with updated role assignments

**Size Limit:** Maximum 5 MB request size

**Permissions:** Permission to manage roles in the space

**Note:** This is an experimental EAP feature.

### Get Space Role Mode
Retrieve the current space role mode configuration.

**Endpoint:** `GET /wiki/api/v2/space-role-mode`

**Response:** Current role mode settings and configuration

## Example Usage

### Get Available Space Roles
```http
GET /wiki/api/v2/space-roles?space-id=123456789&limit=50
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "results": [
    {
      "id": "role123",
      "name": "Content Editor",
      "description": "Can create and edit content in the space",
      "type": "custom",
      "spacePermissions": [
        {
          "id": "perm1",
          "key": "read",
          "name": "View"
        },
        {
          "id": "perm2", 
          "key": "write",
          "name": "Create/Edit"
        }
      ],
      "createdAt": "2024-01-15T10:00:00.000Z"
    }
  ]
}
```

### Create Custom Space Role
```http
POST /wiki/api/v2/space-roles
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Content Reviewer",
  "description": "Can review and approve content changes",
  "spacePermissions": ["perm1", "perm2", "perm5"]
}
```

### Get Space Role Assignments
```http
GET /wiki/api/v2/spaces/123456789/role-assignments?role-type=custom&limit=25
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "results": [
    {
      "id": "assignment123",
      "principal": {
        "type": "user",
        "id": "user123",
        "displayName": "John Doe",
        "accountId": "5d5f9fbf-2d5b-4b5a-8b1a-1234567890ab"
      },
      "role": {
        "id": "role123",
        "name": "Content Editor",
        "type": "custom"
      },
      "assignedAt": "2024-01-15T10:00:00.000Z",
      "assignedBy": {
        "accountId": "admin123",
        "displayName": "Admin User"
      }
    }
  ]
}
```

### Set Role Assignments
```http
POST /wiki/api/v2/spaces/123456789/role-assignments
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "assignments": [
    {
      "principal": {
        "type": "user",
        "id": "user123"
      },
      "role": {
        "id": "role123"
      }
    },
    {
      "principal": {
        "type": "group",
        "id": "group456"
      },
      "role": {
        "id": "role789"
      }
    }
  ]
}
```

## Principal Types

### User Principals
```json
{
  "type": "user",
  "id": "user123",
  "displayName": "John Doe",
  "accountId": "5d5f9fbf-2d5b-4b5a-8b1a-1234567890ab"
}
```

### Group Principals
```json
{
  "type": "group",
  "id": "group123",
  "name": "confluence-users"
}
```

### Access Class Principals
Special principal types for system-wide access:
- `anonymous-users` - Anonymous/public access
- `authenticated-users` - All authenticated users
- `all-licensed-users` - All users with Confluence licenses
- `all-product-admins` - All product administrators
- `jsm-project-admins` - Jira Service Management project administrators

## Role Types
- **`system`** - Built-in system roles (e.g., Admin, User)
- **`custom`** - User-defined custom roles
- **`inherited`** - Roles inherited from parent spaces or groups

## Use Cases

### Custom Role Management
- **Department Roles:** Create roles specific to organizational departments
- **Project Roles:** Define roles for project-specific access patterns
- **Workflow Roles:** Create roles that match content workflow stages
- **Compliance Roles:** Define roles that meet regulatory requirements

### Access Control
- **Granular Permissions:** Assign specific permission combinations to roles
- **Role-Based Security:** Implement role-based access control patterns
- **Bulk Assignment:** Assign roles to multiple users or groups efficiently
- **Permission Auditing:** Track and audit role-based permissions

### Integration Scenarios
- **Identity Management:** Sync roles with external identity systems
- **Automated Provisioning:** Automatically assign roles based on user attributes
- **Workflow Integration:** Integrate role assignments with approval workflows
- **Compliance Reporting:** Generate role-based compliance reports

### Administrative Tools
- **Role Dashboards:** Build administrative interfaces for role management
- **Permission Planning:** Plan and model permission structures
- **Access Reviews:** Conduct periodic access reviews and cleanup
- **Role Analytics:** Analyze role usage and effectiveness

## Data Structure

### Space Role
```json
{
  "id": "role-id",
  "name": "Role Name",
  "description": "Role description",
  "type": "custom|system|inherited",
  "spacePermissions": [
    {
      "id": "permission-id",
      "key": "permission-key",
      "name": "Permission Name"
    }
  ],
  "createdAt": "2024-01-15T10:00:00.000Z",
  "updatedAt": "2024-01-15T12:00:00.000Z"
}
```

### Role Assignment
```json
{
  "id": "assignment-id",
  "principal": {
    "type": "user|group|access_class",
    "id": "principal-id",
    "displayName": "Principal Name"
  },
  "role": {
    "id": "role-id",
    "name": "Role Name",
    "type": "custom|system"
  },
  "assignedAt": "2024-01-15T10:00:00.000Z",
  "assignedBy": {
    "accountId": "assigner-id",
    "displayName": "Assigner Name"
  }
}
```

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Roles:** Permission to access Confluence site and view space
- **Create Roles:** Organization or site admin permissions required
- **Manage Assignments:** Permission to manage roles in the space
- **Admin Operations:** Connect and Forge apps are not authorized for role creation

## Error Handling
- **400 Bad Request:** Invalid role configuration, parameters, or assignments
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for role operations
- **404 Not Found:** Role, space, or assignment not found
- **413 Payload Too Large:** Request exceeds 5 MB size limit
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Names:** Choose clear, meaningful role names and descriptions
- **Principle of Least Privilege:** Assign minimal permissions necessary for role function
- **Regular Reviews:** Periodically review and audit role assignments
- **Document Roles:** Maintain documentation of role purposes and permissions
- **Test Permissions:** Verify role permissions work as expected before deployment
- **Monitor Usage:** Track role usage and effectiveness over time
- **Plan Hierarchy:** Design logical role hierarchies and inheritance patterns

## Important Notes
- **EAP Feature:** This is an experimental Early Access Program feature
- **Admin Requirements:** Role creation requires organization or site admin permissions
- **App Limitations:** Connect and Forge apps cannot create roles
- **Size Limits:** Role assignment requests are limited to 5 MB
- **Experimental Status:** API endpoints may change as the feature evolves
