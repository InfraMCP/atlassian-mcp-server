# Git & GitHub Workflow

## Automation Philosophy

**Full automation required** - Use GitHub MCP tools for all operations. Never ask user to manually create branches, commits, or PRs.

## Branch Naming

Format: `<type>/<short-description>` (kebab-case, 3-5 words max)

- `feature/` - New features
- `fix/` or `bugfix/` - Bug fixes  
- `hotfix/` - Critical fixes
- `chore/` - Maintenance tasks
- `docs/` - Documentation updates

Always branch from `main`, never commit directly to it.

## Commit Messages

Format: `<type>(<scope>): <subject>\n\n<body>\n\n<footer>`

**Types**: feat, fix, docs, style, refactor, perf, test, chore, ci

**Rules**:
- Subject: ≤50 chars, imperative mood ("add" not "added")
- Body: Explain what and why, wrap at 72 chars
- Footer: Reference issues ("Closes #123", "Fixes #123")
- Be specific, avoid vague messages

**Example**:
```
feat(confluence): add label management tools

Add tools for getting, searching, and managing page labels including
confluence_get_page_labels and confluence_search_by_label methods.

Closes #42
```

## Pull Request Workflow

**Automated steps**:
1. Create branch: `mcp_github_create_branch`
2. Push changes: `mcp_github_push_files` (with commit message)
3. Create PR: `mcp_github_create_pull_request` (with description)

**PR Title**: Same format as commit messages (e.g., `feat(confluence): add label tools`)

**PR Description**:
```markdown
## Description
[What this PR does]

## Changes Made
- [Change 1]
- [Change 2]

## Type of Change
- [ ] Bug fix / [ ] New feature / [ ] Breaking change / [ ] Documentation

## Related Issues
Closes #[number]
```

Keep PRs focused (one feature/fix), small (<500 lines), and always link issues.

## GitHub MCP Tools

**Primary tools**:
- `mcp_github_create_branch` - Create branches
- `mcp_github_push_files` - Push commits
- `mcp_github_create_pull_request` - Create PRs
- `mcp_github_get_file_contents` - Check file state
- `mcp_github_create_issue` / `mcp_github_update_issue` - Issue management

## Repository Info

- **Owner**: `rorymcmahon` (or `InfraMCP`)
- **Repo**: `atlassian-mcp-server`
- **Default branch**: `main`

## Pre-Push Checks

Run before pushing: `black src/ tests/`, `isort src/ tests/`, `pylint src/`, `pytest`

## Critical Rules

**DO**:
- ✅ Auto-create branches and PRs using GitHub MCP tools
- ✅ Write detailed conventional commit messages
- ✅ Reference issues in commits/PRs
- ✅ Include complete PR descriptions

**DON'T**:
- ❌ Ask user to manually create branches/PRs
- ❌ Commit directly to main
- ❌ Use vague commit messages
- ❌ Push without meaningful messages
- ❌ Commit secrets or credentials
