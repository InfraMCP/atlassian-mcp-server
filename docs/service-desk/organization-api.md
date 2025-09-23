# Organization API

The Organization API provides comprehensive management of organizations in Jira Service Management, including organization CRUD operations, user management, service desk associations, and custom properties.

## Core Organization Management

### Create Organization

**POST** `/rest/servicedeskapi/organization`

This method creates an organization by passing the name of the organization.

**Permissions required**: Service desk administrator or agent. Note: Permission to create organizations can be switched to users with the Jira administrator permission, using the **Organization management** feature.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization:jira-service-management`, `write:organization:jira-service-management`

**Connect app scope required**: ADMIN

#### Request Body

```json
{
  "name": "Charlie Cakes Franchises"
}
```

#### Response

**201 - Created**
```json
{
  "_links": {
    "self": "https://your-domain.atlassian.net/rest/servicedeskapi/organization/1"
  },
  "id": "1",
  "name": "Charlie Cakes Franchises",
  "scimManaged": false
}
```

---

### Get Organization

**GET** `/rest/servicedeskapi/organization/{organizationId}`

This method returns details of an organization. Use this method to get organization details whenever your application component is passed an organization ID but needs to display other organization details.

**Permissions required**: Any

**Response limitations**: Customers can only retrieve organization of which they are members.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization:jira-service-management`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | integer | Yes | The ID of the organization |

#### Response

**200 - Success**
```json
{
  "_links": {
    "self": "https://your-domain.atlassian.net/rest/servicedeskapi/organization/1"
  },
  "id": "1",
  "name": "Charlie Cakes Franchises",
  "scimManaged": false
}
```

---

### Delete Organization

**DELETE** `/rest/servicedeskapi/organization/{organizationId}`

This method deletes an organization. Note that the organization is deleted regardless of other associations it may have. For example, associations with service desks.

**Permissions required**: Jira administrator.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization:jira-service-management`, `delete:organization:jira-service-management`

**Connect app scope required**: DELETE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | integer | Yes | The ID of the organization |

#### Response

**204 - No Content**
Organization was deleted.

## User Management

### Get Users in Organization

**GET** `/rest/servicedeskapi/organization/{organizationId}/user`

This method returns all the users associated with an organization. Use this method where you want to provide a list of users for an organization or determine if a user is associated with an organization.

**Permissions required**: Service desk administrator or agent.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.user:jira-service-management`, `read:user:jira`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | integer | Yes | The ID of the organization |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum number of users per page (default: 50) |

#### Response

**200 - Success**
Returns a paged list of users associated with the organization, ordered by their accountId.

---

### Add Users to Organization

**POST** `/rest/servicedeskapi/organization/{organizationId}/user`

This method adds users to an organization.

**Permissions required**: Service desk administrator or agent. Note: Permission to add users to an organization can be switched to users with the Jira administrator permission, using the **Organization management** feature.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.user:jira-service-management`, `write:organization.user:jira-service-management`, `read:user:jira`

**Connect app scope required**: ADMIN

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | integer | Yes | The ID of the organization |

#### Request Body

```json
{
  "accountIds": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3a01db05e2a66fa80bd"
  ],
  "usernames": []
}
```

#### Response

**204 - No Content**
All users were valid and added to the organization.

---

### Remove Users from Organization

**DELETE** `/rest/servicedeskapi/organization/{organizationId}/user`

This method removes users from an organization.

**Permissions required**: Service desk administrator or agent. Note: Permission to delete users from an organization can be switched to users with the Jira administrator permission, using the **Organization management** feature.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.user:jira-service-management`, `delete:organization.user:jira-service-management`, `read:user:jira`

**Connect app scope required**: DELETE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | integer | Yes | The ID of the organization |

#### Request Body

```json
{
  "accountIds": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3a01db05e2a66fa80bd"
  ],
  "usernames": []
}
```

#### Response

**204 - No Content**
Request completed successfully.

## Service Desk Associations

### Get Organizations

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/organization`

This method returns a list of all organizations associated with a service desk.

**Permissions required**: Service desk's agent.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:servicedesk.organization:jira-service-management`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum number of items per page (default: 50) |
| `accountId` | string | Account ID of the user to filter organizations |

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
    "next": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/10001/organization?start=6&limit=3",
    "prev": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/10001/organization?start=0&limit=3"
  },
  "values": [
    {
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/organization/1"
      },
      "id": "1",
      "name": "Charlie Cakes Franchises",
      "scimManaged": false
    },
    {
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/organization/2"
      },
      "id": "2",
      "name": "Atlas Coffee Co",
      "scimManaged": false
    },
    {
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/organization/3"
      },
      "id": "3",
      "name": "The Adjustment Bureau",
      "scimManaged": false
    }
  ]
}
```

---

### Add Organization

**POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/organization`

This method adds an organization to a service desk. If the organization ID is already associated with the service desk, no change is made and the resource returns a 204 success code.

**Permissions required**: Service desk's agent.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:servicedesk.organization:jira-service-management`, `write:servicedesk.organization:jira-service-management`

**Connect app scope required**: WRITE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Request Body

```json
{
  "organizationId": 1
}
```

#### Response

**204 - No Content**
Organization was added or was already associated with the service desk.

---

### Remove Organization

**DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/organization`

This method removes an organization from a service desk. If the organization ID does not match an organization associated with the service desk, no change is made and the resource returns a 204 success code.

**Permissions required**: Service desk's agent.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:servicedesk.organization:jira-service-management`, `delete:servicedesk.organization:jira-service-management`

**Connect app scope required**: DELETE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Request Body

```json
{
  "organizationId": 1
}
```

#### Response

**204 - No Content**
Organization was removed from the service desk or no such organization was associated.

## Organization Properties

### Get Properties Keys

**GET** `/rest/servicedeskapi/organization/{organizationId}/property`

Returns the keys of all organization properties. Organization properties are a type of entity property which are available to the API only, and not shown in Jira Service Management.

**Permissions required**: Any

**Response limitations**: Customers can only access properties of organizations of which they are members.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.property:jira-service-management`

**Connect app scope required**: INACCESSIBLE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | string | Yes | The ID of the organization |

#### Response

**200 - Success**
```json
{
  "entityPropertyKeyBeans": [
    {
      "key": "organization.attributes",
      "self": "/rest/servicedeskapi/organization/1/property/propertyKey"
    }
  ]
}
```

---

### Get Property

**GET** `/rest/servicedeskapi/organization/{organizationId}/property/{propertyKey}`

Returns the value of an organization property. Use this method to obtain the JSON content for an organization's property.

**Permissions required**: Any

**Response limitations**: Customers can only access properties of organizations of which they are members.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.property:jira-service-management`

**Connect app scope required**: INACCESSIBLE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | string | Yes | The ID of the organization |
| `propertyKey` | string | Yes | The key of the property to return |

#### Response

**200 - Success**
```json
{
  "key": "organization.attributes",
  "value": {
    "mail": "charlie@example.com",
    "phone": "0800-1233456789"
  }
}
```

---

### Set Property

**PUT** `/rest/servicedeskapi/organization/{organizationId}/property/{propertyKey}`

Sets the value of an organization property. Use this resource to store custom data against an organization.

**Permissions required**: Service Desk Administrator or Agent. Note: Permission to manage organizations can be switched to users with the Jira administrator permission, using the **Organization management** feature.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.property:jira-service-management`, `write:organization.property:jira-service-management`

**Connect app scope required**: INACCESSIBLE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | string | Yes | The ID of the organization |
| `propertyKey` | string | Yes | The key of the property (max 255 bytes) |

#### Request Body

```json
{
  "mail": "charlie@example.com",
  "phone": "0800-1233456789"
}
```

The value must be valid, non-empty JSON. Maximum length: 32768 bytes.

#### Response

**200 - OK**
Organization property was updated.

**201 - Created**
Organization property was created.

---

### Delete Property

**DELETE** `/rest/servicedeskapi/organization/{organizationId}/property/{propertyKey}`

Removes an organization property.

**Permissions required**: Service Desk Administrator or Agent. Note: Permission to manage organizations can be switched to users with the Jira administrator permission, using the **Organization management** feature.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:organization.property:jira-service-management`, `delete:organization.property:jira-service-management`

**Connect app scope required**: INACCESSIBLE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | string | Yes | The ID of the organization |
| `propertyKey` | string | Yes | The key of the property to remove |

#### Response

**204 - No Content**
Organization property was removed.

## Implementation Notes

- **Organization Management Feature**: Many permissions can be switched to Jira administrators using the Organization management feature
- **SCIM Integration**: Organizations can be SCIM-managed for enterprise directory integration
- **Entity Properties**: Organization properties are API-only and not visible in the JSM UI
- **Customer Limitations**: Customers can only access organizations they are members of
- **Service Desk Associations**: Organizations can be associated with multiple service desks
- **User Management**: Both account IDs and usernames are supported for user operations
- **Property Limits**: Property keys max 255 bytes, values max 32768 bytes
- **Data Security**: Some endpoints are exempt from app access rules, others are not
