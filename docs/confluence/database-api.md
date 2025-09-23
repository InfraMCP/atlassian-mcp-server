# Confluence Database API

## Overview
The Database API provides operations for managing Confluence databases - structured data tables that can store and organize information within Confluence spaces. Databases support collaborative data management with permissions, properties, and hierarchical relationships.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:database:confluence` - Read database content and metadata
  - `write:database:confluence` - Create databases
  - `delete:database:confluence` - Delete databases

## Core Endpoints

### Create Database
Create a new database in a Confluence space.

**Endpoint:** `POST /wiki/api/v2/databases`

**Parameters:**
- `private` (boolean, default: false) - Create private database (only creator has access)

**Request Body:** DatabaseCreateRequest
- Must specify space and database configuration
- Supports structured data schema definition

**Response:** 200 OK with created database details

**Size Limit:** Maximum 5 MB request size

### Get Database by ID
Retrieve a specific database with optional metadata.

**Endpoint:** `GET /wiki/api/v2/databases/{id}`

**Parameters:**
- `id` (integer, required) - Database ID
- `include-collaborators` (boolean, default: false) - Include collaborators
- `include-direct-children` (boolean, default: false) - Include direct children
- `include-operations` (boolean, default: false) - Include available operations (max 50)
- `include-properties` (boolean, default: false) - Include content properties (max 50)

**Response:** Database details with optional metadata

### Delete Database
Delete a database (moves to trash, can be restored).

**Endpoint:** `DELETE /wiki/api/v2/databases/{id}`

**Response:** 204 No Content (database moved to trash)

## Related Endpoints

### Database Properties
Manage custom properties attached to databases:

- `GET /wiki/api/v2/databases/{id}/properties` - Get database properties
- `POST /wiki/api/v2/databases/{id}/properties` - Create property
- `GET /wiki/api/v2/databases/{database-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/databases/{database-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/databases/{database-id}/properties/{property-id}` - Delete property

### Database Operations
- `GET /wiki/api/v2/databases/{id}/operations` - Get available operations

### Database Hierarchy
- `GET /wiki/api/v2/databases/{id}/direct-children` - Get direct children
- `GET /wiki/api/v2/databases/{id}/descendants` - Get all descendants
- `GET /wiki/api/v2/databases/{id}/ancestors` - Get ancestors

### Database Classification
- `GET /wiki/api/v2/databases/{id}/classification-level` - Get classification level
- `PUT /wiki/api/v2/databases/{id}/classification-level` - Set classification level
- `POST /wiki/api/v2/databases/{id}/classification-level/reset` - Reset classification

## Example Usage

### Create Database
```http
POST /wiki/api/v2/databases?private=false
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "spaceId": "123456789",
  "title": "Project Tracker",
  "description": "Database for tracking project tasks and milestones"
}
```

### Get Database with Metadata
```http
GET /wiki/api/v2/databases/987654321?include-collaborators=true&include-properties=true
Authorization: Bearer {access_token}
```

### Create Database Property
```http
POST /wiki/api/v2/databases/987654321/properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "schema-version",
  "value": {
    "version": "1.0",
    "lastUpdated": "2024-01-15",
    "fields": ["name", "status", "priority", "assignee"]
  }
}
```

## Use Cases

### Data Management
- **Project Tracking:** Create databases for project tasks, milestones, and resources
- **Inventory Management:** Track assets, equipment, or resources
- **Contact Management:** Store and organize contact information
- **Knowledge Base:** Structure FAQ, documentation, or reference data

### Collaboration
- **Team Dashboards:** Create shared data views for team metrics
- **Resource Planning:** Manage shared resources and scheduling
- **Decision Tracking:** Record decisions, outcomes, and follow-ups
- **Process Management:** Track workflow states and process data

### Integration Scenarios
- **External Data Import:** Import structured data from external systems
- **Reporting:** Create data sources for reports and analytics
- **Configuration Management:** Store application or system configuration data
- **Audit Trails:** Maintain structured logs and audit information

## Database Features
- **Structured Data:** Support for typed columns and data validation
- **Collaborative Editing:** Multiple users can edit database content
- **Permissions:** Fine-grained access control at database level
- **Properties:** Attach custom metadata to databases
- **Hierarchical:** Support parent-child relationships between databases
- **Classification:** Security classification and data governance support

## Privacy Options
- **Public Databases:** Visible to all space members with appropriate permissions
- **Private Databases:** Only visible to creator, useful for personal data organization

## Permissions
- **View Database:** Permission to view the database and its space
- **Create Database:** Permission to create databases in the space
- **Edit Database:** Permission to modify database content and structure
- **Delete Database:** Permission to delete databases in the space
- **Manage Properties:** Permission to manage database properties and metadata

## Error Handling
- **400 Bad Request:** Invalid database configuration or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for database operations
- **404 Not Found:** Database or space not found
- **413 Payload Too Large:** Request exceeds 5 MB size limit
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Names:** Choose clear, meaningful database titles
- **Set Appropriate Privacy:** Use private databases for personal data, public for shared data
- **Manage Properties:** Use properties to store schema information and metadata
- **Handle Permissions:** Ensure proper space and database permissions before operations
- **Structure Data:** Design clear column structures and data types
- **Regular Cleanup:** Remove unused databases to avoid clutter
- **Classification:** Apply appropriate security classifications for sensitive data
