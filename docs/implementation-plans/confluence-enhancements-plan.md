# Confluence Enhancements Implementation Plan

## Overview
This plan details the implementation of enhanced Confluence features for the Atlassian MCP Server, following existing code patterns and maintaining consistency with current tools.

## Current Implementation Analysis

### Existing Confluence Tools
- `confluence_search()` - Search pages by title
- `confluence_get_page()` - Get page content by ID  
- `confluence_create_page()` - Create new pages
- `confluence_update_page()` - Update existing pages

### Code Patterns to Follow

#### 1. Method Structure Pattern
```python
async def confluence_method_name(self, param1: str, param2: Optional[int] = None) -> ReturnType:
    """Method description with clear purpose.
    
    Args:
        param1: Description of required parameter
        param2: Description of optional parameter with default
        
    Returns:
        Description of return value
    """
    cloud_id = await self.get_cloud_id()  # Standard cloud ID retrieval
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/endpoint"
    
    # Build params/data as needed
    params = {"param": value, "limit": limit}
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])  # or response.json() for single objects
```

#### 2. Tool Wrapper Pattern
```python
@mcp.tool()
async def confluence_tool_name(param1: str, param2: Optional[int] = None) -> ReturnType:
    """Tool description for MCP interface.
    
    Args:
        param1: Description for users
        param2: Description with default value
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_method_name(param1, param2)
```

#### 3. Error Handling Pattern
- All API calls use `make_request()` which handles:
  - Token refresh on 401 errors
  - Structured error responses with AtlassianError
  - Operation context for debugging
  - Comprehensive logging

#### 4. OAuth Scopes Required
Current scopes for Confluence:
- `read:page:confluence` - Read pages (granular scope for v2 API)
- `read:space:confluence` - Read space info (granular scope for v2 API)
- `write:page:confluence` - Create/update pages (granular scope for v2 API)

Additional scopes needed:
- `read:comment:confluence` - Read comments
- `write:comment:confluence` - Create/update comments
- `read:label:confluence` - Read labels
- `write:label:confluence` - Add/remove labels (if needed)
- `read:attachment:confluence` - Read attachments

## Implementation Plan

### Phase 1: Space Management (High Priority)

#### 1.1 confluence_list_spaces()
**Method Implementation:**
```python
async def confluence_list_spaces(self, limit: int = 25, space_type: Optional[str] = None, status: str = "current") -> List[Dict[str, Any]]:
    """List Confluence spaces with filtering options."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/spaces"
    
    params = {"limit": limit, "status": status}
    if space_type:
        params["type"] = space_type
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

**Tool Wrapper:**
```python
@mcp.tool()
async def confluence_list_spaces(limit: int = 25, space_type: Optional[str] = None, status: str = "current") -> List[Dict[str, Any]]:
    """List Confluence spaces.
    
    Args:
        limit: Maximum number of spaces to return (1-250, default: 25)
        space_type: Filter by type: 'global', 'collaboration', 'knowledge_base', 'personal'
        status: Filter by status: 'current', 'archived' (default: 'current')
    """
    if not atlassian_client or not atlassian_client.config.access_token:
        raise ValueError("Not authenticated. Use authenticate_atlassian tool first.")
    return await atlassian_client.confluence_list_spaces(limit, space_type, status)
```

#### 1.2 confluence_get_space()
**Method Implementation:**
```python
async def confluence_get_space(self, space_id: str, include_icon: bool = False) -> Dict[str, Any]:
    """Get detailed information about a specific space."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/spaces/{space_id}"
    
    params = {"include-icon": include_icon}
    
    response = await self.make_request("GET", url, params=params)
    return response.json()
```

#### 1.3 confluence_get_space_pages()
**Method Implementation:**
```python
async def confluence_get_space_pages(self, space_id: str, limit: int = 25, status: str = "current") -> List[Dict[str, Any]]:
    """Get pages in a specific space."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages"
    
    params = {
        "space-id": space_id,
        "limit": limit,
        "status": status,
        "body-format": "storage"
    }
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

### Phase 2: Enhanced Search & Discovery (High Priority)

#### 2.1 confluence_search_content()
**Method Implementation:**
```python
async def confluence_search_content(self, query: str, limit: int = 25, space_id: Optional[str] = None, content_type: str = "page") -> List[Dict[str, Any]]:
    """Advanced search across Confluence content."""
    cloud_id = await self.get_cloud_id()
    
    if content_type == "page":
        url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages"
        params = {"title": query, "limit": limit, "body-format": "storage"}
    else:
        # Future: support other content types
        url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages"
        params = {"title": query, "limit": limit, "body-format": "storage"}
    
    if space_id:
        params["space-id"] = space_id
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 2.2 confluence_get_page_children()
**Method Implementation:**
```python
async def confluence_get_page_children(self, page_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Get child pages of a specific page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}/children"
    
    params = {"limit": limit, "body-format": "storage"}
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 2.3 confluence_get_page_ancestors()
**Method Implementation:**
```python
async def confluence_get_page_ancestors(self, page_id: str) -> List[Dict[str, Any]]:
    """Get ancestor pages (breadcrumb trail) for a specific page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}/ancestors"
    
    response = await self.make_request("GET", url)
    return response.json().get("results", [])
```

### Phase 3: Comments & Collaboration (Medium Priority)

#### 3.1 confluence_get_page_comments()
**Method Implementation:**
```python
async def confluence_get_page_comments(self, page_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Get comments for a specific page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/footer-comments"
    
    params = {
        "page-id": page_id,
        "limit": limit,
        "body-format": "storage"
    }
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 3.2 confluence_add_comment()
**Method Implementation:**
```python
async def confluence_add_comment(self, page_id: str, comment: str, parent_comment_id: Optional[str] = None) -> Dict[str, Any]:
    """Add a comment to a page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/footer-comments"
    
    data = {
        "pageId": page_id,
        "body": {
            "representation": "storage",
            "value": comment
        }
    }
    
    if parent_comment_id:
        data["parentCommentId"] = parent_comment_id
    
    response = await self.make_request("POST", url, json=data)
    return response.json()
```

#### 3.3 confluence_get_comment()
**Method Implementation:**
```python
async def confluence_get_comment(self, comment_id: str) -> Dict[str, Any]:
    """Get a specific comment by ID."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/footer-comments/{comment_id}"
    
    params = {"body-format": "storage"}
    
    response = await self.make_request("GET", url, params=params)
    return response.json()
```

### Phase 4: Labels & Organization (Medium Priority)

#### 4.1 confluence_get_page_labels()
**Method Implementation:**
```python
async def confluence_get_page_labels(self, page_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Get labels for a specific page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}/labels"
    
    params = {"limit": limit}
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 4.2 confluence_search_by_label()
**Method Implementation:**
```python
async def confluence_search_by_label(self, label_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Find pages with a specific label."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/labels/{label_id}/pages"
    
    params = {"limit": limit, "body-format": "storage"}
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 4.3 confluence_list_labels()
**Method Implementation:**
```python
async def confluence_list_labels(self, limit: int = 25, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all labels with optional filtering."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/labels"
    
    params = {"limit": limit}
    if prefix:
        params["prefix"] = prefix
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

### Phase 5: Attachments (Lower Priority)

#### 5.1 confluence_get_page_attachments()
**Method Implementation:**
```python
async def confluence_get_page_attachments(self, page_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Get attachments for a specific page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}/attachments"
    
    params = {"limit": limit}
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 5.2 confluence_get_attachment()
**Method Implementation:**
```python
async def confluence_get_attachment(self, attachment_id: str) -> Dict[str, Any]:
    """Get details of a specific attachment."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/attachments/{attachment_id}"
    
    response = await self.make_request("GET", url)
    return response.json()
```

### Phase 6: Version History (Lower Priority)

#### 6.1 confluence_get_page_versions()
**Method Implementation:**
```python
async def confluence_get_page_versions(self, page_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Get version history for a page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}/versions"
    
    params = {"limit": limit, "body-format": "storage"}
    
    response = await self.make_request("GET", url, params=params)
    return response.json().get("results", [])
```

#### 6.2 confluence_get_page_version()
**Method Implementation:**
```python
async def confluence_get_page_version(self, page_id: str, version_number: int) -> Dict[str, Any]:
    """Get a specific version of a page."""
    cloud_id = await self.get_cloud_id()
    url = f"https://api.atlassian.com/ex/confluence/{cloud_id}/wiki/api/v2/pages/{page_id}/versions/{version_number}"
    
    params = {"body-format": "storage"}
    
    response = await self.make_request("GET", url, params=params)
    return response.json()
```

## Implementation Guidelines

### 1. File Locations
- **Class methods**: Add to `AtlassianClient` class in `src/atlassian_mcp_server/server.py` around line 554 (after existing Confluence methods)
- **Tool wrappers**: Add after line 1205 (after existing Confluence tools)

### 2. Code Organization
- Group methods by phase/functionality
- Add clear section comments like `# Phase 1: Space Management`
- Maintain alphabetical order within each phase

### 3. Documentation Standards
- Use consistent docstring format matching existing methods
- Include clear parameter descriptions with types and defaults
- Specify return value structure
- Add usage examples in tool descriptions

### 4. Error Handling
- All methods use existing `make_request()` for consistent error handling
- No additional try/catch needed - `make_request()` handles all error scenarios
- Follow existing pattern of returning `response.json()` or `response.json().get("results", [])`

### 5. OAuth Scope Updates
Update the scopes list in the `authenticate()` method (around line 163) to include:
```python
# Confluence - Enhanced scopes for full functionality
"read:page:confluence",              # Read pages
"read:space:confluence",             # Read space info  
"write:page:confluence",             # Create/update pages
"read:comment:confluence",           # Read comments (NEW)
"write:comment:confluence",          # Create comments (NEW)
"read:label:confluence",             # Read labels (NEW)
"read:attachment:confluence",        # Read attachments (NEW)
```

### 6. Testing Strategy
- Test each phase incrementally
- Use existing test patterns from `tests/test_functionality.py`
- Verify OAuth scopes work with new endpoints
- Test error handling scenarios

### 7. Implementation Order
1. **Phase 1**: Space Management (essential for discovery)
2. **Phase 2**: Enhanced Search (improves existing search capabilities)
3. **Phase 3**: Comments (collaboration features)
4. **Phase 4**: Labels (organization features)
5. **Phase 5**: Attachments (file management)
6. **Phase 6**: Version History (audit trail)

## Success Criteria
- All new tools follow existing patterns exactly
- Error handling is consistent with current implementation
- OAuth scopes are properly configured
- Documentation matches existing standards
- Tools integrate seamlessly with current MCP interface
- No breaking changes to existing functionality

## Notes for Implementation
- Use the exact method signatures provided
- Follow the existing cloud_id retrieval pattern
- Maintain the same parameter naming conventions
- Use consistent return type annotations
- Add operation_context to make_request calls for complex operations (optional but recommended for debugging)
