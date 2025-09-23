# Jira Search API (v3)

The Jira Search API v3 provides powerful issue search capabilities using JQL (Jira Query Language) with enhanced performance, pagination, and consistency features. This documentation covers the search endpoints used in the Atlassian MCP Server.

## Base URL Structure

All Jira v3 API endpoints follow this pattern:
```
https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/{endpoint}
```

## OAuth 2.0 Scopes Required

### Granular Scopes (Recommended)
- **`read:jira-work`** - Search and read issues across projects

### Classic Scopes (Legacy)
- **`read:jira-work`** - Read access to Jira work items

## Enhanced Search Operations

### Search Issues (Enhanced)

**GET** `/search/jql`

**POST** `/search/jql`

The enhanced search endpoint with improved performance, cursor-based pagination, and read-after-write consistency options. This is the recommended search method.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters (GET) / Request Body (POST)

| Parameter | Type | Description |
|-----------|------|-------------|
| `jql` | string | JQL query expression (required, must be bounded) |
| `nextPageToken` | string | Token for next page (cursor-based pagination) |
| `maxResults` | integer | Maximum results per page (default: 50, max: 5000) |
| `fields` | array | Fields to return (default: `id` only) |
| `expand` | string | Additional data: `renderedFields`, `names`, `schema`, `transitions`, `operations`, `editmeta`, `changelog` |
| `properties` | array | Issue properties to include (max: 5) |
| `fieldsByKeys` | boolean | Reference fields by keys instead of IDs (default: false) |
| `failFast` | boolean | Fail quickly on field loading errors (default: false) |
| `reconcileIssues` | array | Issue IDs for read-after-write consistency (max: 50) |

#### JQL Requirements
- **Bounded queries required**: Must include search restrictions (e.g., project, assignee)
- **Maximum 7 fields** in `ORDER BY` clause
- **Examples**:
  - ✅ Valid: `assignee = currentUser() ORDER BY created DESC`
  - ❌ Invalid: `ORDER BY key DESC` (unbounded)

#### Request Example (GET)
```
GET /search/jql?jql=project=WEB AND status!=Done&fields=summary,status,assignee&maxResults=50&expand=names
```

#### Request Example (POST)
```json
{
  "jql": "project = WEB AND assignee = currentUser() ORDER BY created DESC",
  "fields": ["summary", "status", "assignee", "created"],
  "maxResults": 100,
  "expand": "names,schema",
  "reconcileIssues": [10001, 10002]
}
```

#### Response Example
```json
{
  "issues": [
    {
      "id": "10001",
      "key": "WEB-123",
      "self": "https://your-domain.atlassian.net/rest/api/3/issue/10001",
      "fields": {
        "summary": "Fix login page bug",
        "status": {
          "id": "3",
          "name": "In Progress",
          "statusCategory": {
            "id": 4,
            "name": "In Progress",
            "colorName": "yellow"
          }
        },
        "assignee": {
          "accountId": "5b10a2844c20165700ede21g",
          "displayName": "John Smith",
          "active": true
        },
        "created": "2024-01-15T10:30:00.000+0000"
      }
    }
  ],
  "nextPageToken": "eyJzdGFydEF0IjoxMDB9",
  "isLast": false,
  "names": {
    "summary": "Summary",
    "status": "Status",
    "assignee": "Assignee"
  }
}
```

### Legacy Search (Deprecated)

**GET** `/search`

**POST** `/search`

**⚠️ Deprecated**: These endpoints are being removed (effective May 1, 2025). Use `/search/jql` instead.

Legacy search endpoints with offset-based pagination. Provided for reference only.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Migration Path
```javascript
// Old (deprecated)
const results = await searchIssues({
  jql: 'project = WEB',
  startAt: 0,
  maxResults: 50
});

// New (recommended)
const results = await searchIssuesEnhanced({
  jql: 'project = WEB ORDER BY created DESC',
  maxResults: 50,
  fields: ['id', 'key', 'summary']
});
```

## JQL Helper Operations

### Get JQL Autocomplete Data

**GET** `/jql/autocompletedata`

Get autocomplete suggestions for JQL field names, operators, and functions.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Response Example
```json
{
  "visibleFieldNames": [
    {
      "value": "assignee",
      "displayName": "Assignee",
      "auto": "true",
      "orderable": "true",
      "searchable": "true"
    },
    {
      "value": "project",
      "displayName": "Project", 
      "auto": "true",
      "orderable": "true",
      "searchable": "true"
    }
  ],
  "visibleFunctionNames": [
    {
      "value": "currentUser()",
      "displayName": "currentUser()",
      "isList": "false"
    }
  ],
  "jqlReservedWords": ["and", "or", "not", "in", "is", "was"]
}
```

### Get JQL Autocomplete Suggestions

**GET** `/jql/autocompletedata/suggestions`

Get field value suggestions for JQL autocomplete.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `fieldName` | string | Field name for suggestions |
| `fieldValue` | string | Partial field value |
| `predicateName` | string | JQL predicate (e.g., "in", "=") |
| `predicateValue` | string | Predicate value |

#### Request Example
```
GET /jql/autocompletedata/suggestions?fieldName=project&fieldValue=WE
```

#### Response Example
```json
{
  "results": [
    {
      "value": "WEB",
      "displayName": "Web Application (WEB)"
    },
    {
      "value": "WEBSITE", 
      "displayName": "Website Project (WEBSITE)"
    }
  ]
}
```

### Parse JQL Query

**GET** `/jql/parse`

Parse and validate a JQL query, returning structure and any errors.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `queries` | array | JQL queries to parse |
| `validation` | string | Validation level: `strict`, `warn`, `none` |

#### Request Example
```
GET /jql/parse?queries=project=WEB AND status!=Done&validation=strict
```

#### Response Example
```json
{
  "queries": [
    {
      "query": "project = WEB AND status != Done",
      "structure": {
        "where": {
          "logicalOperator": "and",
          "clauses": [
            {
              "field": "project",
              "operator": "=",
              "operand": "WEB"
            },
            {
              "field": "status", 
              "operator": "!=",
              "operand": "Done"
            }
          ]
        }
      },
      "errors": []
    }
  ]
}
```

### Sanitize JQL Query

**POST** `/jql/sanitize`

Sanitize JQL queries by removing or replacing invalid elements.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `queries` | array | JQL queries to sanitize |

#### Request Example
```json
{
  "queries": [
    {
      "query": "project = WEB AND assignee = john.smith@company.com"
    }
  ]
}
```

#### Response Example
```json
{
  "queries": [
    {
      "query": "project = WEB AND assignee = \"5b10a2844c20165700ede21g\"",
      "accountId": "5b10a2844c20165700ede21g",
      "errors": []
    }
  ]
}
```

### Match JQL Query

**POST** `/jql/match`

Check if specific issues match a JQL query without running a full search.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Request Body

| Field | Type | Description |
|-------|------|-------------|
| `jqls` | array | JQL queries to test |
| `issueIds` | array | Issue IDs to test against |

#### Request Example
```json
{
  "jqls": ["project = WEB AND status = 'In Progress'"],
  "issueIds": [10001, 10002, 10003]
}
```

#### Response Example
```json
{
  "matches": [
    {
      "matchedIssues": [10001, 10003],
      "errors": []
    }
  ]
}
```

## Search Count Operations

### Get Approximate Issue Count

**GET** `/search/approximate-count`

Get an approximate count of issues matching a JQL query without retrieving the full result set.

**OAuth 2.0 Scopes**: `read:jira-work`

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `jql` | string | JQL query for counting |

#### Request Example
```
GET /search/approximate-count?jql=project=WEB AND status!=Done
```

#### Response Example
```json
{
  "count": 1247,
  "isApproximate": true
}
```

## Use Cases

### Basic Issue Search
```javascript
// Search for current user's open issues
const myIssues = await searchIssuesEnhanced({
  jql: 'assignee = currentUser() AND status != Done ORDER BY priority DESC',
  fields: ['summary', 'status', 'priority', 'created'],
  maxResults: 50,
  expand: 'names'
});

// Search by project and component
const componentIssues = await searchIssuesEnhanced({
  jql: 'project = WEB AND component = "Frontend" ORDER BY created DESC',
  fields: ['key', 'summary', 'assignee', 'status'],
  maxResults: 100
});
```

### Advanced Search with Pagination
```javascript
// Initial search
let results = await searchIssuesEnhanced({
  jql: 'project = WEB ORDER BY created DESC',
  fields: ['summary', 'status', 'assignee'],
  maxResults: 50
});

// Paginate through results
while (!results.isLast) {
  const nextResults = await searchIssuesEnhanced({
    jql: 'project = WEB ORDER BY created DESC',
    fields: ['summary', 'status', 'assignee'],
    maxResults: 50,
    nextPageToken: results.nextPageToken
  });
  
  results.issues.push(...nextResults.issues);
  results = nextResults;
}
```

### JQL Autocomplete Implementation
```javascript
// Get field suggestions
const fieldSuggestions = await getJqlAutocompleteData();

// Get value suggestions for a field
const projectSuggestions = await getJqlAutocompleteSuggestions({
  fieldName: 'project',
  fieldValue: 'WE'
});

// Validate JQL before search
const parseResult = await parseJql({
  queries: ['project = WEB AND status != Done'],
  validation: 'strict'
});

if (parseResult.queries[0].errors.length === 0) {
  // JQL is valid, proceed with search
  const results = await searchIssuesEnhanced({
    jql: parseResult.queries[0].query
  });
}
```

### Read-After-Write Consistency
```javascript
// Create or update issues
const newIssue = await createIssue({...});
const updatedIssue = await updateIssue('WEB-123', {...});

// Search with consistency guarantee
const results = await searchIssuesEnhanced({
  jql: 'project = WEB AND updated >= -1h ORDER BY updated DESC',
  reconcileIssues: [newIssue.id, updatedIssue.id],
  fields: ['summary', 'status', 'updated']
});
```

## Best Practices

### JQL Query Optimization
- **Use bounded queries**: Always include project, assignee, or date restrictions
- **Limit ORDER BY fields**: Maximum 7 fields in ORDER BY clause
- **Index-friendly fields**: Use indexed fields like project, status, assignee for better performance
- **Avoid wildcards**: Minimize use of wildcards in text searches

### Field Selection
- **Request only needed fields**: Use `fields` parameter to reduce response size
- **Default behavior**: Enhanced search returns only `id` by default (vs. all navigable fields in legacy)
- **Field exclusion**: Use minus prefix to exclude specific fields (e.g., `-description`)
- **Expand selectively**: Only expand additional data when necessary

### Pagination Strategy
- **Use enhanced search**: Cursor-based pagination is more efficient than offset-based
- **Reasonable page sizes**: Start with 50-100 results per page
- **Handle large datasets**: Use `nextPageToken` for datasets over 1000 issues
- **Monitor performance**: Larger `maxResults` may impact response time

### Error Handling
- **Validate JQL first**: Use parse endpoint to validate complex queries
- **Handle bounded query errors**: Ensure queries include search restrictions
- **Graceful degradation**: Fall back to simpler queries if complex ones fail
- **Rate limiting**: Implement backoff for rate limit responses

### Performance Optimization
- **Cache autocomplete data**: JQL field and function data changes infrequently
- **Use approximate counts**: For UI indicators, approximate counts are sufficient
- **Batch operations**: Group related searches when possible
- **Field-specific searches**: Use appropriate fields for different search types

## Error Handling

### Common HTTP Status Codes

| Status | Description | Common Causes |
|--------|-------------|---------------|
| `200` | Success | Search completed successfully |
| `400` | Bad Request | Invalid JQL syntax or unbounded query |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Insufficient permissions for search scope |
| `404` | Not Found | Referenced projects or fields don't exist |

### JQL Error Types

| Error Type | Description | Solution |
|------------|-------------|----------|
| `UNBOUNDED_QUERY` | Query lacks search restrictions | Add project, assignee, or date filters |
| `INVALID_SYNTAX` | JQL syntax error | Use parse endpoint to validate |
| `UNKNOWN_FIELD` | Field doesn't exist | Check field names with autocomplete |
| `INVALID_OPERATOR` | Operator not supported for field | Use appropriate operator for field type |

### Error Response Example
```json
{
  "errorMessages": [
    "The query must be bounded with a search restriction."
  ],
  "errors": {
    "jql": "Query is unbounded. Please add a search restriction such as project, assignee, or date range."
  }
}
```

## Related APIs

- **[Issues API](issues-api.md)** - Get detailed issue information from search results
- **[Projects API](projects-api.md)** - Discover projects for search filtering
- **[Users API](users-api.md)** - Find users for assignee-based searches
- **[Fields API](fields-api.md)** - Understand available fields for JQL queries

## JQL Reference

### Common JQL Fields
- **`project`** - Project key or name
- **`assignee`** - Issue assignee (use accountId)
- **`status`** - Issue status name
- **`priority`** - Issue priority name
- **`created`** - Issue creation date
- **`updated`** - Last update date
- **`component`** - Project component
- **`fixVersion`** - Target version
- **`labels`** - Issue labels

### JQL Functions
- **`currentUser()`** - Current authenticated user
- **`now()`** - Current date/time
- **`startOfDay()`** - Start of current day
- **`endOfWeek()`** - End of current week
- **`membersOf()`** - Members of a group

### JQL Operators
- **Equality**: `=`, `!=`, `IS`, `IS NOT`
- **Comparison**: `>`, `>=`, `<`, `<=`
- **Text**: `~` (contains), `!~` (not contains)
- **Lists**: `IN`, `NOT IN`
- **Date**: `>=`, `<=` with date functions

### Example JQL Queries
```sql
-- Current user's open issues
assignee = currentUser() AND status != Done

-- Recent bugs in project
project = WEB AND type = Bug AND created >= -7d

-- High priority issues without assignee
priority = High AND assignee IS EMPTY

-- Issues updated this week
updated >= startOfWeek() AND updated <= endOfWeek()

-- Component-specific search
project = WEB AND component IN ("Frontend", "Backend")
```
