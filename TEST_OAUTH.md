# Atlassian OAuth Test Script

This script validates the OAuth 2.0 flow for Atlassian Cloud APIs based on the [official documentation](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/).

## Prerequisites

1. **Environment Variables** - Set these in your shell:
   ```bash
   export ATLASSIAN_SITE_URL="https://your-domain.atlassian.net"
   export ATLASSIAN_CLIENT_ID="your-oauth-client-id"
   export ATLASSIAN_CLIENT_SECRET="your-oauth-client-secret"
   ```

2. **OAuth App Setup** - In [Atlassian Developer Console](https://developer.atlassian.com/console/myapps/):
   - Create OAuth 2.0 app
   - Set callback URL: `http://localhost:8080/callback`
   - Add scopes: `read:jira-work`, `read:jira-user`, `offline_access`

## Usage

### Step 1: Start OAuth Flow
```bash
python3 test_oauth.py start
```
This will:
- Generate PKCE codes for security
- Open your browser to Atlassian login
- Display the authorization URL

### Step 2: Complete Authentication
After authorizing in the browser, you'll see "This site can't be reached" - this is normal!

Copy the full callback URL from your browser address bar and run:
```bash
python3 test_oauth.py complete 'http://localhost:8080/callback?code=ABC123&state=XYZ789'
```

This will:
- Validate the callback
- Exchange authorization code for tokens
- Save tokens securely

### Step 3: Test API Access
```bash
python3 test_oauth.py test
```

This will test:
- ✅ Get accessible resources
- ✅ Get current user info
- ✅ List Jira projects
- ✅ Search recent issues

## Files Created

- `~/.atlassian_test_session.json` - Temporary OAuth session (auto-deleted)
- `~/.atlassian_test_tokens.json` - Saved access/refresh tokens (600 permissions)

## Troubleshooting

**"No accessible resources found"**
- Check your OAuth app has the right scopes
- Ensure you have access to the Atlassian site

**"Token exchange failed"**
- Verify client ID/secret are correct
- Check callback URL matches exactly: `http://localhost:8080/callback`

**"API calls fail with 401"**
- Tokens may have expired
- Re-run the OAuth flow from step 1
