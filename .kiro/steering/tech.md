# Technology Stack

## Language & Runtime

- **Python**: 3.10+ (minimum 3.10, supports 3.11, 3.12)
- **Package Manager**: pip3
- **Build System**: setuptools with pyproject.toml

## Core Dependencies

- **mcp** (1.14.1): FastMCP framework for MCP server implementation
- **httpx** (0.28.1): Async HTTP client for API requests
- **pydantic** (2.11.9): Data validation and settings management
- **pydantic-settings** (2.10.1): Environment variable configuration

## Development Dependencies

- **pytest** (8.3.3): Testing framework
- **pytest-asyncio** (0.24.0): Async test support
- **black** (24.8.0): Code formatting
- **isort** (5.13.2): Import sorting
- **mypy** (1.0.0+): Type checking
- **pylint**: Code linting

## Security Tools

- **safety** (3.0.0+): Dependency vulnerability scanning
- **pip-audit** (2.6.0+): Additional security auditing

## Common Commands

### Installation
```bash
# Install from PyPI
pip3 install atlassian-mcp-server

# Install from source (development)
pip3 install -e .

# Install with dev dependencies
pip3 install -e ".[dev]"

# Install with security tools
pip3 install -e ".[security]"
```

### Running
```bash
# Run the server
python -m atlassian_mcp_server

# Or directly
python src/atlassian_mcp_server/server.py

# Or via installed command
atlassian-mcp-server
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_functionality.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
pylint src/
```

### Security Scanning
```bash
# Generate dependency report
python scripts/generate_dependency_report.py

# Check for vulnerabilities
safety check
pip-audit

# Update dependencies safely
python scripts/update_dependencies.py
```

### Building & Publishing
```bash
# Build distribution
python -m build

# Upload to PyPI
twine upload dist/*
```

## Configuration

Environment variables required:
- `ATLASSIAN_SITE_URL`: Your Atlassian Cloud site URL
- `ATLASSIAN_CLIENT_ID`: OAuth app client ID
- `ATLASSIAN_CLIENT_SECRET`: OAuth app client secret
- `ATLASSIAN_MODULES` (optional): Comma-separated list of modules to enable (jira,confluence,service_desk)

## Dependency Management

- **All dependencies use exact version pins** for supply chain security
- Dependencies are tracked in `requirements.txt` with pinned versions
- Regular security scanning via GitHub Actions
- Documentation in `docs/DEPENDENCIES.md`
