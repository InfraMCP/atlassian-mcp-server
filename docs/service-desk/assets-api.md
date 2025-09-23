# Assets API

The Assets API provides access to Jira Service Management Assets (formerly Insight) workspaces.

## Endpoints

### Get Assets Workspaces

**GET** `/rest/servicedeskapi/assets/workspace`

Returns a list of Assets workspace IDs. Include a workspace ID in the path to access the [Assets REST APIs](https://developer.atlassian.com/cloud/assets/rest).

**Permissions required**: Any

**OAuth 2.0 Scopes**: `read:servicedesk-request`

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start` | integer | 0 | The starting index of the returned workspace IDs. Base index: 0 |
| `limit` | integer | 50 | The maximum number of workspace IDs to return per page |

#### Response

**200 - Success**
```json
{
  "_expands": [],
  "size": 1,
  "start": 1,
  "limit": 1,
  "isLastPage": true,
  "_links": {
    "base": "https://your-domain.atlassian.net/rest/servicedeskapi",
    "context": "context",
    "next": "https://your-domain.atlassian.net/rest/servicedeskapi/rest/servicedeskapi/assets/workspace?start=2&limit=1",
    "prev": "https://your-domain.atlassian.net/rest/servicedeskapi/rest/servicedeskapi/assets/workspace?start=0&limit=1"
  },
  "values": [
    {
      "workspaceId": "1060ba0e-178b-4e0e-g0h1-jedb02cccb5f"
    }
  ]
}
```

**401 - Unauthorized**
Authentication credentials are incorrect or missing.

**403 - Forbidden**
User does not have the necessary permission.

**500 - Internal Server Error**
Server error occurred.

---

### Get Insight Workspaces (Deprecated)

**GET** `/rest/servicedeskapi/insight/workspace`

⚠️ **DEPRECATED**: This endpoint is deprecated, please use `/assets/workspace/`.

**OAuth 2.0 Scopes**: `read:servicedesk-request`

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start` | integer | 0 | Starting index for pagination |
| `limit` | integer | 50 | Maximum number of items per page |

#### Response

**200 - Success**
Returns paginated insight workspace data.

**500 - Internal Server Error**
Server error occurred.

## Implementation Notes

- The Assets API requires the `read:servicedesk-request` OAuth scope
- Use the newer `/assets/workspace` endpoint instead of the deprecated `/insight/workspace`
- Workspace IDs returned from this API can be used with the dedicated [Assets REST APIs](https://developer.atlassian.com/cloud/assets/rest)
- All endpoints support pagination using `start` and `limit` parameters
