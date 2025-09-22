# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned - Service Management Enhancements (0.3.x series)
- **v0.3.1**: Approval workflows and participant management
- **v0.3.2**: SLA monitoring, attachments, and feedback systems

## [0.3.0] - 2025-09-23

### Added
- **Service Management Integration (Phase 1)** - Complete support for Jira Service Management
  - `servicedesk_get_requests()` - Retrieve service desk requests with optional filtering
  - `servicedesk_get_request()` - Get detailed information about specific requests
  - `servicedesk_create_request()` - Create new service desk requests
  - `servicedesk_add_comment()` - Add public or internal comments to requests
  - `servicedesk_get_request_status()` - Get current status of service requests
- Added `write:servicedesk-request` OAuth scope for creating and updating service requests
- Comprehensive test suite for Service Management functionality
- Updated documentation with Service Management tools and examples

### Changed
- Updated OAuth scopes from 9 to 10 total required scopes
- Enhanced README with Service Management usage examples
- Updated implementation status to show Phase 1 completion

### Technical Details
- All Service Management methods follow the same authentication and error handling patterns as existing Jira/Confluence tools
- Uses Jira Service Management REST API v3 endpoints
- Maintains backward compatibility with existing functionality
- Follows minimal permissions principle with only required scopes

## [0.2.0] - 2025-09-22

### Added
- Initial release with Jira and Confluence integration
- Seamless OAuth 2.0 authentication flow with PKCE
- Comprehensive Jira operations (search, create, update, comment)
- Confluence content operations (search, read, create, update)
- Automatic token refresh and credential management

### Security
- PKCE (Proof Key for Code Exchange) implementation
- Minimal required OAuth scopes (9 total)
- Secure credential storage with proper file permissions
- State validation for CSRF protection
