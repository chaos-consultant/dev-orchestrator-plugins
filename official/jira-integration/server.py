"""
Jira Integration Plugin for Dev Orchestrator
Provides tools for creating, updating, and managing Jira issues.
"""
import os
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio

try:
    from jira import JIRA
    from jira.exceptions import JIRAError
except ImportError:
    raise ImportError("jira package is required. Install with: pip install jira>=3.5.0")

# Initialize MCP server
server = Server("jira-integration")

# Global Jira client
_jira_client: Optional[JIRA] = None


def get_jira_client() -> JIRA:
    """Get or create Jira client instance."""
    global _jira_client
    
    if _jira_client is None:
        jira_url = os.getenv("JIRA_URL")
        jira_email = os.getenv("JIRA_EMAIL")
        jira_token = os.getenv("JIRA_API_TOKEN")
        
        if not all([jira_url, jira_email, jira_token]):
            raise ValueError(
                "Missing Jira configuration. Required environment variables: "
                "JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN"
            )
        
        _jira_client = JIRA(
            server=jira_url,
            basic_auth=(jira_email, jira_token)
        )
    
    return _jira_client


@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available Jira tools."""
    return [
        Tool(
            name="jira_search_issues",
            description="Search Jira issues using JQL (Jira Query Language)",
            inputSchema={
                "type": "object",
                "properties": {
                    "jql": {
                        "type": "string",
                        "description": "JQL query string (e.g., 'project = MYPROJ AND status = Open')"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 50
                    },
                    "fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific fields to return (optional)"
                    }
                },
                "required": ["jql"]
            }
        ),
        Tool(
            name="jira_get_issue",
            description="Get detailed information about a specific Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "Issue key (e.g., 'PROJ-123')"
                    },
                    "expand": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Additional data to expand (e.g., ['changelog', 'comments'])"
                    }
                },
                "required": ["issue_key"]
            }
        ),
        Tool(
            name="jira_create_issue",
            description="Create a new Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project key (e.g., 'PROJ')"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Issue summary/title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Issue description"
                    },
                    "issue_type": {
                        "type": "string",
                        "description": "Issue type (e.g., 'Bug', 'Story', 'Task')",
                        "default": "Task"
                    },
                    "priority": {
                        "type": "string",
                        "description": "Priority (e.g., 'High', 'Medium', 'Low')"
                    },
                    "assignee": {
                        "type": "string",
                        "description": "Assignee username or email"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Issue labels"
                    }
                },
                "required": ["project", "summary", "issue_type"]
            }
        ),
        Tool(
            name="jira_update_issue",
            description="Update an existing Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "Issue key (e.g., 'PROJ-123')"
                    },
                    "summary": {
                        "type": "string",
                        "description": "New summary/title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    },
                    "priority": {
                        "type": "string",
                        "description": "New priority"
                    },
                    "assignee": {
                        "type": "string",
                        "description": "New assignee username or email"
                    },
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "New labels"
                    }
                },
                "required": ["issue_key"]
            }
        ),
        Tool(
            name="jira_add_comment",
            description="Add a comment to a Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "Issue key (e.g., 'PROJ-123')"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Comment text (supports Jira markdown)"
                    }
                },
                "required": ["issue_key", "comment"]
            }
        ),
        Tool(
            name="jira_transition_issue",
            description="Change the status of a Jira issue (e.g., move to In Progress, Done)",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "Issue key (e.g., 'PROJ-123')"
                    },
                    "transition": {
                        "type": "string",
                        "description": "Transition name or ID (e.g., 'In Progress', 'Done', '21')"
                    },
                    "comment": {
                        "type": "string",
                        "description": "Optional comment when transitioning"
                    }
                },
                "required": ["issue_key", "transition"]
            }
        ),
        Tool(
            name="jira_get_transitions",
            description="Get available transitions (status changes) for a Jira issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_key": {
                        "type": "string",
                        "description": "Issue key (e.g., 'PROJ-123')"
                    }
                },
                "required": ["issue_key"]
            }
        ),
        Tool(
            name="jira_list_projects",
            description="List all accessible Jira projects",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_archived": {
                        "type": "boolean",
                        "description": "Include archived projects",
                        "default": False
                    }
                }
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    try:
        jira = get_jira_client()
        
        if name == "jira_search_issues":
            jql = arguments["jql"]
            max_results = arguments.get("max_results", 50)
            fields = arguments.get("fields")
            
            issues = jira.search_issues(jql, maxResults=max_results, fields=fields)
            
            results = []
            for issue in issues:
                issue_data = {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "issue_type": issue.fields.issuetype.name,
                    "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                    "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
                    "priority": issue.fields.priority.name if issue.fields.priority else None,
                    "created": str(issue.fields.created),
                    "updated": str(issue.fields.updated),
                }
                results.append(issue_data)
            
            return [TextContent(
                type="text",
                text=f"Found {len(results)} issue(s):\n\n" + json.dumps(results, indent=2)
            )]
        
        elif name == "jira_get_issue":
            issue_key = arguments["issue_key"]
            expand = arguments.get("expand")
            
            issue = jira.issue(issue_key, expand=",".join(expand) if expand else None)
            
            issue_data = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": issue.fields.status.name,
                "issue_type": issue.fields.issuetype.name,
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "reporter": issue.fields.reporter.displayName if issue.fields.reporter else None,
                "priority": issue.fields.priority.name if issue.fields.priority else None,
                "labels": issue.fields.labels,
                "created": str(issue.fields.created),
                "updated": str(issue.fields.updated),
                "url": f"{jira.client_info()}/browse/{issue.key}"
            }
            
            # Add comments if expanded
            if expand and "comments" in expand:
                comments = jira.comments(issue)
                issue_data["comments"] = [
                    {
                        "author": c.author.displayName,
                        "body": c.body,
                        "created": str(c.created)
                    }
                    for c in comments
                ]
            
            return [TextContent(
                type="text",
                text=json.dumps(issue_data, indent=2)
            )]
        
        elif name == "jira_create_issue":
            project = arguments["project"]
            summary = arguments["summary"]
            description = arguments.get("description", "")
            issue_type = arguments.get("issue_type", "Task")
            priority = arguments.get("priority")
            assignee = arguments.get("assignee")
            labels = arguments.get("labels", [])
            
            issue_dict = {
                "project": {"key": project},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
            }
            
            if priority:
                issue_dict["priority"] = {"name": priority}
            
            if assignee:
                issue_dict["assignee"] = {"name": assignee}
            
            if labels:
                issue_dict["labels"] = labels
            
            new_issue = jira.create_issue(fields=issue_dict)
            
            return [TextContent(
                type="text",
                text=f"✅ Issue created successfully!\n\n"
                     f"Key: {new_issue.key}\n"
                     f"URL: {jira.client_info()}/browse/{new_issue.key}\n"
                     f"Summary: {summary}"
            )]
        
        elif name == "jira_update_issue":
            issue_key = arguments["issue_key"]
            
            issue = jira.issue(issue_key)
            update_fields = {}
            
            if "summary" in arguments:
                update_fields["summary"] = arguments["summary"]
            
            if "description" in arguments:
                update_fields["description"] = arguments["description"]
            
            if "priority" in arguments:
                update_fields["priority"] = {"name": arguments["priority"]}
            
            if "assignee" in arguments:
                update_fields["assignee"] = {"name": arguments["assignee"]}
            
            if "labels" in arguments:
                update_fields["labels"] = arguments["labels"]
            
            issue.update(fields=update_fields)
            
            return [TextContent(
                type="text",
                text=f"✅ Issue {issue_key} updated successfully!"
            )]
        
        elif name == "jira_add_comment":
            issue_key = arguments["issue_key"]
            comment = arguments["comment"]
            
            jira.add_comment(issue_key, comment)
            
            return [TextContent(
                type="text",
                text=f"✅ Comment added to {issue_key}"
            )]
        
        elif name == "jira_transition_issue":
            issue_key = arguments["issue_key"]
            transition = arguments["transition"]
            comment = arguments.get("comment")
            
            # Get available transitions
            transitions = jira.transitions(issue_key)
            
            # Find matching transition by name or ID
            transition_id = None
            for t in transitions:
                if t["name"].lower() == transition.lower() or t["id"] == transition:
                    transition_id = t["id"]
                    transition_name = t["name"]
                    break
            
            if not transition_id:
                available = ", ".join([t["name"] for t in transitions])
                return [TextContent(
                    type="text",
                    text=f"❌ Transition '{transition}' not found.\n\n"
                         f"Available transitions: {available}"
                )]
            
            # Perform transition
            jira.transition_issue(issue_key, transition_id, comment=comment)
            
            return [TextContent(
                type="text",
                text=f"✅ Issue {issue_key} transitioned to '{transition_name}'"
            )]
        
        elif name == "jira_get_transitions":
            issue_key = arguments["issue_key"]
            
            transitions = jira.transitions(issue_key)
            
            result = {
                "issue": issue_key,
                "available_transitions": [
                    {
                        "id": t["id"],
                        "name": t["name"],
                        "to_status": t["to"]["name"]
                    }
                    for t in transitions
                ]
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "jira_list_projects":
            include_archived = arguments.get("include_archived", False)
            
            projects = jira.projects()
            
            result = []
            for project in projects:
                # Filter archived projects if needed
                if not include_archived and hasattr(project, 'archived') and project.archived:
                    continue
                
                result.append({
                    "key": project.key,
                    "name": project.name,
                    "lead": project.lead.displayName if hasattr(project, 'lead') else None,
                    "url": f"{jira.client_info()}/browse/{project.key}"
                })
            
            return [TextContent(
                type="text",
                text=f"Found {len(result)} project(s):\n\n" + json.dumps(result, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]
    
    except JIRAError as e:
        return [TextContent(
            type="text",
            text=f"❌ Jira Error: {e.status_code} - {e.text}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]


if __name__ == "__main__":
    asyncio.run(server.run())
