# Confluence Content Properties API

## Overview
The Content Properties API allows you to attach custom metadata to various content types in Confluence. Content properties are key-value pairs that can store structured data, configuration settings, or application-specific information alongside content.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:page:confluence` - Read content properties (varies by content type)
  - `write:page:confluence` - Create/update content properties (varies by content type)

## Supported Content Types
Content properties can be attached to:
- **Pages** - `/pages/{page-id}/properties`
- **Blog Posts** - `/blogposts/{blogpost-id}/properties`
- **Attachments** - `/attachments/{attachment-id}/properties`
- **Custom Content** - `/custom-content/{custom-content-id}/properties`
- **Comments** - `/comments/{comment-id}/properties`
- **Spaces** - `/spaces/{space-id}/properties`
- **Whiteboards** - `/whiteboards/{whiteboard-id}/properties`
- **Databases** - `/databases/{database-id}/properties`
- **Embeds** - `/embeds/{embed-id}/properties`
- **Folders** - `/folders/{folder-id}/properties`

## Core Operations

### Get Content Properties
Retrieve all properties for a specific content item.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{content-id}/properties`

**Parameters:**
- `key` (string, optional) - Filter by specific property key (case sensitive)
- `sort` (ContentPropertySortOrder, optional) - Sort order for results
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Example:** `GET /wiki/api/v2/pages/123456789/properties?key=custom-metadata`

### Create Content Property
Create a new property for a content item.

**Endpoint Pattern:** `POST /wiki/api/v2/{content-type}/{content-id}/properties`

**Request Body:** ContentPropertyCreateRequest
- `key` (string, required) - Property key identifier
- `value` (object, required) - Property value (JSON object)

**Response:** 200 OK with created property details

### Get Specific Content Property
Retrieve a specific property by its ID.

**Endpoint Pattern:** `GET /wiki/api/v2/{content-type}/{content-id}/properties/{property-id}`

**Response:** Property details with key, value, and metadata

### Update Content Property
Update an existing property's value.

**Endpoint Pattern:** `PUT /wiki/api/v2/{content-type}/{content-id}/properties/{property-id}`

**Request Body:** Updated property value and metadata

**Response:** 200 OK with updated property details

### Delete Content Property
Remove a property from content.

**Endpoint Pattern:** `DELETE /wiki/api/v2/{content-type}/{content-id}/properties/{property-id}`

**Response:** 204 No Content (permanent deletion)

## Example Usage

### Create Page Property
```http
POST /wiki/api/v2/pages/123456789/properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "review-status",
  "value": {
    "status": "pending",
    "reviewer": "john.doe@company.com",
    "dueDate": "2024-02-15",
    "priority": "high"
  }
}
```

### Get Properties with Filter
```http
GET /wiki/api/v2/pages/123456789/properties?key=review-status&limit=10
Authorization: Bearer {access_token}
```

### Update Property Value
```http
PUT /wiki/api/v2/pages/123456789/properties/987654321
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "review-status",
  "value": {
    "status": "approved",
    "reviewer": "john.doe@company.com",
    "approvedDate": "2024-02-10",
    "priority": "high"
  }
}
```

## Use Cases

### Metadata Management
- **Document Status:** Track review, approval, or publication status
- **Custom Fields:** Store additional structured data not available in standard fields
- **Integration Data:** Store external system IDs or synchronization metadata
- **Workflow State:** Maintain custom workflow or process state information

### Application Integration
- **Configuration Storage:** Store app-specific configuration per content item
- **External References:** Link content to external systems or databases
- **Analytics Data:** Store usage metrics or performance data
- **Automation Triggers:** Store data for automated processes or workflows

### Content Organization
- **Classification:** Add custom taxonomies or categorization
- **Relationships:** Define custom relationships between content items
- **Versioning:** Track custom version information or change history
- **Access Control:** Store additional permission or access metadata

## Data Structure
Content properties store JSON objects with the following structure:
```json
{
  "id": "property-id",
  "key": "property-key",
  "value": {
    // Custom JSON object
  },
  "version": {
    "number": 1,
    "createdAt": "2024-01-15T10:00:00.000Z"
  },
  "_links": {
    "self": "/wiki/api/v2/pages/123/properties/456"
  }
}
```

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **Read Properties:** Permission to view the parent content
- **Create/Update Properties:** Permission to update the parent content
- **Delete Properties:** Permission to update the parent content

## Error Handling
- **400 Bad Request:** Invalid property key, value format, or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for content or property operations
- **404 Not Found:** Content item or property not found
- **409 Conflict:** Property key already exists (for create operations)
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Keys:** Choose meaningful, consistent property key names
- **Structure Values:** Use well-structured JSON objects for complex data
- **Namespace Keys:** Prefix keys with app/feature names to avoid conflicts
- **Validate Data:** Ensure property values conform to expected schemas
- **Handle Permissions:** Check content permissions before property operations
- **Cache Appropriately:** Cache property data when appropriate to reduce API calls
- **Clean Up:** Remove unused properties to avoid clutter
