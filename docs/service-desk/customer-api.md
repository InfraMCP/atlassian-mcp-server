# Customer API

The Customer API provides methods to manage customers in Jira Service Management.

## Endpoints

### Create Customer

**POST** `/rest/servicedeskapi/customer`

This method adds a customer to the Jira Service Management instance by passing a JSON file including an email address and display name. The display name does not need to be unique. The record's identifiers, `name` and `key`, are automatically generated from the request details.

**Permissions required**: Jira Administrator Global permission

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:customer:jira-service-management`, `write:customer:jira-service-management`, `read:user:jira`

**Connect app scope required**: ADMIN

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `strictConflictStatusCode` | boolean | Optional boolean flag to return 409 Conflict status code for duplicate customer creation request |

#### Request Body

```json
{
  "displayName": "Fred F. User",
  "email": "fred@example.com"
}
```

#### Response

**201 - Created**
```json
{
  "accountId": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
  "name": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
  "key": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
  "emailAddress": "fred@example.com",
  "displayName": "Fred F. User",
  "active": true,
  "timeZone": "Australia/Sydney",
  "_links": {
    "jiraRest": "https://your-domain.atlassian.net/rest/api/2/user?username=qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "avatarUrls": {
      "16x16": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=16&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D16%26noRedirect%3Dtrue",
      "24x24": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=24&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D24%26noRedirect%3Dtrue",
      "32x32": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=32&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D32%26noRedirect%3Dtrue",
      "48x48": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=48&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D48%26noRedirect%3Dtrue"
    },
    "self": "https://your-domain.atlassian.net/rest/api/2/user?username=qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b"
  }
}
```

**400 - Bad Request**
Request is invalid, either because the email address is incorrectly formed or already exists in the database.

**401 - Unauthorized**
User is not logged in.

**403 - Forbidden**
User does not have permission to complete this request.

**409 - Conflict**
Email address already exists in the database and `strictConflictStatusCode=true`.

**500 - Internal Server Error**
Server error occurred.

---

### Get Customers

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/customer`

This method returns a list of the customers on a service desk.

The returned list of customers can be filtered using the `query` parameter. The parameter is matched against customers' `displayName`, `name`, or `email`. For example, searching for "John", "Jo", "Smi", or "Smith" will match a user with display name "John Smith".

**Permissions required**: Permission to view this Service Desk's customers

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:servicedesk.customer:jira-service-management`, `read:user:jira`

**Connect app scope required**: READ

**Experimental**: This endpoint is experimental

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Filter string matched against displayName, name, or email |
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum number of users per page (default: 50) |

#### Response

**200 - Success**
```json
{
  "_expands": [],
  "size": 1,
  "start": 1,
  "limit": 1,
  "isLastPage": false,
  "_links": {
    "base": "https://your-domain.atlassian.net/rest/servicedeskapi",
    "context": "context",
    "next": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/1/customer?start=2&limit=1",
    "prev": "https://your-domain.atlassian.net/rest/servicedeskapi/servicedesk/1/customer?start=0&limit=1"
  },
  "values": [
    {
      "accountId": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
      "name": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
      "key": "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
      "emailAddress": "fred@example.com",
      "displayName": "Fred F. User",
      "active": true,
      "timeZone": "Australia/Sydney",
      "_links": {
        "jiraRest": "https://your-domain.atlassian.net/rest/api/2/user?username=qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
        "avatarUrls": {
          "16x16": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=16&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D16%26noRedirect%3Dtrue",
          "24x24": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=24&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D24%26noRedirect%3Dtrue",
          "32x32": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=32&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D32%26noRedirect%3Dtrue",
          "48x48": "https://avatar-cdn.atlassian.com/9bc3b5bcb0db050c6d7660b28a5b86c9?s=48&d=https%3A%2F%2Fsecure.gravatar.com%2Favatar%2F9bc3b5bcb0db050c6d7660b28a5b86c9%3Fd%3Dmm%26s%3D48%26noRedirect%3Dtrue"
        },
        "self": "https://your-domain.atlassian.net/rest/api/2/user?username=qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b"
      }
    }
  ]
}
```

---

### Add Customers

**POST** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/customer`

Adds one or more customers to a service desk. If any of the passed customers are associated with the service desk, no changes will be made for those customers and the resource returns a 204 success code.

**Permissions required**: Service desk administrator

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:servicedesk.customer:jira-service-management`, `write:servicedesk.customer:jira-service-management`

**Connect app scope required**: WRITE

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Request Body

```json
{
  "accountIds": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3a01db05e2a66fa80bd",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
  ],
  "usernames": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3a01db05e2a66fa80bd",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
  ]
}
```

#### Response

**204 - No Content**
All customers were added to the service desk or were already associated with it.

**400 - Bad Request**
Some customers do not exist. Valid customers are still added.

**401 - Unauthorized**
User is not logged in.

**403 - Forbidden**
User does not have permission to complete this request.

**404 - Not Found**
Service desk does not exist.

**500 - Internal Server Error**
Server error occurred.

---

### Remove Customers

**DELETE** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/customer`

This method removes one or more customers from a service desk. The service desk must have closed access. If any of the passed customers are not associated with the service desk, no changes will be made for those customers and the resource returns a 204 success code.

**Permissions required**: Services desk administrator

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `manage:servicedesk-customer`
- **Granular**: `read:servicedesk.customer:jira-service-management`, `delete:servicedesk.customer:jira-service-management`

**Connect app scope required**: INACCESSIBLE

**Experimental**: This endpoint is experimental

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Request Body

```json
{
  "accountIds": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3a01db05e2a66fa80bd",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
  ],
  "usernames": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3581db05e2a66fa80b",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d3a01db05e2a66fa80bd",
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
  ]
}
```

#### Response

**204 - No Content**
Customers were removed from the service desk, or customers were not associated with the service desk.

**400 - Bad Request**
Service desk has public signup or open access enabled.

**401 - Unauthorized**
User is not logged in.

**403 - Forbidden**
User does not have permission to complete this request.

**404 - Not Found**
Service desk does not exist.

**500 - Internal Server Error**
Server error occurred.

## Implementation Notes

- All Customer API endpoints require the `manage:servicedesk-customer` OAuth scope
- Customer filtering supports partial matches against displayName, name, or email fields
- Service desk must have closed access for customer removal operations
- Account IDs and usernames can be used interchangeably for customer identification
- All endpoints support standard error responses (401, 403, 404, 500)
