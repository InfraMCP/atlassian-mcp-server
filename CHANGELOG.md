# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.3] - 2025-12-15

### Security
- 🔒 **CRITICAL**: Fixed MCP vulnerability (ID 82197) - Information Disclosure via HTTP-based localhost MCP
- Updated `mcp` dependency from 1.14.1 to 1.24.0 to resolve security vulnerability
- Verified full compatibility with existing codebase - no breaking changes

### Changed
- Bumped project version to reflect security patch

## [0.3.3] - 2024-09-26

### Fixed
- 🚨 **CRITICAL**: Fixed URL protocol error that was breaking all API operations after authentication
- Fixed malformed base URL definitions in AtlassianClient initialization
- Resolved "Request URL is missing http/https protocol" error affecting all API calls

### Added
- MIT License file
- Comprehensive pylint configuration (.pylintrc)
- Helper methods for confluence page operations to reduce complexity
- Dedicated CHANGELOG.md following Keep a Changelog format

### Changed
- Achieved 10.00/10 pylint rating with comprehensive code quality improvements
- Refactored `confluence_create_page` method to reduce local variables
- Improved error handling and code structure
- Enhanced documentation with troubleshooting guides

### Removed
- Obsolete `server_old.py` file that was causing code quality issues

## [Unreleased]

## [0.3.2] - 2024-09-24

### Added
- Enhanced Service Management API support with comprehensive tools
- Discovery tools for service desks and request types
- Approval and participant management for service requests
- SLA tracking and knowledge base search capabilities
- Comprehensive Confluence v2 API integration
- Space management, comments, labels, and attachments support
- Version history and enhanced search capabilities

### Changed
- Migrated to Confluence v2 API for better performance and future-proofing
- Updated to use granular OAuth scopes for improved security
- Enhanced error handling with structured error responses
- Improved documentation with detailed scope requirements

### Fixed
- OAuth token refresh mechanism
- API endpoint compatibility issues
- Scope validation and error reporting

## [0.3.1] - 2024-09-20

### Added
- Basic Service Management API integration
- Service desk request creation and management
- Enhanced Confluence page creation capabilities

### Fixed
- Authentication flow improvements
- Token persistence issues

## [0.3.0] - 2024-09-18

### Added
- Seamless OAuth 2.0 authentication with PKCE security
- Automatic browser-based authentication flow
- Comprehensive Jira API integration (search, create, update, comment)
- Basic Confluence API integration (search, read content)
- Automatic token refresh and management
- Structured error handling for AI agent consumption

### Changed
- Complete rewrite using modern MCP framework
- Improved security with minimal required permissions
- Enhanced user experience with automatic authentication

## [0.2.0] - 2024-09-15

### Added
- Initial MCP server implementation
- Basic Atlassian Cloud connectivity
- OAuth 2.0 authentication support

## [0.1.0] - 2024-09-10

### Added
- Project initialization
- Basic project structure and dependencies
- Initial documentation

[Unreleased]: https://github.com/rorymcmahon/atlassian-mcp-server/compare/v0.3.3...HEAD
[0.3.3]: https://github.com/rorymcmahon/atlassian-mcp-server/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/rorymcmahon/atlassian-mcp-server/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/rorymcmahon/atlassian-mcp-server/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/rorymcmahon/atlassian-mcp-server/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/rorymcmahon/atlassian-mcp-server/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/rorymcmahon/atlassian-mcp-server/releases/tag/v0.1.0
