# Assets Schemas API (v1)

The Assets Schemas API provides management capabilities for object schemas, object types, and their attributes within Assets workspaces. Schemas define the structure and organization of your Assets data.

## Base URL Structure

All Assets API endpoints follow this pattern:
```
https://api.atlassian.com/jsm/assets/workspace/{workspaceId}/v1/{endpoint}
```

## OAuth 2.0 Scopes Required

### Schema Operations
- **`read:cmdb-schema:jira`** - Read schemas, object types, and attributes
- **`write:cmdb-schema:jira`** - Create and update schemas and object types
- **`delete:cmdb-schema:jira`** - Delete schemas and object types

## Object Schema Operations

### List Object Schemas

**GET** `/objectschema/list`

Retrieve all object schemas in the workspace with pagination support.

**Query Parameters:**
- `startAt` (integer, default: 0): Starting index for pagination
- `maxResults` (integer, default: 25): Maximum number of schemas to return
- `includeCounts` (boolean, default: false): Include object and object type counts

**Response Example:**
```json
{
  "startAt": 0,
  "maxResults": 25,
  "total": 5,
  "isLast": true,
  "values": [
    {
      "workspaceId": "g2778e1d-939d-581d-c8e2-9d5g59de456b",
      "globalId": "g2778e1d-939d-581d-c8e2-9d5g59de456b:6",
      "id": "6",
      "name": "ITSM",
      "objectSchemaKey": "ITSM",
      "status": "Ok",
      "created": "2021-02-16T18:04:31.284Z",
      "updated": "2021-02-16T18:04:31.288Z",
      "objectCount": 95,
      "objectTypeCount": 34,
      "canManage": true
    }
  ]
}
```

### Get Object Schema

**GET** `/objectschema/{id}`

Retrieve details of a specific object schema.

**Parameters:**
- `id` (path, required): The object schema ID

### Create Object Schema

**POST** `/objectschema/create`

Create a new object schema in the workspace.

**Request Body:**
```json
{
  "name": "IT Assets",
  "objectSchemaKey": "ITA",
  "description": "Schema for managing IT assets and infrastructure"
}
```

### Get Schema Attributes

**GET** `/objectschema/{id}/attributes`

Get all attributes defined across all object types in a schema.

**Parameters:**
- `id` (path, required): The object schema ID

### Get Schema Object Types

**GET** `/objectschema/{id}/objecttypes`

Get all object types in a schema with hierarchical structure.

**Parameters:**
- `id` (path, required): The object schema ID

### Get Schema Object Types (Flat)

**GET** `/objectschema/{id}/objecttypes/flat`

Get all object types in a schema as a flat list without hierarchy.

**Parameters:**
- `id` (path, required): The object schema ID

## Object Type Operations

### Get Object Type

**GET** `/objecttype/{id}`

Retrieve details of a specific object type.

**Parameters:**
- `id` (path, required): The object type ID

**Response Example:**
```json
{
  "workspaceId": "f1668d0c-828c-470c-b7d1-8c4f48cd345a",
  "globalId": "f1668d0c-828c-470c-b7d1-8c4f48cd345a:23",
  "id": "23",
  "name": "Computer",
  "description": "Desktop and laptop computers",
  "icon": {
    "id": "13",
    "name": "Computer",
    "url16": "https://api.atlassian.com/.../icon.png?size=16"
  },
  "position": 2,
  "created": "2021-02-16T19:36:51.951Z",
  "updated": "2021-04-16T15:17:03.384Z",
  "objectCount": 150,
  "objectSchemaId": "6",
  "inherited": false,
  "abstractObjectType": false,
  "parentObjectTypeInherited": false
}
```

### Create Object Type

**POST** `/objecttype/create`

Create a new object type within a schema.

**Request Body:**
```json
{
  "name": "Server",
  "description": "Physical and virtual servers",
  "iconId": "15",
  "objectSchemaId": "6",
  "parentObjectTypeId": "1",
  "inherited": false,
  "abstractObjectType": false
}
```

### Get Object Type Attributes

**GET** `/objecttype/{id}/attributes`

Get all attributes defined for a specific object type.

**Parameters:**
- `id` (path, required): The object type ID

### Update Object Type Position

**PUT** `/objecttype/{id}/position`

Update the position/order of an object type within its schema.

**Parameters:**
- `id` (path, required): The object type ID

**Request Body:**
```json
{
  "position": 5
}
```

## Object Type Attribute Operations

### Get Object Type Attribute

**GET** `/objecttypeattribute/{id}`

Retrieve details of a specific object type attribute.

**Parameters:**
- `id` (path, required): The object type attribute ID

### List Object Type Attributes

**GET** `/objecttypeattribute/{objectTypeId}`

Get all attributes for a specific object type.

**Parameters:**
- `objectTypeId` (path, required): The object type ID

### Get Specific Attribute

**GET** `/objecttypeattribute/{objectTypeId}/{id}`

Get a specific attribute within an object type.

**Parameters:**
- `objectTypeId` (path, required): The object type ID
- `id` (path, required): The attribute ID

## Global Configuration

### Get Schema Properties

**GET** `/global/config/objectschema/{id}/property`

Get global configuration properties for a schema.

**Parameters:**
- `id` (path, required): The object schema ID

## Schema Status Types

Object schemas can have the following status values:
- **`Ok`** - Schema is active and functioning normally
- **`Inactive`** - Schema is temporarily disabled
- **`Error`** - Schema has configuration errors

## Object Type Hierarchy

Object types support inheritance and hierarchical relationships:

- **Parent-Child Relationships**: Object types can inherit from parent types
- **Abstract Types**: Can serve as templates but cannot have direct instances
- **Inherited Attributes**: Child types inherit attributes from parent types
- **Position Ordering**: Types can be ordered within their schema

## Attribute Types

Assets supports various attribute types:

- **Text** (id: 0): Simple text values
- **Number** (id: 1): Numeric values
- **Boolean** (id: 2): True/false values
- **Date** (id: 3): Date values
- **Time** (id: 4): Time values
- **DateTime** (id: 6): Combined date and time
- **URL** (id: 7): Web URLs
- **Email** (id: 8): Email addresses
- **Reference** (id: 9): References to other objects
- **User** (id: 10): Atlassian user references
- **Group** (id: 11): Atlassian group references

## Response Codes

- **200** - Success
- **400** - Bad Request - Invalid parameters or request body
- **401** - Unauthorized - Authentication required
- **404** - Not Found - Schema or object type not found
- **500** - Internal Server Error

## Implementation Notes

- **Schema Keys** must be unique within the workspace
- **Object Type Names** must be unique within their schema
- **Attribute Names** must be unique within their object type
- **Position Values** determine display order in the UI
- **Inheritance** allows for efficient schema design and maintenance
- **Icon Management** uses predefined icon sets or custom uploads
- **Permissions** are checked at the schema level (`canManage` field)
- **Counts** can be expensive to calculate, use `includeCounts=false` for better performance
