# Confluence Space Permissions API

## Overview
The Space Permissions API provides read-only access to space permission assignments and available permission types in Confluence. This API allows you to understand who has access to spaces and what permissions are available for assignment.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:space:confluence` - Read space permission assignments
  - `read:space.permission:confluence` - Read available space permissions (EAP)

## Core Endpoints

### Get Space Permission Assignments
Retrieve permission assignments for a specific space.

**Endpoint:** `GET /wiki/api/v2/spaces/{id}/permissions`

**Parameters:**
- `id` (integer, required) - Space ID
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Response:** List of permission assignments with users, groups, and permissions

**Permissions:** Permission to view the space required

### Get Available Space Permissions (EAP)
Retrieve the list of available space permission types.

**Endpoint:** `GET /wiki/api/v2/space-permissions`

**Parameters:**
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Response:** List of available space permission types and descriptions

**Permissions:** Permission to access Confluence site required

**Note:** This is an experimental feature available only on EAP sites.

## Example Usage

### Get Space Permission Assignments
```http
GET /wiki/api/v2/spaces/123456789/permissions?limit=50
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "results": [
    {
      "id": "perm123",
      "principal": {
        "type": "user",
        "id": "user123",
        "displayName": "John Doe",
        "accountId": "5d5f9fbf-2d5b-4b5a-8b1a-1234567890ab"
      },
      "permission": {
        "key": "read",
        "name": "View",
        "description": "View pages and content in the space"
      },
      "grantedAt": "2024-01-15T10:00:00.000Z",
      "grantedBy": {
        "accountId": "admin123",
        "displayName": "Admin User"
      }
    },
    {
      "id": "perm456",
      "principal": {
        "type": "group",
        "id": "group123",
        "name": "confluence-users"
      },
      "permission": {
        "key": "write",
        "name": "Create/Edit",
        "description": "Create and edit pages in the space"
      },
      "grantedAt": "2024-01-15T10:00:00.000Z"
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/spaces/123456789/permissions?cursor=next_page_token"
  }
}
```

### Get Available Space Permissions (EAP)
```http
GET /wiki/api/v2/space-permissions?limit=25
Authorization: Bearer {access_token}
```

**Example Response:**
```json
{
  "results": [
    {
      "key": "read",
      "name": "View",
      "description": "View pages and content in the space",
      "category": "content"
    },
    {
      "key": "write",
      "name": "Create/Edit",
      "description": "Create and edit pages in the space",
      "category": "content"
    },
    {
      "key": "delete",
      "name": "Delete",
      "description": "Delete pages and content in the space",
      "category": "content"
    },
    {
      "key": "administer",
      "name": "Space Admin",
      "description": "Full administrative access to the space",
      "category": "administration"
    }
  ]
}
```

## Permission Types

### Content Permissions
- **`read`** - View pages and content in the space
- **`write`** - Create and edit pages in the space
- **`delete`** - Delete pages and content in the space
- **`export`** - Export space content
- **`comment`** - Add comments to pages

### Administrative Permissions
- **`administer`** - Full administrative access to the space
- **`restrict_read`** - Manage read restrictions on content
- **`restrict_write`** - Manage write restrictions on content

### Advanced Permissions
- **`archive`** - Archive and restore content
- **`purge`** - Permanently delete content
- **`move`** - Move content between spaces

## Principal Types

### User Principals
```json
{
  "type": "user",
  "id": "user123",
  "displayName": "John Doe",
  "accountId": "5d5f9fbf-2d5b-4b5a-8b1a-1234567890ab",
  "email": "john.doe@company.com"
}
```

### Group Principals
```json
{
  "type": "group",
  "id": "group123",
  "name": "confluence-users",
  "displayName": "Confluence Users"
}
```

### Anonymous Access
```json
{
  "type": "anonymous",
  "name": "anonymous"
}
```

## Use Cases

### Permission Auditing
- **Access Review:** Audit who has access to sensitive spaces
- **Compliance Reporting:** Generate reports on space access permissions
- **Security Analysis:** Identify overprivileged users or groups
- **Permission Cleanup:** Find and remove unnecessary permissions

### Access Management
- **User Onboarding:** Understand current permission structure for new users
- **Role Analysis:** Analyze permission patterns across spaces
- **Group Management:** Review group-based permission assignments
- **Permission Planning:** Plan permission changes based on current state

### Integration Scenarios
- **Identity Management:** Sync permissions with external identity systems
- **Automated Governance:** Monitor and alert on permission changes
- **Workflow Integration:** Include permission data in approval workflows
- **Analytics:** Analyze permission usage patterns and trends

### Administrative Tools
- **Permission Dashboards:** Build administrative dashboards for permission management
- **Bulk Operations:** Prepare data for bulk permission changes
- **Documentation:** Document current permission structure
- **Troubleshooting:** Diagnose access issues and permission conflicts

## Data Structure

### Permission Assignment
```json
{
  "id": "assignment-id",
  "principal": {
    "type": "user|group|anonymous",
    "id": "principal-id",
    "displayName": "Display Name",
    "accountId": "account-id"
  },
  "permission": {
    "key": "permission-key",
    "name": "Permission Name",
    "description": "Permission description"
  },
  "grantedAt": "2024-01-15T10:00:00.000Z",
  "grantedBy": {
    "accountId": "granter-account-id",
    "displayName": "Granter Name"
  }
}
```

### Space Permission
```json
{
  "key": "permission-key",
  "name": "Permission Name",
  "description": "Detailed permission description",
  "category": "content|administration|advanced"
}
```

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Space Permissions:** Permission to view the space required
- **View Available Permissions:** Basic Confluence site access required
- **No Write Operations:** This is a read-only API for permission discovery

## Error Handling
- **400 Bad Request:** Invalid parameters or malformed request
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions to view space permissions
- **404 Not Found:** Space not found or no permission to view
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Regular Auditing:** Periodically review space permissions for security
- **Cache Appropriately:** Cache permission data to reduce API calls
- **Monitor Changes:** Track permission changes over time
- **Document Permissions:** Maintain documentation of permission structure
- **Principle of Least Privilege:** Use permission data to enforce minimal access
- **Group Management:** Prefer group-based permissions over individual assignments
- **Compliance Tracking:** Use permission data for compliance and audit requirements

## Integration Patterns

### Permission Audit
```javascript
// Get all permission assignments for a space
const permissions = await getSpacePermissions(spaceId, { limit: 250 });

// Analyze user vs group permissions
const userPermissions = permissions.filter(p => p.principal.type === 'user');
const groupPermissions = permissions.filter(p => p.principal.type === 'group');

// Generate audit report
const auditReport = {
  spaceId: spaceId,
  totalAssignments: permissions.length,
  userAssignments: userPermissions.length,
  groupAssignments: groupPermissions.length,
  adminUsers: permissions.filter(p => p.permission.key === 'administer')
};
```

### Permission Analysis
```javascript
// Get available permissions for reference
const availablePermissions = await getAvailableSpacePermissions();

// Analyze permission distribution
const permissionCounts = permissions.reduce((acc, perm) => {
  acc[perm.permission.key] = (acc[perm.permission.key] || 0) + 1;
  return acc;
}, {});

// Identify potential security issues
const adminPermissions = permissions.filter(p => p.permission.key === 'administer');
const anonymousAccess = permissions.filter(p => p.principal.type === 'anonymous');
```

### Compliance Reporting
```javascript
// Generate compliance report
const complianceReport = {
  spaceId: spaceId,
  auditDate: new Date().toISOString(),
  permissions: permissions.map(p => ({
    principal: p.principal.displayName,
    principalType: p.principal.type,
    permission: p.permission.name,
    grantedAt: p.grantedAt,
    grantedBy: p.grantedBy?.displayName
  })),
  riskFactors: {
    hasAnonymousAccess: permissions.some(p => p.principal.type === 'anonymous'),
    adminCount: permissions.filter(p => p.permission.key === 'administer').length,
    externalUsers: permissions.filter(p => p.principal.email?.includes('@external.com')).length
  }
};
```
