# Requesttype API

The Requesttype API provides management of customer request types in Jira Service Management, including retrieval, creation, field configuration, and property management.

## Core Request Type Management

### Get All Request Types

**GET** `/rest/servicedeskapi/requesttype`

This method returns all customer request types used in the Jira Service Management instance, optionally filtered by a query string.

**Permissions required**: Any

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:requesttype:jira-service-management`

**Connect app scope required**: READ

**Experimental**: This endpoint is experimental

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `searchQuery` | string | Filter results by name or description |
| `serviceDeskId` | array | Filter by service desk IDs (multiple values supported) |
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum items per page (default: 50) |
| `expand` | array | Expand properties |
| `includeHiddenRequestTypesInSearch` | boolean | Include hidden request types in search results (default: false) |
| `restrictionStatus` | string | Filter by restriction status: `open` or `restricted` |

#### Response

**200 - Success**
```json
{
  "_expands": [],
  "size": 3,
  "start": 3,
  "limit": 3,
  "isLastPage": false,
  "_links": {
    "base": "https://your-domain.atlassian.net/rest/servicedeskapi",
    "context": "context",
    "next": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/28/requesttype?start=6&limit=3",
    "prev": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/28/requesttype?start=0&limit=3"
  },
  "values": [
    {
      "_expands": [],
      "id": "11001",
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/28/requesttype/11001"
      },
      "name": "Get IT Help",
      "description": "Get IT Help",
      "helpText": "Please tell us clearly the problem you have within 100 words.",
      "issueTypeId": "12345",
      "serviceDeskId": "28",
      "portalId": "2",
      "groupIds": ["12"],
      "icon": {
        "id": "12345",
        "_links": {
          "iconUrls": {
            "48x48": "https://your-domain.atlassian.net/rest/api/2/universal_avatar/view/type/SD_REQTYPE/avatar/12345?size=large",
            "24x24": "https://your-domain.atlassian.net/rest/api/2/universal_avatar/view/type/SD_REQTYPE/avatar/12345?size=small",
            "16x16": "https://your-domain.atlassian.net/rest/api/2/universal_avatar/view/type/SD_REQTYPE/avatar/12345?size=xsmall",
            "32x32": "https://your-domain.atlassian.net/rest/api/2/universal_avatar/view/type/SD_REQTYPE/avatar/12345?size=medium"
          }
        }
      }
    }
  ]
}
```

**Note**: By default, this API filters out request types hidden in the portal (request types without groups and request types where a user doesn't have permission) when `searchQuery` is provided, unless `includeHiddenRequestTypesInSearch` is set to true.

---

### Get Request Types for Service Desk

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype`

This method returns all customer request types from a service desk. There are two parameters for filtering the returned list: `groupId` and `searchQuery`.

**Permissions required**: Permission to access the service desk.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:requesttype:jira-service-management`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `groupId` | integer | Filter results to those in a customer request type group |
| `expand` | array | Expand properties |
| `searchQuery` | string | Filter by name or description |
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum items per page (default: 50) |
| `includeHiddenRequestTypesInSearch` | boolean | Include hidden request types in search results (default: false) |
| `restrictionStatus` | string | Filter by restriction status: `open` or `restricted` |

#### Response

**200 - Success**
Returns the requested customer request types with the same structure as the global endpoint.

---

### Create Request Type

**POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype`

This method enables a customer request type to be added to a service desk based on an issue type. Note that not all customer request type fields can be specified in the request and these fields are given default values.

**Permissions required**: Service desk's administrator

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `read:requesttype:jira-service-management`, `write:requesttype:jira-service-management`

**Connect app scope required**: PROJECT_ADMIN

**Experimental**: This endpoint is experimental

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Request Body

```json
{
  "name": "Get IT Help",
  "description": "Get IT Help",
  "helpText": "Please tell us clearly the problem you have within 100 words.",
  "issueTypeId": "12345"
}
```

#### Default Values Applied

When creating a request type, the following defaults are applied:
- **Request type icon**: Given the headset icon
- **Request type groups**: Left empty (request type won't be visible on customer portal)
- **Status mapping**: Left empty (inherits from issue type)
- **Field mapping**: Set to show required fields from the issue type

These can be updated later by a service desk administrator using Project settings.

#### Response

**200 - Success**
Returns the created customer request type with full details including ID, icon, and configuration.

**Note**: Request Types are created in next-gen projects by creating Issue Types. Use the Jira Cloud Platform Create issue type endpoint instead for next-gen projects.

---

### Get Request Type by ID

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}`

This method returns a customer request type from a service desk.

**Permissions required**: Permission to access the service desk.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:requesttype:jira-service-management`

**Connect app scope required**: INACCESSIBLE

**Anonymous Access**: This operation can be accessed anonymously.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |
| `requestTypeId` | string | Yes | The ID of the customer request type |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | array | Expand properties |

#### Response

**200 - Success**
Returns the customer request type with complete details including name, description, help text, icon, and group associations.

---

### Delete Request Type

**DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}`

This method deletes a customer request type from a service desk, and removes it from all customer requests. This only supports classic projects.

**Permissions required**: Service desk administrator.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**: `manage:jira-project`

**Connect app scope required**: PROJECT_ADMIN

**Experimental**: This endpoint is experimental

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |
| `requestTypeId` | integer | Yes | The ID of the request type |

#### Response

**204 - No Content**
Request type is deleted.

## Field Management

### Get Request Type Fields

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/field`

This method returns the fields for a service desk's customer request type. Also returns information about the user's permissions for the request type.

**Permissions required**: Permission to view the Service Desk. However, hidden fields would be visible to only Service desk's Administrator.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:requesttype:jira-service-management`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |
| `requestTypeId` | integer | Yes | The ID of the request type |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | array | Use `hiddenFields` to include hidden fields in the response |

#### Response

**200 - Success**
```json
{
  "canAddRequestParticipants": true,
  "canRaiseOnBehalfOf": true,
  "requestTypeFields": [
    {
      "fieldId": "summary",
      "jiraSchema": {
        "system": "summary",
        "type": "string"
      },
      "name": "What do you need?",
      "required": true,
      "validValues": [],
      "visible": true
    },
    {
      "fieldId": "customfield_10000",
      "jiraSchema": {
        "custom": "com.atlassian.jira.plugin.system.customfieldtypes:userpicker",
        "customId": 10000,
        "type": "user"
      },
      "name": "Nominee",
      "required": true,
      "validValues": [],
      "visible": true
    },
    {
      "fieldId": "customfield_10001",
      "jiraSchema": {
        "custom": "com.atlassian.jira.plugin.system.customfieldtypes:radiobuttons",
        "customId": 10001,
        "type": "string"
      },
      "name": "Gifts",
      "required": true,
      "validValues": [
        {
          "children": [],
          "label": "Bottle of Wine",
          "value": "10000"
        },
        {
          "children": [],
          "label": "Threadless Voucher",
          "value": "10001"
        },
        {
          "children": [],
          "label": "2 Movie Tickets",
          "value": "10002"
        }
      ],
      "visible": false
    }
  ]
}
```

#### Permission Information

The response includes user permission details:
- **`canRaiseOnBehalfOf`**: `true` if the user can raise requests on behalf of other customers
- **`canAddRequestParticipants`**: `true` if the user can add request participants

#### Field Information

Each field includes:
- **`fieldId`**: Jira field identifier
- **`jiraSchema`**: Field type and schema information
- **`name`**: Display name for the field
- **`required`**: Whether the field is mandatory
- **`validValues`**: Available options for select fields
- **`visible`**: Whether the field is visible to the user

## Property Management

### Get Request Type Property Keys

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property`

Returns the keys of all properties for a request type.

**Permissions required**: The user must have permission to view the request type.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:requesttype.property:jira-service-management`

**Connect app scope required**: INACCESSIBLE

**Experimental**: This endpoint is experimental

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |
| `requestTypeId` | integer | Yes | The ID of the request type |

#### Response

**200 - Success**
```json
{
  "entityPropertyKeyBeans": [
    {
      "key": "requestType.attributes",
      "self": "/rest/servicedeskapi/servicedesk/1/requestType/2/property/propertyKey"
    }
  ]
}
```

**Note**: Properties for a Request Type in next-gen are stored as Issue Type properties and are also available via the Jira Cloud Platform Get issue type property keys endpoint.

---

### Get Request Type Property

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property/{propertyKey}`

Returns the value of a request type property.

**Permissions required**: The user must have permission to view the request type.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Set Request Type Property

**PUT** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property/{propertyKey}`

Sets the value of a request type property.

**Permissions required**: Service desk administrator.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

---

### Delete Request Type Property

**DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property/{propertyKey}`

Removes a request type property.

**Permissions required**: Service desk administrator.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

## Additional Features

### Check Request Type Permissions

**POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/permissions/check`

Checks if the user has permission to create requests for specific request types.

**Permissions required**: Permission to access the service desk.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Get Request Type Groups

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttypegroup`

Returns all request type groups for a service desk.

**Permissions required**: Permission to access the service desk.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

## Implementation Notes

### Request Type Visibility
- **Hidden Request Types**: Request types without groups or where users lack permission are filtered out by default in search operations
- **Restricted Request Types**: Not returned for non-admin users
- **Portal Visibility**: Request types need to be in groups to be visible on the customer portal

### Field Schema Types
- **System Fields**: `summary`, `description`, etc.
- **Custom Fields**: Various types including user pickers, select lists, text fields
- **Valid Values**: Available for select fields, radio buttons, checkboxes
- **Visibility**: Fields can be hidden from certain user types

### Project Type Considerations
- **Classic Projects**: Full CRUD operations supported
- **Next-gen Projects**: Request types are created via Issue Type endpoints
- **Property Storage**: Next-gen properties are stored as Issue Type properties

### Permission Levels
- **Any**: Basic read access to request types
- **Service Desk Access**: View service desk specific request types
- **Service Desk Administrator**: Full management capabilities
- **Anonymous Access**: Some endpoints support anonymous access

### Default Configurations
New request types receive default configurations that can be customized:
- Default headset icon
- Empty group assignments (hidden from portal)
- Inherited status mappings
- Required field mappings from issue type
