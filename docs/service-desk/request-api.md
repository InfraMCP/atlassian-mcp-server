# Request API

The Request API provides comprehensive management of customer requests in Jira Service Management, including creation, retrieval, comments, attachments, approvals, SLA tracking, and workflow transitions.

## Core Request Management

### Get Customer Requests

**GET** `/rest/servicedeskapi/request`

This method returns all customer requests for the user executing the query. The returned customer requests are ordered chronologically by the latest activity on each request.

**Permissions required**: Permission to access the specified service desk.

**Response limitations**: For customers, the list returned will include request they created (or were created on their behalf) or are participating in only.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:request:jira-service-management`, `read:user:jira`

**Connect app scope required**: READ

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `searchTerm` | string | Filter requests where summary matches the search term (wildcards supported) |
| `requestOwnership` | array | Filter by ownership: `OWNED_REQUESTS`, `PARTICIPATED_REQUESTS`, `ORGANIZATION`, `ALL_ORGANIZATIONS`, `APPROVER`, `ALL_REQUESTS` |
| `requestStatus` | string | Filter by status: `CLOSED_REQUESTS`, `OPEN_REQUESTS`, `ALL_REQUESTS` |
| `approvalStatus` | string | Filter by approval status: `MY_PENDING_APPROVAL`, `MY_HISTORY_APPROVAL` (requires `requestOwnership=APPROVER`) |
| `organizationId` | integer | Filter by organization (requires `requestOwnership=ORGANIZATION`) |
| `serviceDeskId` | integer | Filter by service desk |
| `requestTypeId` | integer | Filter by request type (requires `serviceDeskId`) |
| `expand` | array | Expand properties: `serviceDesk`, `requestType`, `participant`, `sla`, `status`, `attachment`, `action`, `comment`, `comment.attachment`, `comment.renderedBody` |
| `start` | integer | Starting index for pagination (base: 0) |
| `limit` | integer | Maximum items per page (default: 50) |

#### Response

**200 - Success**
Returns paginated list of customer requests with comprehensive details including field values, status, reporter information, and expanded properties.

---

### Create Customer Request

**POST** `/rest/servicedeskapi/request`

This method creates a customer request in a service desk. The JSON request must include the service desk and customer request type, as well as any fields that are required for the request type.

**Permissions required**: Permission to create requests in the specified service desk.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `write:servicedesk-request`
- **Granular**: `read:request:jira-service-management`, `write:request:jira-service-management`, `read:user:jira`

**Connect app scope required**: WRITE

#### Request Body

```json
{
  "serviceDeskId": "10",
  "requestTypeId": "25",
  "requestFieldValues": {
    "summary": "Request JSD help via REST",
    "description": "I need a new *mouse* for my Mac"
  },
  "requestParticipants": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
  ],
  "form": {
    "answers": {
      "1": {
        "text": "Answer to a text form field"
      },
      "2": {
        "date": "2023-07-06"
      },
      "3": {
        "time": "14:35"
      },
      "4": {
        "choices": ["5"]
      },
      "5": {
        "users": [
          "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
        ]
      }
    }
  },
  "isAdfRequest": false
}
```

#### Field Requirements

- **`serviceDeskId`** (required): The service desk ID
- **`requestTypeId`** (required): The request type ID
- **`requestFieldValues`** (required): Map of Jira field IDs and their values
- **`requestParticipants`** (optional): Array of user account IDs (not available to customer-only users)
- **`raiseOnBehalfOf`** (optional): Account ID to create request on behalf of (not available to customer-only users)
- **`form`** (optional): Form answers for Proforma forms
- **`isAdfRequest`** (optional): Whether request uses Atlassian Document Format

#### Response

**201 - Created**
Returns the created customer request with full details including issue ID, key, field values, status, and reporter information.

---

### Get Customer Request

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}`

This method returns a customer request by ID or key.

**Permissions required**: Permission to access the specified service desk.

**Response limitations**: For customers, only a request they created, was created on their behalf, or they are participating in will be returned.

**Data Security Policy**: Not exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:request:jira-service-management`, `read:user:jira`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issueIdOrKey` | string | Yes | The ID or Key of the customer request |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `expand` | array | Expand properties: `serviceDesk`, `requestType`, `participant`, `sla`, `status`, `attachment`, `action`, `comment`, `comment.attachment`, `comment.renderedBody` |

#### Response

**200 - Success**
Returns the customer request with comprehensive details.

**Note**: `requestFieldValues` does not include hidden fields. To get all fields including hidden ones, use the request type field endpoint.

## Comments Management

### Get Request Comments

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/comment`

Returns all comments on a customer request, for the user executing the query.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issueIdOrKey` | string | Yes | The ID or Key of the customer request |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `public` | boolean | Filter by public/internal comments |
| `internal` | boolean | Filter by internal comments |
| `expand` | array | Expand properties: `attachment`, `renderedBody` |
| `start` | integer | Starting index for pagination |
| `limit` | integer | Maximum items per page (default: 50) |

---

### Create Request Comment

**POST** `/rest/servicedeskapi/request/{issueIdOrKey}/comment`

Creates a public or private (internal) comment on a customer request, with the comment visibility set by the `public` field.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issueIdOrKey` | string | Yes | The ID or Key of the customer request |

#### Request Body

```json
{
  "body": "This is a comment",
  "public": true
}
```

## Attachments Management

### Get Request Attachments

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/attachment`

Returns the attachments referenced in a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Create Attachment

**POST** `/rest/servicedeskapi/request/{issueIdOrKey}/attachment`

Adds one or more temporary attachments to a customer request. The attachment visibility is set by the `public` flag.

**Permissions required**: Permission to access the customer request and add attachments.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

#### Request Body

Multipart form data with:
- **`file`**: The attachment file(s)
- **`public`**: Boolean indicating if attachment is public

## Approvals Management

### Get Request Approvals

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/approval`

Returns all approvals on a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Answer Approval

**POST** `/rest/servicedeskapi/request/{issueIdOrKey}/approval/{approvalId}`

Answers a pending approval on a customer request.

**Permissions required**: Permission to answer the approval.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

#### Request Body

```json
{
  "decision": "approve"
}
```

Valid decisions: `approve`, `decline`

## Participants Management

### Get Request Participants

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/participant`

Returns a list of all the participants on a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Add Request Participants

**POST** `/rest/servicedeskapi/request/{issueIdOrKey}/participant`

Adds participants to a customer request.

**Permissions required**: Permission to manage participants on the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

#### Request Body

```json
{
  "accountIds": [
    "qm:a713c8ea-1075-4e30-9d96-891a7d181739:5ad6d69abfa3980ce712caae"
  ],
  "usernames": []
}
```

---

### Remove Request Participants

**DELETE** `/rest/servicedeskapi/request/{issueIdOrKey}/participant`

Removes participants from a customer request.

**Permissions required**: Permission to manage participants on the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

## SLA Management

### Get Request SLA Information

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/sla`

Returns all the SLA records on a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Get SLA Information by ID

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/sla/{slaMetricId}`

Returns the SLA record with the specified ID on a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

## Status and Transitions

### Get Request Status

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/status`

Returns a list of all the statuses a customer request has achieved.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Get Request Transitions

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/transition`

Returns a list of transitions that customers can perform on the request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Perform Request Transition

**POST** `/rest/servicedeskapi/request/{issueIdOrKey}/transition`

Performs a customer transition for a given request and transition ID.

**Permissions required**: Permission to transition the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

#### Request Body

```json
{
  "id": "711",
  "additionalComment": {
    "body": "Transition comment",
    "public": true
  }
}
```

## Notifications Management

### Get Notification Subscription

**GET** `/rest/servicedeskapi/request/{issueIdOrKey}/notification`

Returns the notification subscription status of the user making the request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Subscribe to Notifications

**PUT** `/rest/servicedeskapi/request/{issueIdOrKey}/notification`

Subscribes the user to receiving notifications from a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

---

### Unsubscribe from Notifications

**DELETE** `/rest/servicedeskapi/request/{issueIdOrKey}/notification`

Unsubscribes the user from receiving notifications from a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

## Feedback Management

### Get Request Feedback

**GET** `/rest/servicedeskapi/request/{requestIdOrKey}/feedback`

Returns the feedback associated with a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

---

### Post Request Feedback

**POST** `/rest/servicedeskapi/request/{requestIdOrKey}/feedback`

Adds feedback to a customer request.

**Permissions required**: Permission to access the customer request.

**OAuth 2.0 Scopes**: `write:servicedesk-request`

#### Request Body

```json
{
  "rating": 5,
  "comment": "Great service!"
}
```

## Implementation Notes

### Field Input Formats
- **Text fields**: String values
- **Date fields**: ISO 8601 format (YYYY-MM-DD)
- **DateTime fields**: ISO 8601 format with timezone
- **User fields**: Account ID strings
- **Multi-select fields**: Arrays of option IDs
- **Attachments**: Temporary attachment IDs from upload

### Permission Considerations
- **Customer users**: Limited to requests they created, were created on their behalf, or are participating in
- **Agent users**: Can access all requests in their service desks
- **`raiseOnBehalfOf`**: Not available to customer-only users
- **`requestParticipants`**: Not available to customer-only users or if feature is disabled

### Expansion Options
Use the `expand` parameter to include additional data:
- **`serviceDesk`**: Service desk details
- **`requestType`**: Request type details  
- **`participant`**: Participant information
- **`sla`**: SLA tracking information
- **`status`**: Status transition history
- **`attachment`**: Attachment details
- **`action`**: Available user actions
- **`comment`**: Comments and replies
- **`comment.attachment`**: Comment attachment details
- **`comment.renderedBody`**: HTML-rendered comment content

### Data Security
- Most endpoints are not exempt from app access rules
- Customer access is restricted to their own requests and participations
- Internal comments and attachments have additional visibility restrictions
