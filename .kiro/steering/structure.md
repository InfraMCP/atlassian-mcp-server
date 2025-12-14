# Project Structure

## Directory Layout

```
atlassian-mcp-server/
├── src/atlassian_mcp_server/     # Main source code
│   ├── clients/                   # API client implementations
│   │   ├── base_client.py        # Base OAuth client with authentication
│   │   ├── jira_client.py        # Jira-specific operations
│   │   ├── confluence_client.py  # Confluence-specific operations
│   │   └── service_desk_client.py # Service Management operations
│   ├── modules/                   # MCP tool modules
│   │   ├── base.py               # Base module interface
│   │   ├── jira.py               # Jira MCP tools
│   │   ├── confluence.py         # Confluence MCP tools
│   │   └── service_desk.py       # Service Desk MCP tools
│   ├── server.py                 # Main MCP server entry point
│   ├── module_manager.py         # Module loading and registration
│   ├── __init__.py               # Package initialization
│   └── __main__.py               # CLI entry point
├── tests/                         # Test suite
│   ├── test_functionality.py     # Core functionality tests
│   ├── test_oauth.py             # OAuth flow tests
│   └── test_service_management.py # Service desk tests
├── scripts/                       # Utility scripts
│   ├── generate_dependency_report.py
│   └── update_dependencies.py
├── docs/                          # Documentation
│   ├── DEPENDENCIES.md           # Dependency documentation
│   ├── SECURITY_ASSESSMENT.md    # Security analysis
│   ├── api-specs/                # API specifications
│   ├── implementation-plans/     # Feature planning
│   └── ...
├── .github/workflows/            # CI/CD automation
├── pyproject.toml                # Project metadata and build config
├── requirements.txt              # Pinned dependencies
├── .pylintrc                     # Linting configuration
└── README.md                     # Main documentation
```

## Architecture Patterns

### Modular Design

The codebase follows a **modular architecture** with clear separation:

1. **Clients Layer** (`clients/`): Handles API communication and authentication
   - `BaseAtlassianClient`: Core OAuth 2.0 flow, token management, HTTP requests
   - Service-specific clients extend base with specialized methods
   - Each client is independent and reusable

2. **Modules Layer** (`modules/`): Exposes MCP tools to AI assistants
   - Each module wraps a client and registers MCP tools
   - Modules can be independently enabled/disabled via `ATLASSIAN_MODULES` env var
   - All modules inherit from `BaseModule` interface

3. **Server Layer** (`server.py`): Orchestrates initialization and registration
   - Initializes FastMCP server
   - Uses `ModuleManager` to load enabled modules
   - Registers tools and handles errors

### Key Design Principles

- **Separation of Concerns**: Clients handle API logic, modules handle MCP integration
- **Dependency Injection**: Configuration passed to clients and modules
- **Error Handling**: Custom `AtlassianError` converted to `ValueError` for MCP compatibility
- **Async/Await**: All I/O operations use async patterns
- **Decorator Pattern**: `@handle_atlassian_errors` for consistent error handling

## Code Organization Rules

### Import Order
Use `isort` with black profile:
1. Standard library imports
2. Third-party imports (mcp, httpx, pydantic)
3. Local imports (relative imports from package)

### Naming Conventions
- **Files**: snake_case (e.g., `base_client.py`, `module_manager.py`)
- **Classes**: PascalCase (e.g., `BaseAtlassianClient`, `ModuleManager`)
- **Functions/Methods**: snake_case (e.g., `seamless_oauth_flow`, `register_tools`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `ATLASSIAN_CLIENT`, `MODULE_MANAGER`)
- **MCP Tools**: snake_case with service prefix (e.g., `jira_search`, `confluence_get_page`)

### File Patterns
- Each client class in separate file under `clients/`
- Each module class in separate file under `modules/`
- `__init__.py` files export public interfaces
- Tests mirror source structure in `tests/`

## Configuration Files

- **pyproject.toml**: Single source of truth for project metadata, dependencies, and tool configs
- **requirements.txt**: Pinned production dependencies (generated from pyproject.toml)
- **.pylintrc**: Minimal linting config (ignores archive folder)
- **.gitignore**: Standard Python ignores plus environment files

## Adding New Features

### Adding a New Client
1. Create `src/atlassian_mcp_server/clients/new_client.py`
2. Extend `BaseAtlassianClient`
3. Implement service-specific methods
4. Export from `clients/__init__.py`

### Adding a New Module
1. Create `src/atlassian_mcp_server/modules/new_module.py`
2. Extend `BaseModule`
3. Define `required_scopes` list
4. Implement `register_tools()` and `register_resources()`
5. Add to `ModuleManager.available_modules` dict
6. Export from `modules/__init__.py`

### Adding a New Tool
1. Add method to appropriate client class
2. Register as MCP tool in corresponding module using `@mcp.tool()` decorator
3. Use `@handle_atlassian_errors` for error handling
4. Document in README.md under "Available Tools"

## Testing Structure

- Tests are organized by functionality area
- Use `pytest` with async support (`pytest-asyncio`)
- Mock external API calls for unit tests
- Integration tests require real credentials (optional)
