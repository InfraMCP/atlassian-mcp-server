# Jira Granular Scopes

This document lists all available granular scopes for Jira applications in the Atlassian developer console.

## Comment Information

| Scope | Description |
|-------|-------------|
| `read:comment-info:jira` | Allows the app to read comment information |
| `write:comment-info:jira` | Allows the app to write comment information |
| `delete:comment-info:jira` | Allows the app to delete comment information |

## Project Information

| Scope | Description |
|-------|-------------|
| `read:project-info:jira` | Allows the app to read project information |
| `write:project-info:jira` | Allows the app to write project information |
| `delete:project-info:jira` | Allows the app to delete project information |

## Deployment Information

| Scope | Description |
|-------|-------------|
| `read:deployment-info:jira` | Allows the app to read deployment information |
| `write:deployment-info:jira` | Allows the app to write deployment information |
| `delete:deployment-info:jira` | Allows the app to delete deployment information |

## Development Information

| Scope | Description |
|-------|-------------|
| `read:dev-info:jira` | Allows the app to read development information (commits, branches, pull-requests) |
| `write:dev-info:jira` | Allows the app to write development information (commits, branches, pull-requests) |
| `delete:dev-info:jira` | Allows the app to delete development information (commits, branches, pull-requests) |

## Document Information

| Scope | Description |
|-------|-------------|
| `read:document-info:jira` | Allows the app to read documents information |
| `write:document-info:jira` | Allows the app to write documents information |
| `delete:document-info:jira` | Allows the app to delete documents information |

## Feature Flag Information

| Scope | Description |
|-------|-------------|
| `read:feature-flag-info:jira` | Allows the app to read feature-flag information |
| `write:feature-flag-info:jira` | Allows the app to write feature-flag information |
| `delete:feature-flag-info:jira` | Allows the app to delete feature-flag information |

## Operations Information

| Scope | Description |
|-------|-------------|
| `read:operations-info:jira` | Allows the app to read operations information |
| `write:operations-info:jira` | Allows the app to write operations information |
| `delete:operations-info:jira` | Allows the app to delete operations information |

## Remote Link Information

| Scope | Description |
|-------|-------------|
| `read:remote-link-info:jira` | Allows the app to read remote-link information |
| `write:remote-link-info:jira` | Allows the app to write remote-link information |
| `delete:remote-link-info:jira` | Allows the app to delete remote-link information |

## Security Information

| Scope | Description |
|-------|-------------|
| `read:security:jira` | Allows the app to read security information |
| `write:security:jira` | Allows the app to write security information |
| `delete:security:jira` | Allows the app to delete security information |

## DevOps Component Information

| Scope | Description |
|-------|-------------|
| `read:devops-component-info:jira` | Allows the app to read devops component information |
| `write:devops-component-info:jira` | Allows the app to write devops component information |
| `delete:devops-component-info:jira` | Allows the app to delete devops component information |

## Assets (CMDB) - Import Configuration

| Scope | Description |
|-------|-------------|
| `import:import-configuration:cmdb` | Allow to read and update import structure and import data into Assets |
| `import:cmdb-import-configuration:jira` | Allow the app to read import structure and import data into Assets |

## Assets (CMDB) - Objects

| Scope | Description |
|-------|-------------|
| `read:cmdb-object:jira` | Read Assets objects, their attributes values and details |
| `write:cmdb-object:jira` | Create or update Assets objects, their attributes values and details |
| `delete:cmdb-object:jira` | Allow the app to delete Objects from Assets |

## Assets (CMDB) - Schemas

| Scope | Description |
|-------|-------------|
| `read:cmdb-schema:jira` | Get list of or details of individual schemas in Assets |
| `write:cmdb-schema:jira` | Create new schemas or update details of existing schemas in Assets |
| `delete:cmdb-schema:jira` | Delete Assets schemas |

## Assets (CMDB) - Object Types

| Scope | Description |
|-------|-------------|
| `read:cmdb-type:jira` | Read Assets object types and their attributes |
| `write:cmdb-type:jira` | Create or update Assets object types and their attributes |
| `delete:cmdb-type:jira` | Delete Assets object types |

## Assets (CMDB) - Attributes

| Scope | Description |
|-------|-------------|
| `read:cmdb-attribute:jira` | Get list of all Assets object type attributes for a schema or an object type |
| `write:cmdb-attribute:jira` | Create or update Assets object type attributes |
| `delete:cmdb-attribute:jira` | Delete Assets object type attributes |

## Assets (CMDB) - Icons

| Scope | Description |
|-------|-------------|
| `read:cmdb-icon:jira` | Get an Assets icon details or list of globally defined icons |

## Assets (CMDB) - Configuration

| Scope | Description |
|-------|-------------|
| `read:cmdb-config:jira` | Read Assets configuration |
| `write:cmdb-config:jira` | Create or update Assets configuration |
| `delete:cmdb-config:jira` | Delete Assets configuration |

## App Data

| Scope | Description |
|-------|-------------|
| `read:app-data:jira` | Read connect app properties data |
| `write:app-data:jira` | Create, modify and delete app properties data |

## User Information

| Scope | Description |
|-------|-------------|
| `read:email-address:jira` | View email addresses of all users regardless of the user's profile visibility settings |

## Airtrack/Data Manager

| Scope | Description |
|-------|-------------|
| `read:airtrack-object:jira` | Allow the app to read Objects from Airtrack/Data Manager |
| `write:airtrack-object:jira` | Allow the app to change Objects from Airtrack/Data Manager |

## Jira Service Management - Operations Configuration

| Scope | Description |
|-------|-------------|
| `read:ops-config:jira-service-management` | Read configuration of operations including contacts, custom user roles, escalations, forwarding rules, heartbeats, integrations, maintenances, notification rules, routing rules, schedules, on-calls, and syncs |
| `write:ops-config:jira-service-management` | Create and edit configuration of operations including contacts, custom user roles, escalations, forwarding rules, heartbeats, integrations, maintenances, notification rules, routing rules, schedules, on-calls, and syncs |
| `delete:ops-config:jira-service-management` | Delete configuration of operations including contacts, custom user roles, escalations, forwarding rules, heartbeats, integrations, maintenance, notification rules, routing rules, schedules, on-calls, syncs |

## Jira Service Management - Operations Alerts

| Scope | Description |
|-------|-------------|
| `read:ops-alert:jira-service-management` | Read operations alert data, including request status, alert logs, and listing and searching for alerts |
| `write:ops-alert:jira-service-management` | Create and edit alerts, including status, description, priority, attachments, tags, and notes |
| `delete:ops-alert:jira-service-management` | Delete the alerts |

## Work Item Information

| Scope | Description |
|-------|-------------|
| `read:work-item-info:jira` | Allows the app to read Work Item information |
| `write:work-item-info:jira` | Allows the app to write Work Item information |
| `delete:work-item-info:jira` | Allows the app to delete Work Item information |

## Jira Service Management - Mail Logs

| Scope | Description |
|-------|-------------|
| `read:mail-logs.processing:jira-service-management` | Allows the user to read incoming email processing logs |
| `read:mail-logs.connectivity:jira-service-management` | Allows the user to read email connectivity logs |

## Team Work Graph

| Scope | Description |
|-------|-------------|
| `read:object:jira` | Allows the user to view objects in the Team Work Graph |
| `write:object:jira` | Allows the user to create and update objects in the Team Work Graph |
| `delete:object:jira` | Allows the user to delete objects in the Team Work Graph |