# Attachments API

## Overview
The Attachments API provides comprehensive file management capabilities for Jira issues, including uploading, downloading, metadata retrieval, and archive content inspection. This API supports OAuth 2.0 authentication and follows Jira's permission model for secure file access.

## OAuth 2.0 Scopes

### Required Scopes
- **`read:jira-work`** - Read attachment metadata, download content, and view thumbnails
- **`write:jira-work`** - Upload attachments to issues and delete attachments

### Beta Scopes (Alternative)
- **`read:attachment:jira`** - Read attachment content and metadata
- **`write:attachment:jira`** - Upload attachments to issues
- **`delete:attachment:jira`** - Delete attachments from issues

## Endpoints

### Attachment Management

#### POST /rest/api/3/issue/{issueIdOrKey}/attachments
**Description**: Upload one or more files as attachments to an issue  
**OAuth Scopes**: `write:jira-work`  
**Parameters**:
- `issueIdOrKey` (path, required): Issue ID or key to attach files to
- `file` (form-data, required): One or more files to upload

**Headers Required**:
- `X-Atlassian-Token: no-check` - Required to prevent CSRF attacks
- `Content-Type: multipart/form-data`

**Response**: Array of attachment metadata objects
```json
[
  {
    "id": "10001",
    "filename": "picture.jpg",
    "author": {
      "accountId": "5b10a2844c20165700ede21g",
      "displayName": "Mia Krystof",
      "emailAddress": "mia@example.com"
    },
    "created": "2022-05-01T12:34:56.000+0000",
    "size": 23123,
    "mimeType": "image/jpeg",
    "content": "https://your-domain.atlassian.net/rest/api/3/attachment/content/10001",
    "thumbnail": "https://your-domain.atlassian.net/rest/api/3/attachment/thumbnail/10001",
    "self": "https://your-domain.atlassian.net/rest/api/3/attachments/10001"
  }
]
```

**Error Codes**:
- `403` - User lacks attachment creation permissions
- `404` - Issue not found or no view permission
- `413` - File too large, too many files (>60), or per-issue limit exceeded

**Example**:
```bash
curl -X POST \
  "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/attachments" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@document.pdf" \
  -F "file=@screenshot.png"
```

#### DELETE /rest/api/3/attachment/{id}
**Description**: Delete an attachment from an issue  
**OAuth Scopes**: `write:jira-work`  
**Parameters**:
- `id` (path, required): Attachment ID to delete

**Response**: 204 No Content on success

**Error Codes**:
- `403` - User lacks delete permission (requires "Delete own attachments" or "Delete all attachments")
- `404` - Attachment not found or attachments disabled

**Example**:
```bash
curl -X DELETE \
  "https://your-domain.atlassian.net/rest/api/3/attachment/10001" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Attachment Metadata

#### GET /rest/api/3/attachment/{id}
**Description**: Get metadata for a specific attachment (not the file content)  
**OAuth Scopes**: `read:jira-work`  
**Parameters**:
- `id` (path, required): Attachment ID

**Response**: Attachment metadata object
```json
{
  "id": 10000,
  "filename": "picture.jpg",
  "author": {
    "accountId": "5b10a2844c20165700ede21g",
    "displayName": "Mia Krystof",
    "active": false,
    "avatarUrls": {
      "48x48": "https://avatar-management--avatars.server-location.prod.public.atl-paas.net/initials/MK-5.png?size=48&s=48"
    }
  },
  "created": "2022-10-06T07:32:47.000+0000",
  "size": 23123,
  "mimeType": "image/jpeg",
  "content": "https://your-domain.atlassian.net/jira/rest/api/3/attachment/content/10000",
  "thumbnail": "https://your-domain.atlassian.net/jira/rest/api/3/attachment/thumbnail/10000",
  "self": "https://your-domain.atlassian.net/rest/api/3/attachments/10000"
}
```

**Error Codes**:
- `401` - Authentication required
- `403` - No permission to view attachment
- `404` - Attachment not found or attachments disabled

#### GET /rest/api/3/attachment/meta
**Description**: Get Jira instance attachment settings and limits  
**OAuth Scopes**: `read:jira-work`  
**Parameters**: None

**Response**: Attachment settings
```json
{
  "enabled": true,
  "uploadLimit": 1000000
}
```

**Example**:
```bash
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/attachment/meta" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Attachment Content

#### GET /rest/api/3/attachment/content/{id}
**Description**: Download attachment file content with optional range support  
**OAuth Scopes**: `read:jira-work`  
**Parameters**:
- `id` (path, required): Attachment ID
- `redirect` (query, optional): Whether to redirect to download URL (default: true)

**Headers**:
- `Range` (optional): HTTP range header for partial content downloads

**Response**: 
- `200` - File content (when redirect=false)
- `206` - Partial content (when Range header used and redirect=false)
- `303` - Redirect to download URL (when redirect=true)

**Error Codes**:
- `400` - Malformed Range header
- `401` - Authentication required
- `403` - No permission to view attachment
- `404` - Attachment not found
- `416` - Range not satisfiable

**Example**:
```bash
# Direct download
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/attachment/content/10001?redirect=false" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o downloaded-file.pdf

# Partial download (first 1024 bytes)
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/attachment/content/10001?redirect=false" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Range: bytes=0-1023"
```

#### GET /rest/api/3/attachment/thumbnail/{id}
**Description**: Get thumbnail image for an attachment  
**OAuth Scopes**: `read:jira-work`  
**Parameters**:
- `id` (path, required): Attachment ID
- `redirect` (query, optional): Whether to redirect to thumbnail URL (default: true)
- `fallbackToDefault` (query, optional): Return default thumbnail if specific one unavailable (default: true)
- `width` (query, optional): Maximum thumbnail width
- `height` (query, optional): Maximum thumbnail height

**Response**:
- `200` - Thumbnail image (when redirect=false)
- `303` - Redirect to thumbnail URL (when redirect=true)

**Error Codes**:
- `400` - Invalid request parameters
- `401` - Authentication required
- `403` - No permission to view attachment
- `404` - Attachment not found or thumbnail unavailable (when fallbackToDefault=false)

**Example**:
```bash
curl -X GET \
  "https://your-domain.atlassian.net/rest/api/3/attachment/thumbnail/10001?width=200&height=200" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Archive Content Inspection

#### GET /rest/api/3/attachment/{id}/expand/human
**Description**: Get human-readable metadata for archive contents (ZIP files)  
**OAuth Scopes**: `read:jira-work`  
**Parameters**:
- `id` (path, required): Attachment ID of archive file

**Response**: Archive metadata with readable file sizes
```json
{
  "id": 7237823,
  "name": "images.zip",
  "mediaType": "application/zip",
  "totalEntryCount": 39,
  "entries": [
    {
      "index": 0,
      "label": "MG00N067.JPG",
      "path": "MG00N067.JPG",
      "mediaType": "image/jpeg",
      "size": "119 kB"
    },
    {
      "index": 1,
      "label": "Allegro from Duet in C Major.mp3",
      "path": "Allegro from Duet in C Major.mp3",
      "mediaType": "audio/mpeg",
      "size": "1.36 MB"
    }
  ]
}
```

**Error Codes**:
- `401` - Authentication required
- `403` - No permission to view attachment
- `404` - Attachment not found
- `409` - File is not a supported archive format

#### GET /rest/api/3/attachment/{id}/expand/raw
**Description**: Get machine-readable metadata for archive contents (ZIP files)  
**OAuth Scopes**: `read:jira-work`  
**Parameters**:
- `id` (path, required): Attachment ID of archive file

**Response**: Archive metadata with byte sizes
```json
{
  "totalEntryCount": 24,
  "entries": [
    {
      "entryIndex": 0,
      "name": "Allegro from Duet in C Major.mp3",
      "mediaType": "audio/mpeg",
      "size": 1430174
    },
    {
      "entryIndex": 1,
      "name": "lrm.rtf",
      "mediaType": "text/rtf",
      "size": 331
    }
  ]
}
```

**Use Case**: Processing archive contents programmatically without displaying to users

## Use Cases

### File Upload Workflow
```javascript
// 1. Check attachment settings
const settings = await fetch('/rest/api/3/attachment/meta', {
  headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json());

if (!settings.enabled) {
  throw new Error('Attachments disabled');
}

// 2. Upload files to issue
const formData = new FormData();
formData.append('file', fileBlob, 'document.pdf');

const attachments = await fetch('/rest/api/3/issue/PROJ-123/attachments', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'X-Atlassian-Token': 'no-check'
  },
  body: formData
}).then(r => r.json());

console.log('Uploaded:', attachments[0].filename);
```

### Archive Content Analysis
```javascript
// Get archive contents for processing
const archiveContents = await fetch('/rest/api/3/attachment/10001/expand/raw', {
  headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json());

// Process each file in the archive
for (const entry of archiveContents.entries) {
  if (entry.mediaType.startsWith('image/')) {
    console.log(`Found image: ${entry.name} (${entry.size} bytes)`);
  }
}
```

### Attachment Management
```javascript
// Get attachment metadata
const attachment = await fetch('/rest/api/3/attachment/10001', {
  headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.json());

// Download attachment content
const content = await fetch(attachment.content + '?redirect=false', {
  headers: { 'Authorization': 'Bearer ' + token }
}).then(r => r.blob());

// Delete attachment if needed
await fetch('/rest/api/3/attachment/10001', {
  method: 'DELETE',
  headers: { 'Authorization': 'Bearer ' + token }
});
```

## Best Practices

### Upload Optimization
- **Check limits first**: Always verify `attachment/meta` before uploading
- **Use multipart/form-data**: Required for file uploads
- **Include CSRF header**: `X-Atlassian-Token: no-check` is mandatory
- **Batch uploads**: Upload multiple files in single request when possible
- **Handle 413 errors**: Implement file size validation and chunking for large files

### Download Efficiency
- **Use redirects**: Default `redirect=true` is more efficient for direct downloads
- **Range requests**: Use HTTP Range header for large file streaming
- **Thumbnail optimization**: Specify width/height parameters to reduce bandwidth
- **Cache thumbnails**: Thumbnail URLs are stable and can be cached

### Permission Handling
- **Graceful degradation**: Handle 403 errors by hiding attachment features
- **Check issue permissions**: Attachment access follows issue-level security
- **Respect privacy**: Private comment attachments have additional restrictions

### Archive Processing
- **Use appropriate endpoint**: `/expand/human` for UI display, `/expand/raw` for processing
- **Handle unsupported formats**: Only ZIP archives are currently supported
- **Limit processing**: Large archives may have many entries

## Error Handling

### Common Error Patterns
```javascript
async function uploadAttachment(issueKey, file) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`/rest/api/3/issue/${issueKey}/attachments`, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'X-Atlassian-Token': 'no-check'
      },
      body: formData
    });
    
    if (response.status === 413) {
      throw new Error('File too large or too many files');
    }
    
    if (response.status === 403) {
      throw new Error('No permission to add attachments');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Upload failed:', error.message);
    throw error;
  }
}
```

## Related APIs
- **[Issues API](issues-api.md)** - Issue attachment lists and metadata
- **[Comments API](comments-api.md)** - Comment-level attachment restrictions
- **[Permissions API](permissions-api.md)** - Attachment permission validation
- **[Users API](users-api.md)** - Attachment author information
