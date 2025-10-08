# Assets Import API (v1)

The Assets Import API provides comprehensive data import capabilities for bringing external data into Assets workspaces. This includes CSV imports, database connections, and other data source integrations.

## Base URL Structure

All Assets API endpoints follow this pattern:
```
https://api.atlassian.com/jsm/assets/workspace/{workspaceId}/v1/{endpoint}
```

## OAuth 2.0 Scopes Required

### Import Operations
- **`import:import-configuration:cmdb`** - Manage import configurations and execute imports
- **`read:cmdb-object:jira`** - Read imported objects
- **`write:cmdb-object:jira`** - Create/update objects via import

## Import Execution

### Start Import

**POST** `/import/start/{id}`

Start a configured import process.

**Parameters:**
- `id` (path, required): The import configuration ID

**Response Example:**
```json
{
  "progressInPercent": 0,
  "resourceId": "9fa74b56-d540-4494-b9b2-f27a9bad9e6a",
  "category": "imports",
  "status": "IN_PROGRESS",
  "stepDescription": "Starting CSV import...",
  "currentStep": 1,
  "numberOfSteps": 6,
  "currentWorkUnits": 0,
  "currentWorkDescription": "CSV import started...",
  "currentStepTotalWorkUnits": 0,
  "totalWorkUnits": 0,
  "actor": "6g2c42d1f6fgd2112cgc66dc",
  "startDate": "2021-04-20T13:57:52.404Z",
  "executionUUID": "b36ebb89-4a75-4df3-9101-f40d2771db32"
}
```

## Import Source Management

### Get Import Source Configuration Status

**GET** `/importsource/{importSourceId}/configstatus`

Get the configuration status of an import source.

**Parameters:**
- `importSourceId` (path, required): The import source ID

### Get Import Source Token

**GET** `/importsource/{importSourceId}/token`

Retrieve authentication token for an import source.

**Parameters:**
- `importSourceId` (path, required): The import source ID

### Get Schema and Mapping

**GET** `/importsource/{importSourceId}/schema-and-mapping`

Get the schema definition and field mapping for an import source.

**Parameters:**
- `importSourceId` (path, required): The import source ID

### Get Import Mapping

**GET** `/importsource/{importSourceId}/mapping`

Get the field mapping configuration for an import source.

**Parameters:**
- `importSourceId` (path, required): The import source ID

### Get Mapping Progress

**GET** `/importsource/{importSourceId}/mapping/progress/{resourceId}`

Get the progress of a mapping operation.

**Parameters:**
- `importSourceId` (path, required): The import source ID
- `resourceId` (path, required): The resource ID for the mapping operation

## Import Execution Management

### List Import Executions

**GET** `/importsource/{importSourceId}/executions`

Get all executions for a specific import source.

**Parameters:**
- `importSourceId` (path, required): The import source ID

### Get Import Executions Status

**GET** `/importsource/{importSourceId}/executions/status`

Get the status of all executions for an import source.

**Parameters:**
- `importSourceId` (path, required): The import source ID

### Get Import Execution

**GET** `/importsource/{importSourceId}/executions/{importExecutionId}`

Get details of a specific import execution.

**Parameters:**
- `importSourceId` (path, required): The import source ID
- `importExecutionId` (path, required): The import execution ID

### Get Import Execution Data

**GET** `/importsource/{importSourceId}/executions/{importExecutionId}/data`

Get the data processed during a specific import execution.

**Parameters:**
- `importSourceId` (path, required): The import source ID
- `importExecutionId` (path, required): The import execution ID

### Get Import Execution Progress

**GET** `/importsource/{importSourceId}/executions/{importExecutionId}/progress`

Get the progress of a specific import execution.

**Parameters:**
- `importSourceId` (path, required): The import source ID
- `importExecutionId` (path, required): The import execution ID

### Get Import Execution Status

**GET** `/importsource/{importSourceId}/executions/{importExecutionId}/status`

Get the status of a specific import execution.

**Parameters:**
- `importSourceId` (path, required): The import source ID
- `importExecutionId` (path, required): The import execution ID

## Progress Monitoring

### Get Import Progress

**GET** `/progress/category/imports/{id}`

Get the progress of an import operation by category.

**Parameters:**
- `id` (path, required): The progress resource ID

**Response Example:**
```json
{
  "progressInPercent": 75,
  "resourceId": "9fa74b56-d540-4494-b9b2-f27a9bad9e6a",
  "category": "imports",
  "status": "IN_PROGRESS",
  "stepDescription": "Processing records...",
  "currentStep": 4,
  "numberOfSteps": 6,
  "currentWorkUnits": 750,
  "currentWorkDescription": "Importing objects...",
  "currentStepTotalWorkUnits": 1000,
  "totalWorkUnits": 1000,
  "actor": "6g2c42d1f6fgd2112cgc66dc",
  "startDate": "2021-04-20T13:57:52.404Z",
  "endDate": null,
  "executionUUID": "b36ebb89-4a75-4df3-9101-f40d2771db32"
}
```

## Import Status Values

Import operations can have the following status values:

- **`PENDING`** - Import is queued and waiting to start
- **`IN_PROGRESS`** - Import is currently running
- **`COMPLETED`** - Import completed successfully
- **`FAILED`** - Import failed with errors
- **`CANCELLED`** - Import was cancelled by user
- **`PAUSED`** - Import is temporarily paused

## Import Steps

Typical import process includes these steps:

1. **Validation** - Validate import configuration and data source
2. **Connection** - Establish connection to data source
3. **Schema Discovery** - Analyze source data structure
4. **Mapping** - Apply field mappings and transformations
5. **Processing** - Import and create/update objects
6. **Completion** - Finalize import and cleanup

## Import Types

Assets supports various import types:

- **CSV Import** - Import from CSV files
- **Database Import** - Import from SQL databases
- **LDAP Import** - Import from LDAP directories
- **REST API Import** - Import from REST endpoints
- **Custom Import** - Custom import configurations

## Field Mapping

Import sources support flexible field mapping:

- **Direct Mapping** - Map source fields directly to object attributes
- **Transformation** - Apply data transformations during import
- **Concatenation** - Combine multiple source fields
- **Conditional Logic** - Apply conditional mappings based on data
- **Default Values** - Set default values for missing data
- **Reference Resolution** - Resolve references to other objects

## Error Handling

Import operations provide comprehensive error handling:

- **Validation Errors** - Configuration and data validation issues
- **Connection Errors** - Data source connectivity problems
- **Mapping Errors** - Field mapping and transformation issues
- **Data Errors** - Invalid or incompatible data values
- **Permission Errors** - Insufficient permissions for operations

## Response Codes

- **200** - Success
- **400** - Bad Request - Invalid import configuration
- **401** - Unauthorized - Authentication required
- **403** - Forbidden - Insufficient permissions
- **404** - Not Found - Import source or execution not found
- **500** - Internal Server Error

## Implementation Notes

- **Import Configurations** must be set up before starting imports
- **Progress Monitoring** is essential for long-running imports
- **Error Logs** provide detailed information about import failures
- **Incremental Imports** can update existing objects without full reload
- **Scheduling** allows for automated recurring imports
- **Rollback** capabilities may be available for failed imports
- **Performance** depends on data volume and complexity of mappings
- **Concurrency** limits may apply to prevent system overload
