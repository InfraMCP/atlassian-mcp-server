# PyPI Publishing Setup Guide

## 1. Get PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll down to **API tokens** section
3. Click **Add API token**
4. Set **Token name**: `atlassian-mcp-server-github`
5. Set **Scope**: `Entire account` (or specific to this project once published)
6. Click **Add token**
7. **COPY THE TOKEN** - you won't see it again!

## 2. Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Set **Name**: `PYPI_API_TOKEN`
5. Set **Secret**: Paste your PyPI API token
6. Click **Add secret**

## 3. Update Version for Release

Before creating a release, update the version in `pyproject.toml`:

```toml
[project]
name = "atlassian-mcp-server"
version = "0.2.0"  # Update this version
```

## 4. Create a GitHub Release

1. Go to your GitHub repository
2. Click **Releases** → **Create a new release**
3. Click **Choose a tag** → Type new tag (e.g., `v0.2.0`)
4. Set **Release title**: `v0.2.0`
5. Add **Release notes** describing changes
6. Click **Publish release**

## 5. Automatic Publishing

The workflow will automatically:
- ✅ Trigger when you create a GitHub release
- ✅ Build the package using Python build tools
- ✅ Check the package for issues
- ✅ Publish to PyPI using your API token

## 6. Manual Publishing (if needed)

You can also trigger the workflow manually:
1. Go to **Actions** tab in GitHub
2. Click **Publish to PyPI** workflow
3. Click **Run workflow**

## 7. Verify Publication

After the workflow runs:
1. Check the **Actions** tab for workflow status
2. Visit [PyPI](https://pypi.org/project/atlassian-mcp-server/) to see your package
3. Test installation: `pip3 install atlassian-mcp-server`

## 8. Version Management

For future releases:
1. Update version in `pyproject.toml`
2. Commit and push changes
3. Create new GitHub release with matching tag
4. Workflow automatically publishes to PyPI

## Troubleshooting

### Common Issues:
- **"Package already exists"**: Version number must be unique, increment it
- **"Invalid token"**: Check that PYPI_API_TOKEN secret is set correctly
- **"Build failed"**: Check pyproject.toml syntax and dependencies

### First-Time Publishing:
- PyPI may require email verification
- Package name must be unique on PyPI
- Consider using TestPyPI first: https://test.pypi.org/
