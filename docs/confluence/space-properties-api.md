# Confluence Space Properties API

## Overview
The Space Properties API allows you to manage custom metadata attached to Confluence spaces. Space properties are key-value pairs that can store configuration settings, application-specific data, or any structured information associated with a space.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:space:confluence` - Read space properties
  - `write:space:confluence` - Create and update space properties

## Core Endpoints

### Get Space Properties
Retrieve all properties for a specific space.

**Endpoint:** `GET /wiki/api/v2/spaces/{space-id}/properties`

**Parameters:**
- `space-id` (integer, required) - Space ID
- `key` (string, optional) - Filter by specific property key (case sensitive)
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Permissions:** 'Can use' global permission and 'View' permission for the space

### Create Space Property
Create a new property for a space.

**Endpoint:** `POST /wiki/api/v2/spaces/{space-id}/properties`

**Parameters:**
- `space-id` (integer, required) - Space ID

**Request Body:** SpacePropertyCreateRequest
- `key` (string, required) - Property key identifier
- `value` (object, required) - Property value (JSON object)

**Response:** 201 Created with property details and location header

**Permissions:** 'Can use' global permission and 'Admin' permission for the space

### Get Space Property by ID
Retrieve a specific property by its ID.

**Endpoint:** `GET /wiki/api/v2/spaces/{space-id}/properties/{property-id}`

**Parameters:**
- `space-id` (integer, required) - Space ID
- `property-id` (integer, required) - Property ID

**Response:** Property details with key, value, and metadata

**Permissions:** 'Can use' global permission and 'View' permission for the space

### Update Space Property
Update an existing property's value.

**Endpoint:** `PUT /wiki/api/v2/spaces/{space-id}/properties/{property-id}`

**Parameters:**
- `space-id` (integer, required) - Space ID
- `property-id` (integer, required) - Property ID

**Request Body:** Updated property value and metadata

**Response:** 200 OK with updated property details

**Permissions:** 'Can use' global permission and 'Admin' permission for the space

### Delete Space Property
Remove a property from a space.

**Endpoint:** `DELETE /wiki/api/v2/spaces/{space-id}/properties/{property-id}`

**Parameters:**
- `space-id` (integer, required) - Space ID
- `property-id` (integer, required) - Property ID

**Response:** 204 No Content (permanent deletion)

**Permissions:** 'Can use' global permission and 'Admin' permission for the space

## Example Usage

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
    "autoArchive": false,
    "notifications": {
      "emailDigest": true,
      "slackIntegration": {
        "enabled": true,
        "channel": "#project-updates"
      }
    }
  }
}
```

### Get Properties with Filter
```http
GET /wiki/api/v2/spaces/123456789/properties?key=space-config&limit=10
Authorization: Bearer {access_token}
```

### Update Property Value
```http
PUT /wiki/api/v2/spaces/123456789/properties/987654321
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "key": "space-config",
  "value": {
    "theme": "modern",
    "defaultPageTemplate": "project-status",
    "autoArchive": true,
    "notifications": {
      "emailDigest": false,
      "slackIntegration": {
        "enabled": true,
        "channel": "#project-alerts"
      }
    }
  }
}
```

### Get All Space Properties
```http
GET /wiki/api/v2/spaces/123456789/properties?limit=50
Authorization: Bearer {access_token}
```

## Example Response
```json
{
  "results": [
    {
      "id": "987654321",
      "key": "space-config",
      "value": {
        "theme": "corporate",
        "defaultPageTemplate": "meeting-notes",
        "autoArchive": false,
        "notifications": {
          "emailDigest": true,
          "slackIntegration": {
            "enabled": true,
            "channel": "#project-updates"
          }
        }
      },
      "version": {
        "number": 1,
        "createdAt": "2024-01-15T10:00:00.000Z"
      },
      "_links": {
        "self": "/wiki/api/v2/spaces/123456789/properties/987654321"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/spaces/123456789/properties?cursor=next_page_token"
  }
}
```

## Use Cases

### Space Configuration
- **Theme Settings:** Store space appearance and branding configuration
- **Default Templates:** Configure default page templates for the space
- **Behavior Settings:** Control space-specific behaviors and features
- **Integration Configuration:** Store settings for external integrations

### Application Data
- **App Settings:** Store application-specific configuration per space
- **Feature Flags:** Control feature availability on a per-space basis
- **Workflow Configuration:** Store custom workflow settings and rules
- **Analytics Configuration:** Store tracking and analytics settings

### Metadata Management
- **Space Classification:** Store space categorization and tagging information
- **Ownership Information:** Track space ownership and responsibility
- **Compliance Data:** Store compliance-related metadata and settings
- **Audit Information:** Track space-related audit and governance data

### Integration Scenarios
- **External System Sync:** Store synchronization settings and state
- **API Configuration:** Store API keys and endpoint configurations
- **Notification Settings:** Configure notification preferences and channels
- **Automation Rules:** Store automation and workflow rule configurations

## Data Structure
Space properties store JSON objects with the following structure:
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
    "self": "/wiki/api/v2/spaces/123/properties/456"
  }
}
```

## Common Property Keys
Consider using these conventional key patterns:

### Configuration Properties
- `space-config` - General space configuration
- `theme-settings` - Visual theme and branding
- `template-defaults` - Default template settings
- `feature-flags` - Feature availability flags

### Integration Properties
- `slack-integration` - Slack integration settings
- `jira-integration` - Jira integration configuration
- `external-apis` - External API configurations
- `webhook-settings` - Webhook configurations

### Metadata Properties
- `space-metadata` - General space metadata
- `ownership-info` - Space ownership information
- `compliance-data` - Compliance and governance data
- `analytics-config` - Analytics and tracking settings

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Properties:** 'Can use' global permission + 'View' space permission
- **Create/Update/Delete Properties:** 'Can use' global permission + 'Admin' space permission
- **Property Isolation:** Properties are isolated per space

## Error Handling
- **400 Bad Request:** Invalid property key, value format, or parameters
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions for space or property operations
- **404 Not Found:** Space or property not found
- **409 Conflict:** Property key already exists (for create operations)
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Descriptive Keys:** Choose meaningful, consistent property key names
- **Structure Values:** Use well-structured JSON objects for complex data
- **Namespace Keys:** Prefix keys with app/feature names to avoid conflicts
- **Validate Data:** Ensure property values conform to expected schemas
- **Handle Permissions:** Check space admin permissions before property operations
- **Cache Appropriately:** Cache property data when suitable to reduce API calls
- **Version Management:** Track property changes and maintain version history
- **Clean Up:** Remove unused properties to avoid clutter

## Integration Patterns

### Configuration Management
```javascript
// Get space configuration
const config = await getSpacePropertyByKey(spaceId, 'space-config');

// Update configuration
await updateSpaceProperty(spaceId, config.id, {
  key: 'space-config',
  value: {
    ...config.value,
    theme: 'modern',
    lastUpdated: new Date().toISOString()
  }
});
```

### Feature Flag Management
```javascript
// Check feature availability
const featureFlags = await getSpacePropertyByKey(spaceId, 'feature-flags');
const isAdvancedEditorEnabled = featureFlags.value.advancedEditor;

// Toggle feature
await updateSpaceProperty(spaceId, featureFlags.id, {
  key: 'feature-flags',
  value: {
    ...featureFlags.value,
    advancedEditor: !isAdvancedEditorEnabled
  }
});
```

### Integration Configuration
```javascript
// Store integration settings
await createSpaceProperty(spaceId, {
  key: 'slack-integration',
  value: {
    enabled: true,
    webhookUrl: 'https://hooks.slack.com/...',
    channel: '#project-updates',
    notifications: ['page-created', 'page-updated'],
    lastSync: new Date().toISOString()
  }
});

// Retrieve integration settings
const slackConfig = await getSpacePropertyByKey(spaceId, 'slack-integration');
if (slackConfig.value.enabled) {
  // Send notification to Slack
  await sendSlackNotification(slackConfig.value);
}
```
