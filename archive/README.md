# Development Archive

This directory contains development scripts and test files used during the creation of the Atlassian MCP server.

## Development Scripts (`development-scripts/`)

These scripts were used for testing OAuth flows, API functionality, and debugging during development:

- **OAuth Testing**: `oauth_*.py`, `test_oauth*.py` - Various OAuth flow implementations and tests
- **API Testing**: `test_confluence*.py`, `test_jira*.py` - API functionality validation
- **Diagnostics**: `diagnose_*.py`, `test_permissions.py` - Permission and scope debugging
- **Working Demos**: `working_*.py` - Proof-of-concept implementations

## Purpose

These files are preserved for reference in case future development needs to revisit specific implementation details or debugging approaches. They are not part of the production MCP server.

## Usage

These scripts are not intended for production use. Refer to the main `tests/` directory for proper test scripts and the `src/` directory for the production server implementation.
