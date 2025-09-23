# Servicedesk API

The Servicedesk API provides access to service desk information in Jira Service Management, including listing all service desks and retrieving individual service desk details.

## Core Service Desk Management

### Get Service Desks

**GET** `/rest/servicedeskapi/servicedesk`

This method returns all the service desks in the Jira Service Management instance that the user has permission to access. Use this method where you need a list of service desks or need to locate a service desk by name or keyword.

**Permissions required**: Any

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:servicedesk:jira-service-management`

**Connect app scope required**: READ

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum items per page (default: 50) |

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
    "next": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk?start=6&limit=3",
    "prev": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk?start=0&limit=3"
  },
  "values": [
    {
      "id": "10001",
      "projectId": "11001",
      "projectName": "IT Help Desk",
      "projectKey": "ITH",
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/10001"
      }
    },
    {
      "id": "10002",
      "projectId": "11002",
      "projectName": "HR Self Serve Desk",
      "projectKey": "HR",
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/10002"
      }
    },
    {
      "id": "10003",
      "projectId": "11003",
      "projectName": "Foundation Leave",
      "projectKey": "FL",
      "_links": {
        "self": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/10003"
      }
    }
  ]
}
```

**401 - Unauthorized**
User is not logged in.

**500 - Internal Server Error**
Server error occurred.

#### Performance Note

This method will be slow if the instance has hundreds of service desks. If you want to fetch a single service desk by its ID, use the individual service desk endpoint instead.

---

### Get Service Desk by ID

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}`

This method returns a service desk. Use this method to get service desk details whenever your application component is passed a service desk ID but needs to display other service desk details.

**Permissions required**: Permission to access the Service Desk. For example, being the Service Desk's Administrator or one of its Agents or Users.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:servicedesk:jira-service-management`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Response

**200 - Success**
```json
{
  "id": "10001",
  "projectId": "11001",
  "projectName": "IT Help Desk",
  "projectKey": "ITH",
  "_links": {
    "self": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/10001"
  }
}
```

**401 - Unauthorized**
User is not logged in.

**403 - Forbidden**
User does not have permission to complete this request.

**404 - Not Found**
Service desk does not exist.

**500 - Internal Server Error**
Server error occurred.

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The service desk ID |
| `projectId` | string | The underlying Jira project ID |
| `projectName` | string | The name of the service desk project |
| `projectKey` | string | The key of the service desk project |
| `_links.self` | string | URL to this service desk resource |

## Related Endpoints

The Servicedesk API works in conjunction with other APIs that use service desk IDs:

### Request Types
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype` - Get request types for this service desk
- **POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype` - Create request type in this service desk
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}` - Get specific request type
- **DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}` - Delete request type

### Request Type Fields
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/field` - Get fields for request type

### Request Type Properties
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property` - Get property keys
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property/{propertyKey}` - Get property value
- **PUT** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property/{propertyKey}` - Set property value
- **DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/{requestTypeId}/property/{propertyKey}` - Delete property

### Request Type Groups
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttypegroup` - Get request type groups

### Organizations
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/organization` - Get organizations associated with service desk
- **POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/organization` - Add organization to service desk
- **DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/organization` - Remove organization from service desk

### Customers
- **GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/customer` - Get customers for service desk
- **POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/customer` - Add customers to service desk
- **DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/customer` - Remove customers from service desk

### Permissions
- **POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/requesttype/permissions/check` - Check request type permissions

## Implementation Notes

### Service Desk Identification
- **Service Desk ID**: The primary identifier for service desks in the API
- **Project Identifier**: Can also use project key or project ID as alternative identifiers
- **Project Relationship**: Each service desk is backed by a Jira project

### Permission Levels
- **Any**: Basic read access to list service desks
- **Service Desk Access**: Required to view individual service desk details
- **Administrator**: Full management capabilities
- **Agent**: Can manage requests and some configurations
- **User**: Can create and view own requests

### Performance Considerations
- **List All Service Desks**: Can be slow with hundreds of service desks
- **Individual Lookup**: Much faster for single service desk retrieval
- **Pagination**: Use pagination for large instances
- **Caching**: Consider caching service desk information for frequently accessed data

### Data Security
- **List Endpoint**: Exempt from app access rules (returns only accessible service desks)
- **Individual Endpoint**: Not exempt from app access rules (requires specific permissions)
- **Visibility**: Users only see service desks they have permission to access

### Integration Patterns
1. **Service Desk Discovery**: Use list endpoint to find available service desks
2. **Service Desk Selection**: Present options to users based on their permissions
3. **Request Type Retrieval**: Get available request types for selected service desk
4. **Request Creation**: Use service desk ID in request creation workflows
5. **Organization Management**: Associate organizations with service desks
6. **Customer Management**: Manage customer access to service desks

### Error Handling
- **401 Unauthorized**: User authentication required
- **403 Forbidden**: User lacks permission for specific service desk
- **404 Not Found**: Service desk doesn't exist or user can't access it
- **500 Internal Server Error**: System error, retry may be appropriate

### Best Practices
- **Cache Service Desk Lists**: Avoid repeated calls for static information
- **Use Specific IDs**: Prefer individual service desk lookup over list filtering
- **Handle Permissions**: Gracefully handle cases where users lose access
- **Project Identifiers**: Support both service desk IDs and project keys for flexibility
- **Pagination**: Always implement pagination for list operations in large instances
