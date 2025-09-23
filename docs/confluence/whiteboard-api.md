# Confluence Whiteboard API

## Overview
The Whiteboard API provides operations for managing whiteboards in Confluence spaces. Whiteboards are visual collaboration tools that allow teams to brainstorm, plan, and organize ideas using digital canvases with drawing tools, sticky notes, and other visual elements.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:whiteboard:confluence` - Read whiteboard content and metadata
  - `write:whiteboard:confluence` - Create whiteboards
  - `delete:whiteboard:confluence` - Delete whiteboards

## Core Endpoints

### Create Whiteboard
Create a new whiteboard in a Confluence space.

**Endpoint:** `POST /wiki/api/v2/whiteboards`

**Parameters:**
- `private` (boolean, default: false) - Create private whiteboard (only creator has access)

**Request Body:** WhiteboardCreateRequest
- Must specify space and whiteboard configuration
- Supports visual collaboration setup

**Response:** 200 OK with created whiteboard details

**Size Limit:** Maximum 5 MB request size

### Get Whiteboard by ID
Retrieve a specific whiteboard with optional metadata.

**Endpoint:** `GET /wiki/api/v2/whiteboards/{id}`

**Parameters:**
- `id` (integer, required) - Whiteboard ID
- `include-collaborators` (boolean, default: false) - Include collaborators
- `include-direct-children` (boolean, default: false) - Include direct children
- `include-operations` (boolean, default: false) - Include available operations (max 50)
- `include-properties` (boolean, default: false) - Include content properties (max 50)

**Response:** Whiteboard details with optional metadata

### Delete Whiteboard
Delete a whiteboard (moves to trash, can be restored).

**Endpoint:** `DELETE /wiki/api/v2/whiteboards/{id}`

**Response:** 204 No Content (whiteboard moved to trash)

## Related Endpoints

### Whiteboard Properties
Manage custom properties attached to whiteboards:

- `GET /wiki/api/v2/whiteboards/{id}/properties` - Get whiteboard properties
- `POST /wiki/api/v2/whiteboards/{id}/properties` - Create property
- `GET /wiki/api/v2/whiteboards/{whiteboard-id}/properties/{property-id}` - Get specific property
- `PUT /wiki/api/v2/whiteboards/{whiteboard-id}/properties/{property-id}` - Update property
- `DELETE /wiki/api/v2/whiteboards/{whiteboard-id}/properties/{property-id}` - Delete property

### Whiteboard Operations
- `GET /wiki/api/v2/whiteboards/{id}/operations` - Get available operations

### Whiteboard Hierarchy
- `GET /wiki/api/v2/whiteboards/{id}/direct-children` - Get direct children
- `GET /wiki/api/v2/whiteboards/{id}/descendants` - Get all descendants
- `GET /wiki/api/v2/whiteboards/{id}/ancestors` - Get ancestors

### Whiteboard Classification
- `GET /wiki/api/v2/whiteboards/{id}/classification-level` - Get classification level
- `PUT /wiki/api/v2/whiteboards/{id}/classification-level` - Set classification level
- `POST /wiki/api/v2/whiteboards/{id}/classification-level/reset` - Reset classification

## Example Usage

### Create Whiteboard
```http
POST /wiki/api/v2/whiteboards?private=false
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "spaceId": "123456789",
  "title": "Project Planning Board",
  "description": "Whiteboard for planning the Q2 project roadmap"
}
```

### Get Whiteboard with Metadata
```http
GET /wiki/api/v2/whiteboards/987654321?include-collaborators=true&include-properties=true
Authorization: Bearer {access_token}
```

### Create Whiteboard Property
```http
POST /wiki/api/v2/whiteboards/987654321/properties
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "board-config",
  "value": {
    "template": "project-planning",
    "gridEnabled": true,
    "backgroundColor": "#ffffff",
    "defaultTools": ["sticky-note", "drawing", "text"]
  }
}
```

## Example Response
```json
{
  "id": "987654321",
  "title": "Project Planning Board",
  "description": "Whiteboard for planning the Q2 project roadmap",
  "spaceId": "123456789",
  "createdBy": {
    "accountId": "user123",
    "displayName": "John Doe"
  },
  "createdAt": "2024-01-15T10:00:00.000Z",
  "updatedAt": "2024-01-15T10:00:00.000Z",
  "collaborators": [
    {
      "accountId": "user123",
      "displayName": "John Doe",
      "role": "owner"
    },
    {
      "accountId": "user456",
      "displayName": "Jane Smith",
      "role": "editor"
    }
  ],
  "_links": {
    "self": "/wiki/api/v2/whiteboards/987654321",
    "webui": "/spaces/SPACE/whiteboards/987654321"
  }
}
```

## Use Cases

### Visual Collaboration
- **Brainstorming Sessions:** Create digital brainstorming spaces for team ideation
- **Project Planning:** Visual project roadmaps and timeline planning
- **Design Thinking:** Support design thinking workshops and processes
- **Mind Mapping:** Create visual mind maps and concept diagrams

### Team Workshops
- **Retrospectives:** Facilitate team retrospectives and improvement sessions
- **Strategy Planning:** Visual strategy development and planning sessions
- **Problem Solving:** Collaborative problem-solving and root cause analysis
- **Process Mapping:** Document and improve business processes visually

### Educational Content
- **Training Materials:** Create interactive training and educational content
- **Concept Visualization:** Explain complex concepts through visual diagrams
- **Collaborative Learning:** Enable collaborative learning experiences
- **Knowledge Sharing:** Share knowledge through visual representations

### Integration Scenarios
- **Template Management:** Create and manage whiteboard templates
- **Content Export:** Export whiteboard content for external use
- **Workflow Integration:** Integrate whiteboards into business workflows
- **Analytics:** Track whiteboard usage and collaboration patterns

## Whiteboard Features
- **Visual Canvas:** Infinite canvas for visual collaboration
- **Drawing Tools:** Pens, shapes, arrows, and drawing capabilities
- **Sticky Notes:** Digital sticky notes for idea capture
- **Text Elements:** Text boxes and labels for annotations
- **Templates:** Pre-built templates for common use cases
- **Real-time Collaboration:** Multiple users can collaborate simultaneously
- **Properties:** Custom metadata and configuration storage
- **Hierarchical:** Support parent-child relationships with other content

## Privacy Options
- **Public Whiteboards:** Visible to all space members with appropriate permissions
- **Private Whiteboards:** Only visible to creator, useful for personal brainstorming

## Permissions
- **View Whiteboard:** Permission to view the whiteboard and its space
- **Create Whiteboard:** Permission to create whiteboards in the space
- **Edit Whiteboard:** Permission to modify whiteboard content and properties
- **Delete Whiteboard:** Permission to delete whiteboards in the space
- **Manage Properties:** Permission to manage whiteboard properties and metadata

## Error Handling
- **400 Bad Request:** Invalid whiteboard configuration or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for whiteboard operations
- **404 Not Found:** Whiteboard or space not found
- **413 Payload Too Large:** Request exceeds 5 MB size limit
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Titles:** Choose clear, meaningful whiteboard titles
- **Set Appropriate Privacy:** Use private whiteboards for personal work, public for team collaboration
- **Manage Properties:** Use properties to store configuration and template information
- **Handle Permissions:** Ensure proper space and whiteboard permissions
- **Organize Hierarchically:** Use parent-child relationships for complex whiteboard structures
- **Regular Cleanup:** Remove unused whiteboards to avoid clutter
- **Template Reuse:** Create reusable templates for common whiteboard types
- **Collaboration Guidelines:** Establish team guidelines for whiteboard collaboration

## Integration Patterns

### Whiteboard Template Management
```javascript
// Create whiteboard from template
const whiteboard = await createWhiteboard({
  spaceId: spaceId,
  title: "Sprint Planning",
  description: "Sprint planning session for Team Alpha"
});

// Configure whiteboard with template properties
await createWhiteboardProperty(whiteboard.id, "template-config", {
  templateType: "sprint-planning",
  sprintNumber: 15,
  teamName: "Team Alpha",
  sprintGoal: "Implement user authentication"
});
```

### Collaborative Session Setup
```javascript
// Get whiteboard with collaborators
const whiteboard = await getWhiteboardById(whiteboardId, {
  includeCollaborators: true,
  includeProperties: true
});

// Check collaboration settings
const config = whiteboard.properties?.find(p => p.key === 'collaboration-config');
if (config?.value.realTimeEnabled) {
  // Enable real-time collaboration features
  enableRealTimeCollaboration(whiteboardId);
}
```

### Whiteboard Analytics
```javascript
// Get whiteboard hierarchy for analysis
const children = await getWhiteboardChildren(whiteboardId);
const ancestors = await getWhiteboardAncestors(whiteboardId);

// Analyze whiteboard structure
const analytics = {
  whiteboardId: whiteboardId,
  childCount: children.length,
  hierarchyDepth: ancestors.length,
  collaboratorCount: whiteboard.collaborators?.length || 0,
  lastUpdated: whiteboard.updatedAt
};
```

## Whiteboard Elements
Whiteboards can contain various visual elements:
- **Sticky Notes:** For capturing ideas and feedback
- **Drawings:** Freehand drawings and sketches
- **Shapes:** Geometric shapes and connectors
- **Text:** Text boxes and labels
- **Images:** Embedded images and media
- **Templates:** Pre-designed layouts and structures

## Collaboration Features
- **Real-time Editing:** Multiple users can edit simultaneously
- **Cursor Tracking:** See where other users are working
- **Change History:** Track changes and modifications
- **Comments:** Add comments and feedback to elements
- **Permissions:** Control who can view and edit
- **Notifications:** Get notified of changes and updates
