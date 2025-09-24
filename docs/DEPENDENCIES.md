# Dependency Security Report

Generated: 2025-09-24T09:50:26.832972

## Core Dependencies

### mcp v1.14.1
- **Summary**: Model Context Protocol SDK
- **License**: MIT
- **Homepage**: https://modelcontextprotocol.io
- **Dependencies**: anyio, httpx, httpx-sse, jsonschema, pydantic, pydantic-settings, python-multipart, sse-starlette, starlette, uvicorn

### httpx v0.28.1
- **Summary**: The next generation HTTP client.
- **License**: BSD-3-Clause
- **Homepage**: https://github.com/encode/httpx
- **Dependencies**: anyio, certifi, httpcore, idna

### pydantic v2.11.9
- **Summary**: Data validation using Python type hints
- **License**: 
- **Homepage**: https://github.com/pydantic/pydantic
- **Dependencies**: annotated-types, pydantic-core, typing-extensions, typing-inspection

### pydantic-settings v2.10.1
- **Summary**: Settings management using Pydantic
- **License**: 
- **Homepage**: https://github.com/pydantic/pydantic-settings
- **Dependencies**: pydantic, python-dotenv, typing-inspection

## Security Guidelines

- Review this report when security vulnerabilities are announced
- Update dependencies regularly but test thoroughly
- Monitor security advisories for listed packages
- Consider using tools like safety or pip-audit for vulnerability scanning

## All Installed Packages (89 total)

| Package | Version |
|---------|----------|
| Authlib | 1.6.0 |
| Jinja2 | 3.1.6 |
| MarkupSafe | 3.0.2 |
| PyMuPDF | 1.26.4 |
| PyNaCl | 1.6.0 |
| PyPDF2 | 3.0.1 |
| PyYAML | 6.0.2 |
| Pygments | 2.19.2 |
| annotated-types | 0.7.0 |
| ansible | 11.8.0 |
| ansible-compat | 25.6.0 |
| ansible-core | 2.18.7 |
| ansible-lint | 25.6.1 |
| anyio | 4.10.0 |
| atlassian-mcp-server | 0.3.1 |
| attrs | 25.3.0 |
| bcrypt | 4.3.0 |
| beautifulsoup4 | 4.13.4 |
| black | 25.1.0 |
| bracex | 2.6 |
| certifi | 2025.8.3 |
| cffi | 1.17.1 |
| charset-normalizer | 3.4.2 |
| click | 8.3.0 |
| crowdstrike-falconpy | 1.5.4 |
| cryptography | 45.0.5 |
| cyclopts | 3.22.2 |
| dnspython | 2.7.0 |
| docstring_parser | 0.16 |
| docutils | 0.21.2 |
| email_validator | 2.2.0 |
| exceptiongroup | 1.3.0 |
| falcon-mcp | 0.3.0 |
| fastmcp | 2.10.5 |
| filelock | 3.18.0 |
| foreman-mcp-server | 0.2.0 |
| h11 | 0.16.0 |
| httpcore | 1.0.9 |
| httpx | 0.28.1 |
| httpx-sse | 0.4.1 |
| idna | 3.10 |
| importlib_metadata | 8.7.0 |
| invoke | 2.2.0 |
| jsonschema | 4.25.1 |
| jsonschema-specifications | 2025.9.1 |
| lxml | 6.0.0 |
| markdown-it-py | 3.0.0 |
| mcp | 1.14.1 |
| mdurl | 0.1.2 |
| mypy_extensions | 1.1.0 |
| openapi-pydantic | 0.5.1 |
| packaging | 25.0 |
| paramiko | 4.0.0 |
| pathspec | 0.12.1 |
| pip | 25.2 |
| platformdirs | 4.3.8 |
| pycparser | 2.22 |
| pydantic | 2.11.9 |
| pydantic-settings | 2.10.1 |
| pydantic_core | 2.33.2 |
| pyperclip | 1.9.0 |
| pyspnego | 0.12.0 |
| python-dotenv | 1.1.1 |
| python-multipart | 0.0.20 |
| pyvmomi | 9.0.0.0 |
| pywinrm | 0.5.0 |
| referencing | 0.36.2 |
| requests | 2.32.4 |
| requests_ntlm | 1.3.0 |
| resolvelib | 1.0.1 |
| rich | 14.0.0 |
| rich-rst | 1.3.1 |
| rpds-py | 0.27.1 |
| ruamel.yaml | 0.18.14 |
| ruamel.yaml.clib | 0.2.12 |
| sniffio | 1.3.1 |
| soupsieve | 2.7 |
| sse-starlette | 3.0.2 |
| ssh-mcp-server | 0.1.0 |
| starlette | 0.48.0 |
| subprocess-tee | 0.4.2 |
| typing-inspection | 0.4.1 |
| typing_extensions | 4.15.0 |
| urllib3 | 2.5.0 |
| uvicorn | 0.36.0 |
| wcmatch | 10.1 |
| xmltodict | 1.0.0 |
| yamllint | 1.37.1 |
| zipp | 3.23.0 |
