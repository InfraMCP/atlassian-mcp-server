# Confluence Smart Link API

## Overview
The Smart Link API provides operations for managing Smart Links (embeds) in Confluence's content tree. Smart Links are embedded content items that display rich previews of external resources, URLs, or other content within Confluence pages and spaces.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:embed:confluence` - Read Smart Link content and metadata
  - `write:embed:confluence` - Create Smart Links
  - `delete:embed:confluence` - Delete Smart Links

## Core Endpoints

### Create Smart Link
Create a new Smart Link in the content tree within a space.

**Endpoint:** `POST /wiki/api/v2/embeds`

**Request Body:** SmartLinkCreateRequest
- Must specify space and Smart Link configuration
- Supports embedding various external content types

**Response:** 200 OK with created Smart Link details

**Size Limit:** Maximum 5 MB request size

### Get Smart Link by ID
Retrieve a specific Smart Link with optional metadata.

**Endpoint:** `GET /wiki/api/v2/embeds/{id}`

**Parameters:**
- `id` (integer, required) - Smart Link ID
- `include-collaborators` (boolean, default: false) - Include collaborators
- `include-direct-children` (boolean, default: false) - Include direct children
- `include-operations` (boolean, default: false) - Include available operations (max 50)
- `include-properties` (boolean, default: false) - Include content properties (max 50)

**Response:** Smart Link details with optional metadata

### Delete Smart Link
Delete a Smart Link (moves to trash, can be restored).

**Endpoint:** `DELETE /wiki/api/v2/embeds/{id}`

**Response:** 204 No Content (Smart Link moved to trash)

## Related Endpoints

### Smart Link Properties
Manage custom properties attached to Smart Links:

- `GET /wiki/api/v2/embeds/{id}/properties` - Get Smart Link properties
- `POST /wiki/api/v2/embeds/{id}/properties` - Create property
- `GET /wiki/api/v2/embeds/{embed-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/embeds/{embed-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/embeds/{embed-id}/properties/{property-id}` - Delete property

### Smart Link Operations
- `GET /wiki/api/v2/embeds/{id}/operations` - Get available operations

### Smart Link Hierarchy
- `GET /wiki/api/v2/embeds/{id}/direct-children` - Get direct children
- `GET /wiki/api/v2/embeds/{id}/descendants` - Get all descendants
- `GET /wiki/api/v2/embeds/{id}/ancestors` - Get ancestors

## Example Usage

### Create Smart Link
```http
POST /wiki/api/v2/embeds
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "spaceId": "123456789",
  "title": "Project Dashboard",
  "url": "https://example.com/dashboard",
  "description": "External project dashboard embedded in Confluence"
}
```

### Get Smart Link with Metadata
```http
GET /wiki/api/v2/embeds/987654321?include-collaborators=true&include-properties=true
Authorization: Bearer {access_token}
```

### Create Smart Link Property
```http
POST /wiki/api/v2/embeds/987654321/properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "embed-config",
  "value": {
    "refreshInterval": "300",
    "displayMode": "card",
    "showPreview": true
  }
}
```

## Use Cases

### External Content Integration
- **Dashboard Embedding:** Embed external dashboards and analytics
- **Document Previews:** Display previews of external documents
- **Media Integration:** Embed videos, images, and multimedia content
- **Tool Integration:** Integrate external tools and applications

### Rich Content Display
- **URL Previews:** Generate rich previews for shared URLs
- **Social Media:** Embed social media posts and content
- **Code Repositories:** Display code snippets and repository information
- **Design Assets:** Embed design files and prototypes

### Collaboration Enhancement
- **Shared Resources:** Make external resources easily accessible
- **Reference Materials:** Embed reference documents and resources
- **Interactive Content:** Include interactive elements in pages
- **Real-time Data:** Display live data from external sources

### Content Organization
- **Resource Libraries:** Organize external resources in content tree
- **Topic Collections:** Group related external content by topic
- **Project Resources:** Centralize project-related external links
- **Knowledge Curation:** Curate external knowledge sources

## Smart Link Features
- **Rich Previews:** Automatic generation of rich content previews
- **Content Tree Integration:** Full integration with Confluence content hierarchy
- **Collaborative:** Support for collaborators and sharing
- **Properties:** Custom metadata attachment for configuration
- **Hierarchical:** Support parent-child relationships with other content
- **Permissions:** Inherit and manage access control through content tree

## Smart Link Types
Smart Links can embed various content types:
- **Web Pages:** General web page previews
- **Documents:** PDF, Office documents, and other file types
- **Media:** Images, videos, and audio content
- **Applications:** External application interfaces
- **APIs:** Dynamic content from API endpoints
- **Social Media:** Posts from social platforms

## Permissions
- **View Smart Link:** Permission to view the Smart Link and its space
- **Create Smart Link:** Permission to create Smart Links in the space
- **Edit Smart Link:** Permission to modify Smart Link properties
- **Delete Smart Link:** Permission to delete Smart Links in the space
- **Manage Properties:** Permission to manage Smart Link properties and metadata

## Error Handling
- **400 Bad Request:** Invalid Smart Link configuration or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for Smart Link operations
- **404 Not Found:** Smart Link or space not found
- **413 Payload Too Large:** Request exceeds 5 MB size limit
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Titles:** Choose clear, meaningful Smart Link titles
- **Validate URLs:** Ensure embedded URLs are accessible and appropriate
- **Manage Properties:** Use properties to store configuration and metadata
- **Handle Permissions:** Ensure proper space and Smart Link permissions
- **Monitor Performance:** Consider impact of external content on page load times
- **Regular Maintenance:** Review and update Smart Links to ensure they remain valid
- **Security Considerations:** Be cautious with embedded content from external sources
- **User Experience:** Ensure embedded content enhances rather than disrupts user experience

## Integration Patterns

### Automated Smart Link Creation
```javascript
// Create Smart Link for external dashboard
const smartLink = await createSmartLink({
  spaceId: spaceId,
  title: "Team Metrics Dashboard",
  url: "https://metrics.company.com/team-dashboard",
  description: "Real-time team performance metrics"
});
```

### Smart Link Management
```javascript
// Get Smart Link with full metadata
const smartLink = await getSmartLinkById(linkId, {
  includeProperties: true,
  includeOperations: true,
  includeCollaborators: true
});

// Update Smart Link configuration
await updateSmartLinkProperty(linkId, "display-config", {
  autoRefresh: true,
  refreshInterval: 300,
  showHeader: false
});
```

### Content Organization
```javascript
// Organize Smart Links in content hierarchy
const children = await getSmartLinkChildren(parentLinkId);
const ancestors = await getSmartLinkAncestors(linkId);

// Create hierarchical Smart Link structure
await createSmartLink({
  spaceId: spaceId,
  parentId: parentLinkId,
  title: "Sub-dashboard",
  url: "https://metrics.company.com/sub-dashboard"
});
```
