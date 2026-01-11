# Dev Orchestrator Plugins

Official and community plugins for [Dev Orchestrator MCP](https://github.com/chaos-consultant/dev-orchestrator-mcp).

## Overview

This repository contains MCP (Model Context Protocol) server plugins that extend Dev Orchestrator's capabilities. Plugins add new tools and integrations that Claude Code can use to interact with external services and systems.

## Available Plugins

### Official Plugins

#### Jira Integration
**Status:** 🚧 Coming Soon
**Description:** Create and manage Jira issues, search projects, update tickets, and integrate with Atlassian Jira.

**Tools:**
- `jira_create_issue` - Create new issues
- `jira_update_issue` - Update existing issues
- `jira_search_issues` - Search with JQL
- `jira_add_comment` - Add comments to issues
- `jira_get_issue` - Get issue details
- `jira_list_projects` - List accessible projects
- `jira_assign_issue` - Assign issues to users
- `jira_transition_issue` - Change issue status

**Requirements:**
- Jira URL
- Jira Email
- Jira API Token

---

#### Docker Manager
**Status:** 🚧 Coming Soon
**Description:** Manage Docker containers, images, networks, and volumes. Start/stop services, view logs, and monitor containers.

**Tools:**
- `docker_list_containers` - List all containers
- `docker_start_container` - Start a container
- `docker_stop_container` - Stop a container
- `docker_restart_container` - Restart a container
- `docker_logs` - View container logs
- `docker_inspect_container` - Get container details
- `docker_list_images` - List Docker images
- `docker_pull_image` - Pull image from registry
- `docker_exec_command` - Execute command in container

**Requirements:**
- Docker daemon access

---

#### Database Query Runner
**Status:** 🚧 Coming Soon
**Description:** Execute SQL queries safely across MySQL, PostgreSQL, SQLite with query validation, explain plans, and result formatting.

**Tools:**
- `db_query` - Execute SELECT queries
- `db_list_tables` - List database tables
- `db_describe_table` - Get table schema
- `db_explain_query` - Show query execution plan
- `db_list_databases` - List available databases
- `db_table_row_count` - Count rows in table

**Requirements:**
- Database connection string

**Supported Databases:**
- PostgreSQL
- MySQL/MariaDB
- SQLite

---

## Installation

### Via Dev Orchestrator Dashboard

1. Open the Dev Orchestrator dashboard at http://localhost:3333
2. Navigate to **Plugins** in the sidebar
3. Click **Install Plugin**
4. Enter the Git URL for the plugin:
   ```
   https://github.com/chaos-consultant/dev-orchestrator-plugins.git#<plugin-name>
   ```
5. Follow the configuration prompts

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/chaos-consultant/dev-orchestrator-plugins.git
cd dev-orchestrator-plugins

# Navigate to the plugin directory
cd official/<plugin-name>

# Install dependencies
pip install -r requirements.txt  # For Python plugins
# or
npm install  # For Node.js plugins

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Test the plugin
python server.py  # For Python plugins
# or
npm start  # For Node.js plugins
```

## Creating Your Own Plugin

Dev Orchestrator provides an interactive plugin creator:

```bash
# Use the MCP tool via Claude Code
create_plugin(
    name="my-custom-plugin",
    description="My awesome plugin",
    author="Your Name",
    template_type="basic",  # or "advanced"
    runtime="python"  # or "node"
)
```

Or use the dashboard:
1. Navigate to **Plugins** → **Create Plugin**
2. Follow the interactive wizard
3. Choose template type (basic or advanced)
4. Define your tools
5. Implement the handlers

### Plugin Structure

```
my-plugin/
├── mcp_server.json          # Plugin manifest
├── server.py                # MCP server implementation (Python)
│   or server.js             # MCP server implementation (Node.js)
├── requirements.txt         # Python dependencies
│   or package.json          # Node.js dependencies
├── README.md                # Plugin documentation
└── .env.example             # Environment variables template
```

### Plugin Manifest Example

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "author": "Your Name",
  "tools": [
    {
      "name": "my_tool",
      "description": "Does something useful"
    }
  ],
  "env": [
    "API_KEY",
    "API_URL"
  ]
}
```

## Development Guidelines

See [PLUGIN_CONTRIBUTING.md](https://github.com/chaos-consultant/dev-orchestrator-mcp/blob/main/docs/PLUGIN_CONTRIBUTING.md) for detailed contribution guidelines.

### Key Principles

- **Security First:** Never expose credentials or sensitive data
- **Error Handling:** Provide clear error messages
- **Documentation:** Include examples and usage instructions
- **Testing:** Write tests for your tools
- **Type Safety:** Use type hints (Python) or TypeScript (Node.js)

## Contributing

We welcome contributions! Here's how to submit a plugin:

1. **Fork this repository**
2. **Create a new branch:** `git checkout -b feature/my-plugin`
3. **Add your plugin** in the `community/` directory
4. **Test thoroughly**
5. **Submit a pull request**

### Submission Checklist

- [ ] Plugin follows the standard structure
- [ ] README.md included with usage examples
- [ ] All dependencies listed in requirements.txt or package.json
- [ ] .env.example provided for configuration
- [ ] Security review completed
- [ ] No hardcoded credentials
- [ ] Error handling implemented
- [ ] Tools documented with clear descriptions

## Security

See [PLUGIN_SECURITY.md](https://github.com/chaos-consultant/dev-orchestrator-mcp/blob/main/docs/PLUGIN_SECURITY.md) for security guidelines.

**Important:**
- Never commit API keys, tokens, or passwords
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize data before executing commands
- Follow principle of least privilege

## Plugin Verification Levels

- **🟣 Anthropic Official** - Maintained by Anthropic (highest trust)
- **🔵 Dev Orchestrator Official** - Built by Dev Orchestrator team (high trust)
- **🟢 Verified Community** - Security reviewed (medium trust)
- **⚪ Community** - Not verified - review code before installing (low trust)

## Support

- **Issues:** [GitHub Issues](https://github.com/chaos-consultant/dev-orchestrator-plugins/issues)
- **Discussions:** [GitHub Discussions](https://github.com/chaos-consultant/dev-orchestrator-mcp/discussions)
- **Documentation:** [Dev Orchestrator Docs](https://github.com/chaos-consultant/dev-orchestrator-mcp#readme)

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ for the Dev Orchestrator community
