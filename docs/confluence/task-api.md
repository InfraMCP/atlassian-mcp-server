# Confluence Task API

## Overview
The Task API provides operations for managing tasks within Confluence pages and blog posts. Tasks are actionable items that can be assigned to users, tracked for completion, and managed with due dates. This API allows you to retrieve and update task information programmatically.

## Authentication
- **OAuth 2.0 Scopes Required:**
  - `read:task:confluence` - Read task information
  - `write:task:confluence` - Update task status

## Core Endpoints

### Get All Tasks
Retrieve tasks with comprehensive filtering and pagination.

**Endpoint:** `GET /wiki/api/v2/tasks`

**Parameters:**
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field
- `include-blank-tasks` (boolean, optional) - Include blank tasks (default: true)
- `status` (string, optional) - Filter by status: `complete`, `incomplete`
- `task-id` (array[integer], optional) - Filter by task IDs (max 250)
- `space-id` (array[integer], optional) - Filter by space IDs (max 250)
- `page-id` (array[integer], optional) - Filter by page IDs (max 250)
- `blogpost-id` (array[integer], optional) - Filter by blog post IDs (max 250)
- `created-by` (array[string], optional) - Filter by creator account IDs (max 250)
- `assigned-to` (array[string], optional) - Filter by assignee account IDs (max 250)
- `completed-by` (array[string], optional) - Filter by completer account IDs (max 250)
- `created-at-from` (integer, optional) - Filter by creation date start (epoch milliseconds)
- `created-at-to` (integer, optional) - Filter by creation date end (epoch milliseconds)
- `due-at-from` (integer, optional) - Filter by due date start (epoch milliseconds)
- `due-at-to` (integer, optional) - Filter by due date end (epoch milliseconds)
- `completed-at-from` (integer, optional) - Filter by completion date start (epoch milliseconds)
- `completed-at-to` (integer, optional) - Filter by completion date end (epoch milliseconds)
- `cursor` (string, optional) - Pagination cursor from Link header
- `limit` (integer, optional) - Results per page (1-250, default: 25)

**Permissions:** 'Can use' global permission. Only returns tasks user can view.

### Get Task by ID
Retrieve a specific task by its ID.

**Endpoint:** `GET /wiki/api/v2/tasks/{id}`

**Parameters:**
- `id` (integer, required) - Task ID
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field

**Response:** Task details with content and metadata

**Permissions:** Permission to view the containing page/blog post and its space

### Update Task
Update a task's status (currently only supports status updates).

**Endpoint:** `PUT /wiki/api/v2/tasks/{id}`

**Parameters:**
- `id` (integer, required) - Task ID
- `body-format` (PrimaryBodyRepresentation, optional) - Content format for body field

**Request Body:** TaskUpdateRequest
- Currently supports updating task status only

**Response:** 200 OK with updated task details

**Permissions:** Permission to edit the containing page/blog post and view its space

## Example Usage

### Get All Tasks with Filtering
```http
GET /wiki/api/v2/tasks?status=incomplete&assigned-to=5d5f9fbf-2d5b-4b5a-8b1a-1234567890ab&limit=50
Authorization: Bearer {access_token}
```

### Get Tasks by Date Range
```http
GET /wiki/api/v2/tasks?created-at-from=1704067200000&created-at-to=1706745600000&space-id=123456789
Authorization: Bearer {access_token}
```

### Get Specific Task
```http
GET /wiki/api/v2/tasks/987654321?body-format=storage
Authorization: Bearer {access_token}
```

### Update Task Status
```http
PUT /wiki/api/v2/tasks/987654321
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "complete"
}
```

## Example Response
```json
{
  "results": [
    {
      "id": "987654321",
      "status": "incomplete",
      "body": {
        "storage": {
          "value": "Review API documentation and provide feedback",
          "representation": "storage"
        }
      },
      "createdBy": {
        "accountId": "creator123",
        "displayName": "John Doe"
      },
      "assignedTo": {
        "accountId": "assignee456",
        "displayName": "Jane Smith"
      },
      "createdAt": "2024-01-15T10:00:00.000Z",
      "dueAt": "2024-01-20T17:00:00.000Z",
      "pageId": "123456789",
      "spaceId": "555666777",
      "_links": {
        "self": "/wiki/api/v2/tasks/987654321",
        "page": "/wiki/api/v2/pages/123456789"
      }
    }
  ],
  "_links": {
    "next": "/wiki/api/v2/tasks?cursor=next_page_token"
  }
}
```

## Use Cases

### Task Management
- **Project Tracking:** Track project tasks and deliverables across pages
- **Content Review:** Manage content review and approval tasks
- **Action Items:** Track action items from meetings and discussions
- **Workflow Management:** Integrate tasks into content workflows

### Team Collaboration
- **Assignment Tracking:** Monitor tasks assigned to team members
- **Progress Monitoring:** Track completion rates and overdue tasks
- **Workload Management:** Balance task distribution across team members
- **Deadline Management:** Monitor upcoming due dates and priorities

### Reporting & Analytics
- **Task Analytics:** Analyze task completion patterns and trends
- **Performance Metrics:** Track team productivity and task velocity
- **Overdue Reporting:** Identify and report on overdue tasks
- **Workload Analysis:** Analyze task distribution and capacity

### Integration Scenarios
- **Project Management:** Sync tasks with external project management tools
- **Notification Systems:** Send alerts for task assignments and due dates
- **Dashboard Creation:** Build task management dashboards and reports
- **Workflow Automation:** Automate task creation and status updates

## Task Properties

### Task Status
- **`incomplete`** - Task is not yet completed
- **`complete`** - Task has been completed

### Task Metadata
- **ID:** Unique task identifier
- **Body:** Task description and content
- **Status:** Current completion status
- **Created By:** User who created the task
- **Assigned To:** User assigned to complete the task
- **Completed By:** User who marked the task as complete
- **Created At:** Task creation timestamp
- **Due At:** Task due date (optional)
- **Completed At:** Task completion timestamp (if completed)
- **Page/Blog Post ID:** Container content ID
- **Space ID:** Space containing the task

### Content Association
Tasks are always associated with:
- **Pages:** Tasks within page content
- **Blog Posts:** Tasks within blog post content
- **Spaces:** Inherited from the containing page/blog post

## Date Filtering
All date filters use epoch time in milliseconds:
- **Creation Date:** When the task was created
- **Due Date:** When the task is due (if set)
- **Completion Date:** When the task was completed (if completed)

Date ranges are inclusive on both ends.

## Pagination
Uses cursor-based pagination with Link headers:
- Check `Link` response header for `next` URL
- Use relative URL from Link header for next page
- Maximum 250 results per request

## Permissions
- **View Tasks:** Permission to view the containing page/blog post and its space
- **Update Tasks:** Permission to edit the containing page/blog post and view its space
- **Task Visibility:** Only tasks user has permission to view are returned

## Error Handling
- **400 Bad Request:** Invalid parameters, date formats, or request body
- **401 Unauthorized:** Missing or invalid authentication
- **403 Forbidden:** Insufficient permissions to view or update tasks
- **404 Not Found:** Task, page, or blog post not found
- **429 Too Many Requests:** Rate limit exceeded

## Best Practices
- **Use Specific Filters:** Apply appropriate filters to reduce result sets
- **Handle Permissions:** Only access tasks for content user can view/edit
- **Monitor Due Dates:** Implement due date tracking and notifications
- **Batch Operations:** Use filtering to process multiple tasks efficiently
- **Cache Appropriately:** Cache task data when suitable to reduce API calls
- **Track Changes:** Monitor task status changes for workflow integration
- **Respect Limits:** Use pagination for large task sets

## Integration Patterns

### Task Dashboard
```javascript
// Get incomplete tasks assigned to current user
const myTasks = await getTasks({
  status: 'incomplete',
  assignedTo: [currentUserAccountId],
  limit: 50
});

// Get overdue tasks
const now = Date.now();
const overdueTasks = await getTasks({
  status: 'incomplete',
  dueAtTo: now,
  limit: 100
});
```

### Task Completion Workflow
```javascript
// Mark task as complete
await updateTask(taskId, {
  status: 'complete'
});

// Get updated task details
const completedTask = await getTaskById(taskId);

// Send completion notification
if (completedTask.status === 'complete') {
  await sendNotification(completedTask.assignedTo, 'Task completed');
}
```

### Team Task Analytics
```javascript
// Get team tasks for the month
const monthStart = new Date(2024, 0, 1).getTime();
const monthEnd = new Date(2024, 0, 31).getTime();

const teamTasks = await getTasks({
  createdAtFrom: monthStart,
  createdAtTo: monthEnd,
  assignedTo: teamMemberAccountIds,
  limit: 250
});

// Analyze completion rates
const completedTasks = teamTasks.filter(t => t.status === 'complete');
const completionRate = completedTasks.length / teamTasks.length;
```

## Current Limitations
- **Status Updates Only:** Currently only supports updating task status
- **No Task Creation:** Cannot create new tasks via API (tasks are created within page/blog post content)
- **No Task Deletion:** Cannot delete tasks via API
- **Limited Updates:** Cannot update task content, assignments, or due dates via API

## Future Enhancements
The Task API may be expanded in future releases to support:
- Task creation and deletion
- Assignment and due date updates
- Task content modification
- Advanced task properties and metadata
