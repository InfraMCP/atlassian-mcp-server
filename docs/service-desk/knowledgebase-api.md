# Knowledgebase API

The Knowledgebase API provides access to knowledge base articles in Jira Service Management.

## Endpoints

### Get Articles (All Service Desks)

**GET** `/rest/servicedeskapi/knowledgebase/article`

Returns articles which match the given query string across all service desks.

**Permissions required**: Permission to access the customer portal.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**:
- **Classic (RECOMMENDED)**: `read:servicedesk-request`
- **Granular**: `read:knowledgebase:jira-service-management`

**Connect app scope required**: READ

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | The string used to filter the articles |
| `highlight` | boolean | Yes | If true, matching terms are highlighted using `@@@hl@@@term@@@endhl@@@` syntax (default: false) |
| `start` | integer | No | **Deprecated** - Starting index for pagination (base: 0) |
| `limit` | integer | No | Maximum number of items per page (default: 50) |
| `cursor` | string | No | Pointer to search results from previous search call |
| `prev` | boolean | No | Navigate to previous page (default: false) |

#### Response

**200 - Success**
```json
{
  "_expands": [],
  "size": 2,
  "start": 2,
  "limit": 2,
  "isLastPage": false,
  "_links": {
    "base": "https://your-domain.atlassian.net/rest/servicedeskapi",
    "context": "context",
    "next": "https://your-domain.atlassian.net/rest/servicedeskapi/knowledgebase/article?start=4&limit=2",
    "prev": "https://your-domain.atlassian.net/rest/servicedeskapi/knowledgebase/article?start=0&limit=2"
  },
  "values": [
    {
      "title": "Stolen computer",
      "excerpt": "assuming your computer was stolen",
      "source": {
        "type": "confluence",
        "pageId": "8786177",
        "spaceKey": "IT"
      },
      "content": {
        "iframeSrc": "https://your-domain.atlassian.net/rest/servicedeskapi/knowledgebase/article/view/8786177"
      }
    },
    {
      "title": "Upgrading computer",
      "excerpt": "each computer older then 3 years can be upgraded",
      "source": {
        "type": "confluence",
        "pageId": "8785228",
        "spaceKey": "IT"
      },
      "content": {
        "iframeSrc": "https://your-domain.atlassian.net/rest/servicedeskapi/knowledgebase/article/view/8785228"
      }
    }
  ]
}
```

**400 - Bad Request**
Request is invalid (e.g., missing query parameter).

**401 - Unauthorized**
User is not logged in.

**403 - Forbidden**
User does not have permission to complete this request.

**500 - Internal Server Error**
Server error occurred.

---

### Get Articles (Specific Service Desk)

**GET** `/rest/servicedeskapi/servicedesk/{serviceDeskId}/knowledgebase/article`

Returns articles which match the given query and belong to the knowledge base linked to the service desk.

**Permissions required**: Permission to access the service desk.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**: `read:knowledgebase:jira-service-management`

**Connect app scope required**: READ

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `serviceDeskId` | string | Yes | The ID of the service desk or project identifier |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | The string used to filter the articles |
| `highlight` | boolean | No | If true, matching terms are highlighted using `@@@hl@@@term@@@endhl@@@` syntax (default: false) |
| `start` | integer | No | **Deprecated** - Starting index for pagination (base: 0) |
| `limit` | integer | No | Maximum number of items per page (default: 50) |
| `cursor` | string | No | Pointer to search results from previous search call |
| `prev` | boolean | No | Navigate to previous page (default: false) |

#### Response

**200 - Success**
Same response format as the global articles endpoint, but filtered to the specific service desk's knowledge base.

**400 - Bad Request**
Request is invalid (e.g., missing query parameter).

**401 - Unauthorized**
User is not logged in.

**403 - Forbidden**
User does not have permission to complete this request.

**500 - Internal Server Error**
Server error occurred.

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Article title |
| `excerpt` | string | Article excerpt/summary |
| `source.type` | string | Source type (typically "confluence") |
| `source.pageId` | string | Confluence page ID |
| `source.spaceKey` | string | Confluence space key |
| `content.iframeSrc` | string | URL to view the article content |

## Implementation Notes

- The `query` parameter is required for both endpoints
- Use cursor-based pagination instead of the deprecated `start` parameter
- The `highlight` parameter adds special markup around matching terms for UI highlighting
- Articles are sourced from Confluence pages linked to the service desk
- Global search spans all accessible service desks, while service desk-specific search is scoped to that desk's knowledge base
- Both endpoints are exempt from app access rules but require appropriate OAuth scopes
