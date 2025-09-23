# Confluence Space API

## Overview
The Space API provides operations for managing Confluence spaces - the primary organizational containers for content. Spaces group related pages, blog posts, and other content together with shared permissions, settings, and branding.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:space:confluence` - Read space information and metadata
  - `write:space:confluence` - Create spaces (EAP feature)

## Core Endpoints

### Get All Spaces
Retrieve spaces with comprehensive filtering and pagination.

**Endpoint:** `GET /wiki/api/v2/spaces`

**Parameters:**
- `ids` (array[integer], optional) - Filter by space IDs (max 250)
- `keys` (array[string], optional) - Filter by space keys (max 250)
- `type` (string, optional) - Filter by type: `global`, `collaboration`, `knowledge_base`, `personal`
- `status` (string, optional) - Filter by status: `current`, `archived`
- `labels` (array[string], optional) - Filter by space labels
- `favorited-by` (string, optional) - Filter by user account ID who favorited
- `not-favorited-by` (string, optional) - Filter by user account ID who did NOT favorite
- `sort` (SpaceSortOrder, optional) - Sort order for results
- `description-format` (SpaceDescriptionBodyRepresentation, optional) - Description format
- `include-icon` (boolean, default: false) - Include space icon
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Permissions:** Global 'Can use' permission. Only returns spaces user can view.

### Create Space (EAP)
Create a new space (Early Access Program feature).

**Endpoint:** `POST /wiki/api/v2/spaces`

**Request Body:** SpaceCreateRequest
- Must specify space key, name, and type
- Supports various space configurations

**Response:** 201 Created with space details

**Size Limit:** Maximum 5 MB request size

**Note:** This is an experimental feature available only on EAP sites.

### Get Space by ID
Retrieve a specific space with optional metadata.

**Endpoint:** `GET /wiki/api/v2/spaces/{id}`

**Parameters:**
- `id` (integer, required) - Space ID
- `description-format` (SpaceDescriptionBodyRepresentation, optional) - Description format
- `include-icon` (boolean, default: false) - Include space icon
- `include-operations` (boolean, default: false) - Include available operations (max 50)
- `include-properties` (boolean, default: false) - Include space properties (max 50)
- `include-permissions` (boolean, default: false) - Include space permissions (max 50)
- `include-role-assignments` (boolean, default: false) - Include role assignments (EAP only, max 50)
- `include-labels` (boolean, default: false) - Include space labels (max 50)

## Content-Specific Endpoints

### Get Space Content
Retrieve content within specific spaces:

- `GET /wiki/api/v2/spaces/{id}/pages` - Get space pages
- `GET /wiki/api/v2/spaces/{id}/blogposts` - Get space blog posts
- `GET /wiki/api/v2/spaces/{id}/custom-content` - Get space custom content

### Get Space Labels
- `GET /wiki/api/v2/spaces/{id}/labels` - Get space labels
- `GET /wiki/api/v2/spaces/{id}/content/labels` - Get all content labels in space

## Space Management Endpoints

### Space Properties
- `GET /wiki/api/v2/spaces/{space-id}/properties` - Get space properties
- `POST /wiki/api/v2/spaces/{space-id}/properties` - Create property
- `GET /wiki/api/v2/spaces/{space-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/spaces/{space-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/spaces/{space-id}/properties/{property-id}` - Delete property

### Space Permissions
- `GET /wiki/api/v2/spaces/{id}/permissions` - Get space permissions

### Space Role Assignments (EAP)
- `GET /wiki/api/v2/spaces/{id}/role-assignments` - Get role assignments
- `POST /wiki/api/v2/spaces/{id}/role-assignments` - Create role assignment

### Space Operations
- `GET /wiki/api/v2/spaces/{id}/operations` - Get permitted operations

### Space Classification
- `GET /wiki/api/v2/spaces/{id}/classification-level/default` - Get default classification
- `PUT /wiki/api/v2/spaces/{id}/classification-level/default` - Set default classification
- `DELETE /wiki/api/v2/spaces/{id}/classification-level/default` - Remove default classification

## Example Usage

### Get All Spaces with Filtering
```http
GET /wiki/api/v2/spaces?type=collaboration&status=current&include-icon=true&limit=50
Authorization: Bearer {access_token}
```

### Create Space (EAP)
```http
POST /wiki/api/v2/spaces
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "PROJ",
  "name": "Project Documentation",
  "type": "collaboration",
  "description": {
    "representation": "storage",
    "value": "<p>Space for project documentation and collaboration</p>"
  }
}
```

### Get Space with Full Metadata
```http
GET /wiki/api/v2/spaces/123456789?include-properties=true&include-permissions=true&include-labels=true&include-operations=true
Authorization: Bearer {access_token}
```

### Get Space Content
```http
GET /wiki/api/v2/spaces/123456789/pages?limit=25&sort=title
Authorization: Bearer {access_token}
```

### Create Space Property
```http
POST /wiki/api/v2/spaces/123456789/properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "space-config",
  "value": {
    "theme": "corporate",
    "defaultPageTemplate": "meeting-notes",
    "autoArchive": false
  }
}
```

## Example Response
```json
{
  "results": [
    {
      "id": "123456789",
      "key": "PROJ",
      "name": "Project Documentation",
      "type": "collaboration",
      "status": "current",
      "description": {
        "storage": {
          "value": "<p>Space for project documentation</p>",
          "representation": "storage"
        }
      },
      "homepage": {
        "id": "987654321",
        "title": "Project Home"
      },
      "createdAt": "2024-01-15T10:00:00.000Z",
      "_links": {
        "webui": "/spaces/PROJ",
        "self": "/wiki/api/v2/spaces/123456789"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/spaces?cursor=next_page_token"
  }
}
```

## Use Cases

### Space Discovery
- **Space Browsing:** Find spaces by type, status, or labels
- **Favorite Management:** Filter by user favorites for personalized views
- **Content Organization:** Understand space structure and organization
- **Access Auditing:** Review space permissions and access levels

### Space Management
- **Space Creation:** Create new collaboration or knowledge base spaces
- **Configuration:** Manage space properties and settings
- **Permission Management:** Control access and role assignments
- **Content Organization:** Organize content within space hierarchies

### Integration Scenarios
- **Content Migration:** Discover and migrate content between spaces
- **Automated Organization:** Create spaces programmatically for projects
- **Analytics:** Analyze space usage and content distribution
- **Workflow Integration:** Connect spaces to business processes

### Collaboration
- **Team Workspaces:** Create dedicated spaces for team collaboration
- **Project Spaces:** Organize project-related content and documentation
- **Knowledge Management:** Structure organizational knowledge by topic
- **Department Organization:** Create departmental information hubs

## Space Types
- **`global`** - Site-wide spaces for general information
- **`collaboration`** - Team and project collaboration spaces
- **`knowledge_base`** - Structured knowledge and documentation spaces
- **`personal`** - Individual user spaces for personal content

## Space Status
- **`current`** - Active spaces available for use
- **`archived`** - Archived spaces (read-only, preserved for reference)

## Space Features
- **Content Organization:** Hierarchical organization of pages and content
- **Permission Management:** Granular access control and role-based permissions
- **Branding:** Custom themes, logos, and visual identity
- **Properties:** Custom metadata and configuration storage
- **Labels:** Categorization and tagging for organization
- **Homepage:** Dedicated landing page for space navigation
- **Templates:** Page and content templates for consistency

## Permissions
- **View Space:** Permission to view the space and its content
- **Create Space:** Global permission to create new spaces
- **Administer Space:** Full administrative access to space settings
- **Manage Permissions:** Ability to modify space permissions and roles
- **Manage Properties:** Permission to manage space properties and metadata

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request
- Results sorted by ID ascending by default

## Error Handling
- **400 Bad Request:** Invalid space configuration, parameters, or filters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for space operations
- **404 Not Found:** Space not found or no permission to view
- **413 Payload Too Large:** Request exceeds 5 MB size limit (create operations)
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Keys:** Choose meaningful, consistent space keys
- **Organize by Purpose:** Use appropriate space types for intended use
- **Manage Permissions:** Implement proper access control for sensitive content
- **Leverage Properties:** Use properties for space configuration and metadata
- **Regular Maintenance:** Review and update space settings periodically
- **Label Consistently:** Use consistent labeling for space categorization
- **Monitor Usage:** Track space activity and content growth
- **Plan Hierarchy:** Design logical space organization before creation
