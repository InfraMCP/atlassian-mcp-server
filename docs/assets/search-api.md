# Assets Search API (v1)

The Assets Search API provides powerful query capabilities using Assets Query Language (AQL) and Insight Query Language (IQL) to find objects within Assets workspaces.

## Base URL Structure

All Assets API endpoints follow this pattern:
```
https://api.atlassian.com/jsm/assets/workspace/{workspaceId}/v1/{endpoint}
```

## OAuth 2.0 Scopes Required

- **`read:cmdb-object:jira`** - Read objects and search capabilities

## Search Operations

### Search Objects with AQL (Recommended)

**POST** `/object/aql`

Search for objects using Assets Query Language (AQL) with modern pagination and filtering.

**Query Parameters:**
- `startAt` (integer, default: 0): Starting index for pagination
- `maxResults` (integer, default: 25): Maximum number of objects to return
- `includeAttributes` (boolean, default: true): Include object attributes in response

**Request Body:**
```json
{
  "qlQuery": "objectType = Office AND Name LIKE SYD"
}
```

**Response Example:**
```json
{
  "startAt": 0,
  "maxResults": 25,
  "total": 5,
  "isLast": false,
  "values": [
    {
      "workspaceId": "f1668d0c-828c-470c-b7d1-8c4f48cd345a",
      "globalId": "f1668d0c-828c-470c-b7d1-8c4f48cd345a:88",
      "id": "88",
      "label": "SYD-1",
      "objectKey": "ITSM-88",
      "objectType": {
        "id": "23",
        "name": "Office",
        "description": "Lorem ipsum dolor sit amet...",
        "icon": {
          "id": "13",
          "name": "Building"
        }
      },
      "created": "2021-02-16T20:04:41.527Z",
      "updated": "2021-02-16T20:04:41.527Z",
      "attributes": [
        {
          "id": "637",
          "objectTypeAttributeId": "134",
          "objectAttributeValues": [
            {
              "value": "ITSM-88",
              "displayValue": "ITSM-88",
              "searchValue": "ITSM-88"
            }
          ]
        }
      ]
    }
  ],
  "objectTypeAttributes": [
    {
      "id": "134",
      "name": "Key",
      "defaultType": {
        "id": 0,
        "name": "Text"
      },
      "system": true,
      "editable": false
    }
  ]
}
```

### Search Objects with AQL (Deprecated)

**GET** `/aql/objects`

⚠️ **DEPRECATED**: This endpoint will be removed on September 18, 2024. Use `POST /object/aql` instead.

**Query Parameters:**
- `qlQuery` (string): AQL query string
- `page` (integer, default: 1): Page number for pagination
- `resultPerPage` (integer, default: 25): Results per page
- `includeAttributes` (boolean, default: true): Include object attributes
- `includeAttributesDeep` (integer, default: 1): Depth of attribute references
- `includeTypeAttributes` (boolean, default: false): Include attribute definitions
- `includeExtendedInfo` (boolean, default: false): Include connected Jira issues

### Search Objects with IQL

**GET** `/iql/objects`

Search for objects using Insight Query Language (IQL).

**Query Parameters:**
- `iqlQuery` (string): IQL query string
- `page` (integer, default: 1): Page number for pagination
- `resultPerPage` (integer, default: 25): Results per page
- `includeAttributes` (boolean, default: true): Include object attributes

### Get Total Count

**POST** `/object/aql/totalcount`

Get the total count of objects matching an AQL query without retrieving the actual objects.

**Request Body:**
```json
{
  "qlQuery": "objectType = Computer"
}
```

**Response:**
```json
{
  "totalCount": 150
}
```

## Navigation Lists

### AQL Navigation List

**POST** `/object/navlist/aql`

Get a navigation list of objects using AQL for building hierarchical views.

**Request Body:**
```json
{
  "qlQuery": "objectType = Department",
  "orderByTypeAttrId": "135"
}
```

### IQL Navigation List

**POST** `/object/navlist/iql`

Get a navigation list of objects using IQL for building hierarchical views.

**Request Body:**
```json
{
  "iqlQuery": "objectType = Department",
  "orderByTypeAttrId": "135"
}
```

## Query Language Examples

### Assets Query Language (AQL)

AQL is the modern query language for Assets with powerful filtering capabilities:

```sql
-- Basic object type search
objectType = "Computer"

-- Attribute filtering
objectType = "Computer" AND Status = "Active"

-- Text search with wildcards
objectType = "Server" AND Name LIKE "web*"

-- Date comparisons
objectType = "Asset" AND Created > "2023-01-01"

-- Reference object filtering
objectType = "Computer" AND Location.Name = "Sydney Office"

-- Multiple conditions
objectType = "Computer" AND (Status = "Active" OR Status = "Maintenance") AND Location.City = "Sydney"

-- Sorting
objectType = "Computer" ORDER BY Name ASC

-- Complex queries with functions
objectType = "Computer" AND hasValue(SerialNumber) AND Status IN ("Active", "Maintenance")
```

### Insight Query Language (IQL)

IQL is the legacy query language, still supported but AQL is recommended:

```sql
-- Basic searches
objectType = Computer

-- Attribute searches
objectType = Computer and Status = Active

-- Text matching
objectType = Server and Name like web*
```

## Pagination

### Modern Pagination (AQL POST)
- Uses `startAt` and `maxResults` parameters
- Returns `total`, `isLast` indicators
- Consistent with other Atlassian APIs

### Legacy Pagination (GET endpoints)
- Uses `page` and `resultPerPage` parameters
- Page numbers start from 1
- Returns pagination metadata in response

## Response Codes

- **200** - Success
- **400** - Bad Request - Invalid query syntax or parameters
- **401** - Unauthorized - Authentication required
- **429** - Rate Limited - Too many requests (500 per minute)
- **500** - Internal Server Error

## Implementation Notes

- **Use AQL over IQL** - AQL is more powerful and actively developed
- **Prefer POST `/object/aql`** over deprecated GET endpoints
- **Rate limiting** applies at 500 requests per minute
- **Query optimization** - Use specific object types and indexed attributes for better performance
- **Attribute depth** - Control reference object depth to manage response size
- **Pagination** - Always use pagination for large result sets
- **Case sensitivity** - Object type names and attribute names are case-sensitive
- **Wildcards** - Use `*` for wildcard matching in LIKE operations
