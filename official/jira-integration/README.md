# Jira Integration Plugin

Official Jira integration plugin for [Dev Orchestrator MCP](https://github.com/chaos-consultant/dev-orchestrator-mcp).

## Overview

This plugin provides comprehensive Jira integration, allowing you to create, update, search, and manage Jira issues directly from Claude Code or the Dev Orchestrator dashboard.

## Features

- 🔍 **Search Issues** - Search using JQL (Jira Query Language)
- 📝 **Create Issues** - Create new bugs, tasks, stories, and more
- ✏️ **Update Issues** - Modify existing issues
- 💬 **Comments** - Add comments to issues
- 🔄 **Transitions** - Change issue status (To Do → In Progress → Done)
- 📋 **Project Management** - List and manage projects
- 🔐 **Secure Authentication** - API token-based authentication

## Installation

### Via Dev Orchestrator Dashboard

1. Open the Dev Orchestrator dashboard at http://localhost:3333
2. Navigate to **Plugins** in the sidebar
3. Click **Install Plugin**
4. Enter the Git URL:
   ```
   https://github.com/chaos-consultant/dev-orchestrator-plugins.git#official/jira-integration
   ```
5. Follow the configuration prompts

### Manual Installation

```bash
# Clone the plugins repository
git clone https://github.com/chaos-consultant/dev-orchestrator-plugins.git
cd dev-orchestrator-plugins/official/jira-integration

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Jira credentials
```

## Configuration

### Get Your Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**
3. Give it a name (e.g., "Dev Orchestrator")
4. Copy the generated token

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Your Jira instance URL
JIRA_URL=https://your-company.atlassian.net

# Your Jira account email
JIRA_EMAIL=your-email@example.com

# Your API token (NOT your password)
JIRA_API_TOKEN=your-api-token-here
```

## Usage Examples

### Search Issues

```python
# Search for open bugs in a project
jira_search_issues(
    jql="project = MYPROJ AND status = Open AND type = Bug",
    max_results=10
)

# Search for issues assigned to you
jira_search_issues(
    jql="assignee = currentUser() AND status != Done"
)

# Search with specific fields
jira_search_issues(
    jql="project = MYPROJ",
    fields=["summary", "status", "assignee"]
)
```

### Create Issue

```python
# Create a bug
jira_create_issue(
    project="MYPROJ",
    summary="Login button not working",
    description="Users report that clicking the login button does nothing",
    issue_type="Bug",
    priority="High",
    labels=["frontend", "critical"]
)

# Create a story with assignee
jira_create_issue(
    project="MYPROJ",
    summary="Add dark mode support",
    description="Implement dark mode theme for the dashboard",
    issue_type="Story",
    assignee="john.doe@example.com"
)
```

### Get Issue Details

```python
# Get basic info
jira_get_issue(issue_key="MYPROJ-123")

# Get with comments and changelog
jira_get_issue(
    issue_key="MYPROJ-123",
    expand=["comments", "changelog"]
)
```

### Update Issue

```python
# Update summary and priority
jira_update_issue(
    issue_key="MYPROJ-123",
    summary="Updated issue title",
    priority="High"
)

# Reassign issue
jira_update_issue(
    issue_key="MYPROJ-123",
    assignee="jane.smith@example.com"
)

# Add labels
jira_update_issue(
    issue_key="MYPROJ-123",
    labels=["needs-review", "frontend"]
)
```

### Add Comment

```python
jira_add_comment(
    issue_key="MYPROJ-123",
    comment="I've investigated this issue and found the root cause in the authentication module."
)
```

### Transition Issue (Change Status)

```python
# First, check available transitions
jira_get_transitions(issue_key="MYPROJ-123")

# Then transition to a new status
jira_transition_issue(
    issue_key="MYPROJ-123",
    transition="In Progress",
    comment="Starting work on this issue"
)

# Mark as done
jira_transition_issue(
    issue_key="MYPROJ-123",
    transition="Done"
)
```

### List Projects

```python
# List all accessible projects
jira_list_projects()

# Include archived projects
jira_list_projects(include_archived=True)
```

## Tools Reference

### jira_search_issues
Search for issues using JQL.

**Parameters:**
- `jql` (string, required): JQL query string
- `max_results` (integer, optional): Maximum results (default: 50)
- `fields` (array, optional): Specific fields to return

### jira_get_issue
Get detailed information about a specific issue.

**Parameters:**
- `issue_key` (string, required): Issue key (e.g., "PROJ-123")
- `expand` (array, optional): Additional data to expand (e.g., ["comments", "changelog"])

### jira_create_issue
Create a new issue.

**Parameters:**
- `project` (string, required): Project key
- `summary` (string, required): Issue title
- `issue_type` (string, required): Issue type (Bug, Story, Task, etc.)
- `description` (string, optional): Issue description
- `priority` (string, optional): Priority level
- `assignee` (string, optional): Username or email
- `labels` (array, optional): Issue labels

### jira_update_issue
Update an existing issue.

**Parameters:**
- `issue_key` (string, required): Issue key
- `summary` (string, optional): New title
- `description` (string, optional): New description
- `priority` (string, optional): New priority
- `assignee` (string, optional): New assignee
- `labels` (array, optional): New labels

### jira_add_comment
Add a comment to an issue.

**Parameters:**
- `issue_key` (string, required): Issue key
- `comment` (string, required): Comment text (supports Jira markdown)

### jira_transition_issue
Change the status of an issue.

**Parameters:**
- `issue_key` (string, required): Issue key
- `transition` (string, required): Transition name or ID
- `comment` (string, optional): Comment when transitioning

### jira_get_transitions
Get available status transitions for an issue.

**Parameters:**
- `issue_key` (string, required): Issue key

### jira_list_projects
List all accessible projects.

**Parameters:**
- `include_archived` (boolean, optional): Include archived projects (default: false)

## JQL (Jira Query Language) Examples

```jql
# Find all bugs assigned to you
project = MYPROJ AND type = Bug AND assignee = currentUser()

# High priority issues created in the last week
priority = High AND created >= -1w

# Issues in specific sprint
sprint = "Sprint 1"

# Unassigned open issues
assignee is EMPTY AND status != Done

# Issues with specific label
labels = "technical-debt"

# Recently updated issues
updated >= -1d ORDER BY updated DESC
```

## Troubleshooting

### Authentication Errors

**Error:** "401 Unauthorized"
- Check that your API token is correct
- Verify your email address matches your Jira account
- Ensure your Jira URL includes `https://` and ends with `.atlassian.net`

### Permission Errors

**Error:** "403 Forbidden"
- Your account may not have permission for the requested action
- Check project permissions in Jira settings
- Verify you have the "Browse Projects" permission

### Issue Not Found

**Error:** "404 Not Found"
- Verify the issue key is correct (e.g., "PROJ-123")
- Check that you have access to the project
- Ensure the issue hasn't been deleted

## Security Best Practices

- ✅ Never commit your API token to version control
- ✅ Use `.env` files for local development
- ✅ Store tokens in environment variables in production
- ✅ Rotate API tokens periodically
- ✅ Use read-only tokens when possible
- ✅ Revoke tokens immediately if compromised

## Development

### Running Tests

```bash
pytest tests/
```

### Running Locally

```bash
# Set environment variables
export JIRA_URL="https://your-company.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-token"

# Run the MCP server
python server.py
```

## Support

- **Issues:** [GitHub Issues](https://github.com/chaos-consultant/dev-orchestrator-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/chaos-consultant/dev-orchestrator-mcp/discussions)
- **Jira API Docs:** https://developer.atlassian.com/cloud/jira/platform/rest/v3/

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

Built with ❤️ by the Dev Orchestrator team
