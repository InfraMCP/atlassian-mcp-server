# Info API

The Info API provides information about the Jira Service Management instance.

## Endpoints

### Get Info

**GET** `/rest/servicedeskapi/info`

This method retrieves information about the Jira Service Management instance such as software version, builds, and related links.

**Permissions required**: None, the user does not need to be logged in.

**Data Security Policy**: Exempt from app access rules

**OAuth 2.0 Scopes**: None required (public endpoint)

**Connect app scope required**: READ

#### Response

**200 - Success**
```json
{
  "_links": {
    "self": "https://your-domain.atlassian.net/rest/servicedeskapi/info"
  },
  "buildChangeSet": "c6679417c550918e7c94a9eaaada133f15dc8ff0",
  "buildDate": {
    "epochMillis": 1442259240000,
    "friendly": "Monday 02:34 AM",
    "iso8601": "2015-09-15T02:34:00+0700",
    "jira": "2015-09-15T02:34:00.000+0700"
  },
  "isLicensedForUse": true,
  "platformVersion": "7.0.1",
  "version": "3.0.1"
}
```

**500 - Internal Server Error**
Server error occurred.

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `_links.self` | string | URL to this info endpoint |
| `buildChangeSet` | string | Git commit hash of the build |
| `buildDate` | object | Build timestamp in multiple formats |
| `buildDate.epochMillis` | number | Unix timestamp in milliseconds |
| `buildDate.friendly` | string | Human-readable date format |
| `buildDate.iso8601` | string | ISO 8601 formatted date |
| `buildDate.jira` | string | Jira-specific date format |
| `isLicensedForUse` | boolean | Whether the instance is properly licensed |
| `platformVersion` | string | Jira platform version |
| `version` | string | Jira Service Management version |

## Implementation Notes

- This is a public endpoint that requires no authentication
- Useful for health checks and version verification
- Can be called without any OAuth scopes or user login
- Returns comprehensive version and build information for the JSM instance
