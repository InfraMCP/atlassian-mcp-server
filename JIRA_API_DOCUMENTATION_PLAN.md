# Jira Platform v3 API Documentation Plan

## Overview
Systematically document all Jira Platform v3 API endpoints for the Atlassian MCP Server project. This documentation will help developers build OAuth 2.0 integrations with Jira Cloud.

## Context
- **Project**: Atlassian MCP Server with OAuth 2.0 authentication
- **Source**: `docs/api-specs/jira-platform-swagger.json` OpenAPI specification
- **Target**: Individual markdown files in `docs/jira/` directory
- **Focus**: OAuth-compatible endpoints (skip Forge-only APIs)

## Complete Endpoint List (384 endpoints)
```
/rest/api/3/announcementBanner
/rest/api/3/app/field/{fieldIdOrKey}/context/configuration
/rest/api/3/app/field/{fieldIdOrKey}/value
/rest/api/3/app/field/context/configuration/list
/rest/api/3/app/field/value
/rest/api/3/application-properties
/rest/api/3/application-properties/{id}
/rest/api/3/application-properties/advanced-settings
/rest/api/3/applicationrole
/rest/api/3/applicationrole/{key}
/rest/api/3/attachment/{id}
/rest/api/3/attachment/{id}/expand/human
/rest/api/3/attachment/{id}/expand/raw
/rest/api/3/attachment/content/{id}
/rest/api/3/attachment/meta
/rest/api/3/attachment/thumbnail/{id}
/rest/api/3/auditing/record
/rest/api/3/avatar/{type}/system
/rest/api/3/bulk/issues/delete
/rest/api/3/bulk/issues/fields
/rest/api/3/bulk/issues/move
/rest/api/3/bulk/issues/transition
/rest/api/3/bulk/issues/unwatch
/rest/api/3/bulk/issues/watch
/rest/api/3/bulk/queue/{taskId}
/rest/api/3/changelog/bulkfetch
/rest/api/3/classification-levels
/rest/api/3/comment/{commentId}/properties
/rest/api/3/comment/{commentId}/properties/{propertyKey}
/rest/api/3/comment/list
/rest/api/3/component
/rest/api/3/component/{id}
/rest/api/3/component/{id}/relatedIssueCounts
/rest/api/3/configuration
/rest/api/3/configuration/timetracking
/rest/api/3/configuration/timetracking/list
/rest/api/3/configuration/timetracking/options
/rest/api/3/customFieldOption/{id}
/rest/api/3/dashboard
/rest/api/3/dashboard/{dashboardId}/gadget
/rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}
/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties
/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}
/rest/api/3/dashboard/{id}
/rest/api/3/dashboard/{id}/copy
/rest/api/3/dashboard/bulk/edit
/rest/api/3/dashboard/gadgets
/rest/api/3/dashboard/search
/rest/api/3/data-policy
/rest/api/3/data-policy/project
/rest/api/3/events
/rest/api/3/expression/analyse
/rest/api/3/expression/eval
/rest/api/3/expression/evaluate
/rest/api/3/field
/rest/api/3/field/{fieldId}
/rest/api/3/field/{fieldId}/context
/rest/api/3/field/{fieldId}/context/{contextId}
/rest/api/3/field/{fieldId}/context/{contextId}/issuetype
/rest/api/3/field/{fieldId}/context/{contextId}/issuetype/remove
/rest/api/3/field/{fieldId}/context/{contextId}/option
/rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId}
/rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId}/issue
/rest/api/3/field/{fieldId}/context/{contextId}/option/move
/rest/api/3/field/{fieldId}/context/{contextId}/project
/rest/api/3/field/{fieldId}/context/{contextId}/project/remove
/rest/api/3/field/{fieldId}/context/defaultValue
/rest/api/3/field/{fieldId}/context/issuetypemapping
/rest/api/3/field/{fieldId}/context/mapping
/rest/api/3/field/{fieldId}/context/projectmapping
/rest/api/3/field/{fieldId}/contexts
/rest/api/3/field/{fieldId}/screens
/rest/api/3/field/{fieldKey}/option
/rest/api/3/field/{fieldKey}/option/{optionId}
/rest/api/3/field/{fieldKey}/option/{optionId}/issue
/rest/api/3/field/{fieldKey}/option/suggestions/edit
/rest/api/3/field/{fieldKey}/option/suggestions/search
/rest/api/3/field/{id}
/rest/api/3/field/{id}/restore
/rest/api/3/field/{id}/trash
/rest/api/3/field/association
/rest/api/3/field/search
/rest/api/3/field/search/trashed
/rest/api/3/fieldconfiguration
/rest/api/3/fieldconfiguration/{id}
/rest/api/3/fieldconfiguration/{id}/fields
/rest/api/3/fieldconfigurationscheme
/rest/api/3/fieldconfigurationscheme/{id}
/rest/api/3/fieldconfigurationscheme/{id}/mapping
/rest/api/3/fieldconfigurationscheme/{id}/mapping/delete
/rest/api/3/fieldconfigurationscheme/mapping
/rest/api/3/fieldconfigurationscheme/project
/rest/api/3/filter
/rest/api/3/filter/{id}
/rest/api/3/filter/{id}/columns
/rest/api/3/filter/{id}/favourite
/rest/api/3/filter/{id}/owner
/rest/api/3/filter/{id}/permission
/rest/api/3/filter/{id}/permission/{permissionId}
/rest/api/3/filter/defaultShareScope
/rest/api/3/filter/favourite
/rest/api/3/filter/my
/rest/api/3/filter/search
/rest/api/3/group
/rest/api/3/group/bulk
/rest/api/3/group/member
/rest/api/3/group/user
/rest/api/3/groups/picker
/rest/api/3/groupuserpicker
/rest/api/3/instance/license
/rest/api/3/issue
/rest/api/3/issue/{issueIdOrKey}
/rest/api/3/issue/{issueIdOrKey}/assignee
/rest/api/3/issue/{issueIdOrKey}/attachments
/rest/api/3/issue/{issueIdOrKey}/changelog
/rest/api/3/issue/{issueIdOrKey}/changelog/list
/rest/api/3/issue/{issueIdOrKey}/comment
/rest/api/3/issue/{issueIdOrKey}/comment/{id}
/rest/api/3/issue/{issueIdOrKey}/editmeta
/rest/api/3/issue/{issueIdOrKey}/notify
/rest/api/3/issue/{issueIdOrKey}/properties
/rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey}
/rest/api/3/issue/{issueIdOrKey}/remotelink
/rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}
/rest/api/3/issue/{issueIdOrKey}/transitions
/rest/api/3/issue/{issueIdOrKey}/votes
/rest/api/3/issue/{issueIdOrKey}/watchers
/rest/api/3/issue/{issueIdOrKey}/worklog
/rest/api/3/issue/{issueIdOrKey}/worklog/{id}
/rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties
/rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}
/rest/api/3/issue/{issueIdOrKey}/worklog/move
/rest/api/3/issue/archive
/rest/api/3/issue/bulk
/rest/api/3/issue/bulkfetch
/rest/api/3/issue/createmeta
/rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes
/rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}
/rest/api/3/issue/limit/report
/rest/api/3/issue/picker
/rest/api/3/issue/properties
/rest/api/3/issue/properties/{propertyKey}
/rest/api/3/issue/properties/multi
/rest/api/3/issue/unarchive
/rest/api/3/issue/watching
/rest/api/3/issueLink
/rest/api/3/issueLink/{linkId}
/rest/api/3/issueLinkType
/rest/api/3/issueLinkType/{issueLinkTypeId}
/rest/api/3/issues/archive/export
/rest/api/3/issuesecurityschemes
/rest/api/3/issuesecurityschemes/{id}
/rest/api/3/issuesecurityschemes/{issueSecuritySchemeId}/members
/rest/api/3/issuesecurityschemes/{schemeId}
/rest/api/3/issuesecurityschemes/{schemeId}/level
/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}
/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member
/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member/{memberId}
/rest/api/3/issuesecurityschemes/level
/rest/api/3/issuesecurityschemes/level/default
/rest/api/3/issuesecurityschemes/level/member
/rest/api/3/issuesecurityschemes/project
/rest/api/3/issuesecurityschemes/search
/rest/api/3/issuetype
/rest/api/3/issuetype/{id}
/rest/api/3/issuetype/{id}/alternatives
/rest/api/3/issuetype/{id}/avatar2
/rest/api/3/issuetype/{issueTypeId}/properties
/rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}
/rest/api/3/issuetype/project
/rest/api/3/issuetypescheme
/rest/api/3/issuetypescheme/{issueTypeSchemeId}
/rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype
/rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/{issueTypeId}
/rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/move
/rest/api/3/issuetypescheme/mapping
/rest/api/3/issuetypescheme/project
/rest/api/3/issuetypescreenscheme
/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}
/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping
/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/default
/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/remove
/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/project
/rest/api/3/issuetypescreenscheme/mapping
/rest/api/3/issuetypescreenscheme/project
/rest/api/3/jql/autocompletedata
/rest/api/3/jql/autocompletedata/suggestions
/rest/api/3/jql/function/computation
/rest/api/3/jql/function/computation/search
/rest/api/3/jql/match
/rest/api/3/jql/parse
/rest/api/3/jql/pdcleaner
/rest/api/3/jql/sanitize
/rest/api/3/label
/rest/api/3/license/approximateLicenseCount
/rest/api/3/license/approximateLicenseCount/product/{applicationKey}
/rest/api/3/mypermissions
/rest/api/3/mypreferences
/rest/api/3/mypreferences/locale
/rest/api/3/myself
/rest/api/3/notificationscheme
/rest/api/3/notificationscheme/{id}
/rest/api/3/notificationscheme/{id}/notification
/rest/api/3/notificationscheme/{notificationSchemeId}
/rest/api/3/notificationscheme/{notificationSchemeId}/notification/{notificationId}
/rest/api/3/notificationscheme/project
/rest/api/3/permissions
/rest/api/3/permissions/check
/rest/api/3/permissions/project
/rest/api/3/permissionscheme
/rest/api/3/permissionscheme/{schemeId}
/rest/api/3/permissionscheme/{schemeId}/permission
/rest/api/3/permissionscheme/{schemeId}/permission/{permissionId}
/rest/api/3/plans/plan
/rest/api/3/plans/plan/{planId}
/rest/api/3/plans/plan/{planId}/archive
/rest/api/3/plans/plan/{planId}/duplicate
/rest/api/3/plans/plan/{planId}/team
/rest/api/3/plans/plan/{planId}/team/atlassian
/rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId}
/rest/api/3/plans/plan/{planId}/team/planonly
/rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId}
/rest/api/3/plans/plan/{planId}/trash
/rest/api/3/priority
/rest/api/3/priority/{id}
/rest/api/3/priority/default
/rest/api/3/priority/move
/rest/api/3/priority/search
/rest/api/3/priorityscheme
/rest/api/3/priorityscheme/{schemeId}
/rest/api/3/priorityscheme/{schemeId}/priorities
/rest/api/3/priorityscheme/{schemeId}/projects
/rest/api/3/priorityscheme/mappings
/rest/api/3/priorityscheme/priorities/available
/rest/api/3/project
/rest/api/3/project-template
/rest/api/3/project-template/edit-template
/rest/api/3/project-template/live-template
/rest/api/3/project-template/remove-template
/rest/api/3/project-template/save-template
/rest/api/3/project/{projectId}/email
/rest/api/3/project/{projectId}/hierarchy
/rest/api/3/project/{projectIdOrKey}
/rest/api/3/project/{projectIdOrKey}/archive
/rest/api/3/project/{projectIdOrKey}/avatar
/rest/api/3/project/{projectIdOrKey}/avatar/{id}
/rest/api/3/project/{projectIdOrKey}/avatar2
/rest/api/3/project/{projectIdOrKey}/avatars
/rest/api/3/project/{projectIdOrKey}/classification-level/default
/rest/api/3/project/{projectIdOrKey}/component
/rest/api/3/project/{projectIdOrKey}/components
/rest/api/3/project/{projectIdOrKey}/delete
/rest/api/3/project/{projectIdOrKey}/features
/rest/api/3/project/{projectIdOrKey}/features/{featureKey}
/rest/api/3/project/{projectIdOrKey}/properties
/rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}
/rest/api/3/project/{projectIdOrKey}/restore
/rest/api/3/project/{projectIdOrKey}/role
/rest/api/3/project/{projectIdOrKey}/role/{id}
/rest/api/3/project/{projectIdOrKey}/roledetails
/rest/api/3/project/{projectIdOrKey}/statuses
/rest/api/3/project/{projectIdOrKey}/version
/rest/api/3/project/{projectIdOrKey}/versions
/rest/api/3/project/{projectKeyOrId}/issuesecuritylevelscheme
/rest/api/3/project/{projectKeyOrId}/notificationscheme
/rest/api/3/project/{projectKeyOrId}/permissionscheme
/rest/api/3/project/{projectKeyOrId}/securitylevel
/rest/api/3/project/recent
/rest/api/3/project/search
/rest/api/3/project/type
/rest/api/3/project/type/{projectTypeKey}
/rest/api/3/project/type/{projectTypeKey}/accessible
/rest/api/3/project/type/accessible
/rest/api/3/projectCategory
/rest/api/3/projectCategory/{id}
/rest/api/3/projectvalidate/key
/rest/api/3/projectvalidate/validProjectKey
/rest/api/3/projectvalidate/validProjectName
/rest/api/3/redact
/rest/api/3/redact/status/{jobId}
/rest/api/3/resolution
/rest/api/3/resolution/{id}
/rest/api/3/resolution/default
/rest/api/3/resolution/move
/rest/api/3/resolution/search
/rest/api/3/role
/rest/api/3/role/{id}
/rest/api/3/role/{id}/actors
/rest/api/3/screens
/rest/api/3/screens/{screenId}
/rest/api/3/screens/{screenId}/availableFields
/rest/api/3/screens/{screenId}/tabs
/rest/api/3/screens/{screenId}/tabs/{tabId}
/rest/api/3/screens/{screenId}/tabs/{tabId}/fields
/rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}
/rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}/move
/rest/api/3/screens/{screenId}/tabs/{tabId}/move/{pos}
/rest/api/3/screens/addToDefault/{fieldId}
/rest/api/3/screens/tabs
/rest/api/3/screenscheme
/rest/api/3/screenscheme/{screenSchemeId}
/rest/api/3/search
/rest/api/3/search/approximate-count
/rest/api/3/search/jql
/rest/api/3/securitylevel/{id}
/rest/api/3/serverInfo
/rest/api/3/settings/columns
/rest/api/3/status
/rest/api/3/status/{idOrName}
/rest/api/3/statuscategory
/rest/api/3/statuscategory/{idOrKey}
/rest/api/3/statuses
/rest/api/3/statuses/{statusId}/project/{projectId}/issueTypeUsages
/rest/api/3/statuses/{statusId}/projectUsages
/rest/api/3/statuses/{statusId}/workflowUsages
/rest/api/3/statuses/search
/rest/api/3/task/{taskId}
/rest/api/3/task/{taskId}/cancel
/rest/api/3/uiModifications
/rest/api/3/uiModifications/{uiModificationId}
/rest/api/3/universal_avatar/type/{type}/owner/{entityId}
/rest/api/3/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id}
/rest/api/3/universal_avatar/view/type/{type}
/rest/api/3/universal_avatar/view/type/{type}/avatar/{id}
/rest/api/3/universal_avatar/view/type/{type}/owner/{entityId}
/rest/api/3/user
/rest/api/3/user/assignable/multiProjectSearch
/rest/api/3/user/assignable/search
/rest/api/3/user/bulk
/rest/api/3/user/bulk/migration
/rest/api/3/user/columns
/rest/api/3/user/email
/rest/api/3/user/email/bulk
/rest/api/3/user/groups
/rest/api/3/user/nav4-opt-property/{propertyKey}
/rest/api/3/user/permission/search
/rest/api/3/user/picker
/rest/api/3/user/properties
/rest/api/3/user/properties/{propertyKey}
/rest/api/3/user/search
/rest/api/3/user/search/query
/rest/api/3/user/search/query/key
/rest/api/3/user/viewissue/search
/rest/api/3/users
/rest/api/3/users/search
/rest/api/3/version
/rest/api/3/version/{id}
/rest/api/3/version/{id}/mergeto/{moveIssuesTo}
/rest/api/3/version/{id}/move
/rest/api/3/version/{id}/relatedIssueCounts
/rest/api/3/version/{id}/relatedwork
/rest/api/3/version/{id}/removeAndSwap
/rest/api/3/version/{id}/unresolvedIssueCount
/rest/api/3/version/{versionId}/relatedwork/{relatedWorkId}
/rest/api/3/webhook
/rest/api/3/webhook/failed
/rest/api/3/webhook/refresh
/rest/api/3/workflow
/rest/api/3/workflow/{entityId}
/rest/api/3/workflow/{workflowId}/project/{projectId}/issueTypeUsages
/rest/api/3/workflow/{workflowId}/projectUsages
/rest/api/3/workflow/{workflowId}/workflowSchemes
/rest/api/3/workflow/rule/config
/rest/api/3/workflow/rule/config/delete
/rest/api/3/workflow/search
/rest/api/3/workflow/transitions/{transitionId}/properties
/rest/api/3/workflows
/rest/api/3/workflows/capabilities
/rest/api/3/workflows/create
/rest/api/3/workflows/create/validation
/rest/api/3/workflows/defaultEditor
/rest/api/3/workflows/preview
/rest/api/3/workflows/search
/rest/api/3/workflows/update
/rest/api/3/workflows/update/validation
/rest/api/3/workflowscheme
/rest/api/3/workflowscheme/{id}
/rest/api/3/workflowscheme/{id}/createdraft
/rest/api/3/workflowscheme/{id}/default
/rest/api/3/workflowscheme/{id}/draft
/rest/api/3/workflowscheme/{id}/draft/default
/rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}
/rest/api/3/workflowscheme/{id}/draft/publish
/rest/api/3/workflowscheme/{id}/draft/workflow
/rest/api/3/workflowscheme/{id}/issuetype/{issueType}
/rest/api/3/workflowscheme/{id}/workflow
/rest/api/3/workflowscheme/{workflowSchemeId}/projectUsages
/rest/api/3/workflowscheme/project
/rest/api/3/workflowscheme/read
/rest/api/3/workflowscheme/update
/rest/api/3/workflowscheme/update/mappings
/rest/api/3/worklog/deleted
/rest/api/3/worklog/list
/rest/api/3/worklog/updated
```

## Proposed API Groups (Priority Order)

### Phase 1: Core APIs (High Priority)
1. **Issues API** (`issues-api.md`) - ✅ Already exists
   - `/rest/api/3/issue*` endpoints (30+ endpoints)
   - Core CRUD operations, search, bulk operations

2. **Projects API** (`projects-api.md`)
   - `/rest/api/3/project*` endpoints (40+ endpoints)
   - Project discovery, management, components, versions

3. **Search API** (`search-api.md`)
   - `/rest/api/3/search*` and `/rest/api/3/jql*` endpoints (10+ endpoints)
   - JQL search, autocomplete, parsing

4. **Users API** (`users-api.md`)
   - `/rest/api/3/user*`, `/rest/api/3/myself` endpoints (20+ endpoints)
   - User information, search, permissions

5. **Comments API** (`comments-api.md`)
   - `/rest/api/3/comment*` and issue comment endpoints (5+ endpoints)
   - Comment management and properties

### Phase 2: Essential APIs (Medium Priority)
6. **Attachments API** (`attachments-api.md`)
   - `/rest/api/3/attachment*` endpoints (6 endpoints)
   - File upload, download, metadata

7. **Workflows API** (`workflows-api.md`)
   - `/rest/api/3/workflow*` endpoints (25+ endpoints)
   - Workflow management, transitions, schemes

8. **Fields API** (`fields-api.md`)
   - `/rest/api/3/field*` endpoints (30+ endpoints)
   - Custom fields, contexts, options

9. **Permissions API** (`permissions-api.md`)
   - `/rest/api/3/permissions*`, `/rest/api/3/mypermissions` endpoints (5+ endpoints)
   - Permission checking and validation

10. **Issue Types API** (`issue-types-api.md`)
    - `/rest/api/3/issuetype*` endpoints (15+ endpoints)
    - Issue type management and schemes

### Phase 3: Specialized APIs (Lower Priority)
11. **Versions API** (`versions-api.md`)
    - `/rest/api/3/version*` endpoints (10+ endpoints)
    - Version management and related work

12. **Components API** (`components-api.md`)
    - `/rest/api/3/component*` endpoints (3 endpoints)
    - Component management

13. **Worklog API** (`worklog-api.md`)
    - `/rest/api/3/worklog*` and issue worklog endpoints (10+ endpoints)
    - Time tracking and work logging

14. **Groups API** (`groups-api.md`)
    - `/rest/api/3/group*` endpoints (5+ endpoints)
    - Group management and membership

15. **Filters API** (`filters-api.md`)
    - `/rest/api/3/filter*` endpoints (10+ endpoints)
    - Saved filter management

### Phase 4: Administrative APIs (Specialized Use Cases)
16. **Dashboards API** (`dashboards-api.md`)
    - `/rest/api/3/dashboard*` endpoints (10+ endpoints)
    - Dashboard and gadget management

17. **Security API** (`security-api.md`)
    - `/rest/api/3/issuesecurityschemes*` endpoints (15+ endpoints)
    - Security schemes and levels

18. **Screens API** (`screens-api.md`)
    - `/rest/api/3/screens*` endpoints (15+ endpoints)
    - Screen configuration and management

19. **Priorities API** (`priorities-api.md`)
    - `/rest/api/3/priority*` endpoints (8+ endpoints)
    - Priority management and schemes

20. **Status API** (`status-api.md`)
    - `/rest/api/3/status*` endpoints (10+ endpoints)
    - Status management and categories

## Documentation Standards

### File Structure Template
```markdown
# [API Name] API

## Overview
Brief description of the API's purpose and capabilities.

## OAuth 2.0 Scopes
List required scopes for each endpoint group.

## Endpoints

### [Endpoint Group Name]

#### [HTTP Method] [Endpoint Path]
**Description**: What this endpoint does
**OAuth Scopes**: Required scopes
**Parameters**: Request parameters
**Response**: Response format
**Example**: Practical usage example
**Error Codes**: Common error scenarios

## Use Cases
Practical integration scenarios and patterns.

## Best Practices
Implementation recommendations and gotchas.

## Related APIs
Links to related endpoint documentation.
```

### Key Requirements
- **OAuth Focus**: Document required scopes for each endpoint
- **Practical Examples**: Include JSON request/response examples
- **Error Handling**: Document common HTTP status codes and error responses
- **Use Cases**: Provide real-world integration scenarios
- **Minimal Approach**: Focus on essential information, avoid verbose descriptions

## Execution Strategy

### One-at-a-Time Approach
1. **Extract endpoint details** using jq from OpenAPI spec
2. **Group related endpoints** by functionality
3. **Document each API group** in separate markdown files
4. **Focus on OAuth-compatible endpoints** (skip Forge-only APIs)
5. **Validate against existing issues-api.md** for consistency

### Commands for Extraction
```bash
# Extract specific endpoint group
jq '.paths | to_entries | map(select(.key | startswith("/rest/api/3/project"))) | from_entries' docs/api-specs/jira-platform-swagger.json

# Extract endpoint details
jq '.paths["/rest/api/3/project"].get' docs/api-specs/jira-platform-swagger.json
```

## Next Steps
Start with **Projects API** (`projects-api.md`) as it's fundamental for most OAuth integrations and builds on the existing Issues API documentation pattern.

**Instruction**: Work through each API group systematically, one at a time, extracting endpoint details from the OpenAPI spec and creating comprehensive documentation following the established patterns.
