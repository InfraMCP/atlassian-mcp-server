# Assets Objects API (v1)

The Assets Objects API provides comprehensive object management capabilities for Jira Service Management Assets (formerly Insight). This API allows you to create, read, update, and delete objects within Assets workspaces.

## Base URL Structure

All Assets API endpoints follow this pattern:
```
https://api.atlassian.com/jsm/assets/workspace/{workspaceId}/v1/{endpoint}
```

## OAuth 2.0 Scopes Required

### Object Operations
- **`read:cmdb-object:jira`** - Read objects and their attributes
- **`write:cmdb-object:jira`** - Create and update objects
- **`delete:cmdb-object:jira`** - Delete objects

## Core Object Operations

### Get Object

**GET** `/object/{id}`

Retrieve a specific object by its ID, including all attributes and metadata.

**Parameters:**
- `id` (path, required): The object ID to retrieve

**Response Example:**
```json
{
  "workspaceId": "g2778e1d-939d-581d-c8e2-9d5g59de456b",
  "globalId": "g2778e1d-939d-581d-c8e2-9d5g59de456b:88",
  "id": "88",
  "label": "SYD-1",
  "objectKey": "ITSM-88",
  "objectType": {
    "id": "23",
    "name": "Office",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "icon": {
      "id": "13",
      "name": "Building",
      "url16": "https://api.atlassian.com/jsm/assets/workspace/.../icon.png?size=16"
    }
  },
  "created": "2021-02-16T20:04:41.527Z",
  "updated": "2021-02-16T20:04:41.527Z",
  "attributes": [
    {
      "id": "637",
      "objectTypeAttribute": {
        "id": "134",
        "name": "Key",
        "defaultType": {
          "id": 0,
          "name": "Text"
        }
      },
      "objectAttributeValues": [
        {
          "value": "ITSM-88",
          "displayValue": "ITSM-88"
        }
      ]
    }
  ]
}
```

### Update Object

**PUT** `/object/{id}`

Update an existing object's attributes.

**Parameters:**
- `id` (path, required): The object ID to update

**Request Body:**
```json
{
  "attributes": [
    {
      "objectTypeAttributeId": "265",
      "objectAttributeValues": [
        {
          "value": "Updated value"
        }
      ]
    }
  ],
  "objectTypeId": "23",
  "hasAvatar": false
}
```

### Delete Object

**DELETE** `/object/{id}`

Delete an object from the Assets workspace.

**Parameters:**
- `id` (path, required): The object ID to delete

### Create Object

**POST** `/object/create`

Create a new object in the Assets workspace.

**Request Body:**
```json
{
  "objectTypeId": "23",
  "attributes": [
    {
      "objectTypeAttributeId": "135",
      "objectAttributeValues": [
        {
          "value": "New Object Name"
        }
      ]
    }
  ]
}
```

## Object Attributes

### Get Object Attributes

**GET** `/object/{id}/attributes`

Retrieve all attributes for a specific object.

**Parameters:**
- `id` (path, required): The object ID

### Object History

**GET** `/object/{id}/history`

Get the change history for an object.

**Parameters:**
- `id` (path, required): The object ID

### Object Reference Information

**GET** `/object/{id}/referenceinfo`

Get information about objects that reference this object.

**Parameters:**
- `id` (path, required): The object ID

## Connected Tickets

### Get Connected Tickets

**GET** `/objectconnectedtickets/{objectId}/tickets`

Retrieve Jira tickets connected to an Assets object.

**Parameters:**
- `objectId` (path, required): The object ID

## Response Codes

- **200** - Success
- **400** - Bad Request - Invalid parameters or request body
- **401** - Unauthorized - Authentication required
- **404** - Not Found - Object not found
- **500** - Internal Server Error

## Implementation Notes

- All object operations require appropriate OAuth scopes
- Object IDs are workspace-specific
- Attributes must match the object type's schema
- Referenced objects require valid object type relationships
- Timestamps are in ISO 8601 format
- Avatar management is supported through the `hasAvatar` and `avatarUUID` fields
