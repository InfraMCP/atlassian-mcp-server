# Confluence Folder API

## Overview
The Folder API provides operations for managing folders in Confluence spaces. Folders help organize content hierarchically, allowing users to group related pages, databases, and other content types in a structured manner.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:folder:confluence` - Read folder content and metadata
  - `write:folder:confluence` - Create folders
  - `delete:folder:confluence` - Delete folders

## Core Endpoints

### Create Folder
Create a new folder in a Confluence space.

**Endpoint:** `POST /wiki/api/v2/folders`

**Request Body:** FolderCreateRequest
- Must specify space and folder configuration
- Supports hierarchical placement within content tree

**Response:** 200 OK with created folder details

**Size Limit:** Maximum 5 MB request size

### Get Folder by ID
Retrieve a specific folder with optional metadata.

**Endpoint:** `GET /wiki/api/v2/folders/{id}`

**Parameters:**
- `id` (integer, required) - Folder ID
- `include-collaborators` (boolean, default: false) - Include collaborators
- `include-direct-children` (boolean, default: false) - Include direct children
- `include-operations` (boolean, default: false) - Include available operations (max 50)
- `include-properties` (boolean, default: false) - Include content properties (max 50)

**Response:** Folder details with optional metadata

### Delete Folder
Delete a folder (moves to trash, can be restored).

**Endpoint:** `DELETE /wiki/api/v2/folders/{id}`

**Response:** 204 No Content (folder moved to trash)

## Related Endpoints

### Folder Properties
Manage custom properties attached to folders:

- `GET /wiki/api/v2/folders/{id}/properties` - Get folder properties
- `POST /wiki/api/v2/folders/{id}/properties` - Create property
- `GET /wiki/api/v2/folders/{folder-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/folders/{folder-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/folders/{folder-id}/properties/{property-id}` - Delete property

### Folder Operations
- `GET /wiki/api/v2/folders/{id}/operations` - Get available operations

### Folder Hierarchy
- `GET /wiki/api/v2/folders/{id}/direct-children` - Get direct children
- `GET /wiki/api/v2/folders/{id}/descendants` - Get all descendants
- `GET /wiki/api/v2/folders/{id}/ancestors` - Get ancestors

## Example Usage

### Create Folder
```http
POST /wiki/api/v2/folders
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "spaceId": "123456789",
  "title": "Project Documentation",
  "description": "Folder containing all project-related documentation"
}
```

### Get Folder with Children
```http
GET /wiki/api/v2/folders/987654321?include-direct-children=true&include-properties=true
Authorization: Bearer {access_token}
```

### Create Folder Property
```http
POST /wiki/api/v2/folders/987654321/properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "folder-metadata",
  "value": {
    "category": "documentation",
    "owner": "project-team",
    "lastReview": "2024-01-15"
  }
}
```

## Use Cases

### Content Organization
- **Project Structure:** Organize project-related content in logical hierarchies
- **Department Folders:** Create departmental content organization
- **Topic Grouping:** Group related documentation by subject or theme
- **Archive Organization:** Structure historical or reference content

### Collaboration
- **Team Workspaces:** Create dedicated folders for team collaboration
- **Process Documentation:** Organize procedures and workflows
- **Resource Libraries:** Structure shared resources and templates
- **Knowledge Management:** Organize institutional knowledge and best practices

### Integration Scenarios
- **Content Migration:** Organize imported content from external systems
- **Automated Organization:** Create folder structures programmatically
- **Workflow Management:** Use folders to represent workflow stages
- **Access Control:** Leverage folder hierarchy for permission management

## Folder Features
- **Hierarchical Organization:** Support nested folder structures
- **Content Grouping:** Can contain pages, databases, and other content types
- **Collaborative:** Multiple users can access and organize content
- **Properties:** Attach custom metadata to folders
- **Permissions:** Inherit and manage access control through hierarchy
- **Trash Recovery:** Deleted folders can be restored from trash

## Permissions
- **View Folder:** Permission to view the folder and its space
- **Create Folder:** Permission to create folders in the space
- **Edit Folder:** Permission to modify folder properties and structure
- **Delete Folder:** Permission to delete folders in the space
- **Manage Properties:** Permission to manage folder properties and metadata

## Error Handling
- **400 Bad Request:** Invalid folder configuration or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for folder operations
- **404 Not Found:** Folder or space not found
- **413 Payload Too Large:** Request exceeds 5 MB size limit
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Names:** Choose clear, meaningful folder titles
- **Plan Hierarchy:** Design logical folder structures before creation
- **Manage Properties:** Use properties to store organizational metadata
- **Handle Permissions:** Ensure proper space and folder permissions
- **Regular Maintenance:** Review and reorganize folder structures periodically
- **Avoid Deep Nesting:** Keep folder hierarchies reasonably shallow for usability
- **Document Structure:** Use folder descriptions to explain organizational logic
