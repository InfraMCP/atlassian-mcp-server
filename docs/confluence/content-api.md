# Confluence Content API

## Overview
The Content API provides a utility endpoint for converting content IDs to their associated content types. This is primarily designed for users migrating from Confluence REST API v1 to v2.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:content.metadata:confluence` - Read content metadata

## Endpoint

### Convert Content IDs to Content Types
Converts a list of content IDs into their associated content types for v2 API compatibility.

**Endpoint:** `POST /wiki/api/v2/content/convert-ids-to-types`

**Request Body:** Array of content IDs to convert

**Response:** Mapping of content IDs to their v2 content types

**Key Differences from v1:**
- Returns `inline-comment` for inline comments (was `comment` in v1)
- Returns `footer-comment` for footer comments (was `comment` in v1)
- Other content types remain consistent with v2 naming

**Permissions:** 
- Permission to view the requested content required
- Content without view permission or non-existent content returns `null`

**Example Request:**
```http
POST /wiki/api/v2/content/convert-ids-to-types
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "contentIds": ["123456789", "987654321", "555666777"]
}
```

**Example Response:**
```json
{
  "results": {
    "123456789": "page",
    "987654321": "footer-comment", 
    "555666777": null
  }
}
```

## Use Cases
- **API Migration:** Convert v1 stored content IDs to v2 compatible types
- **Content Type Discovery:** Determine content types for existing IDs
- **Batch Processing:** Convert multiple content IDs in single request

## Error Handling
- **400 Bad Request:** Invalid request format or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **429 Too Many Requests:** Rate limit exceeded
