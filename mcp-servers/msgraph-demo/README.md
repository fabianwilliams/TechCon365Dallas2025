# Microsoft Graph MCP Server

A Model Context Protocol (MCP) server that connects AI assistants to Microsoft 365 via Graph API for email and calendar operations.

## Overview

This MCP server enables LLMs to interact with Microsoft 365 through 4 specialized tools:
- Read and search emails
- Get calendar events
- Create calendar events (write operations)

**Key Feature**: Demonstrates MCP composition by working alongside the Conference Sessions MCP to add conference sessions directly to your calendar!

## Features

- **Email Access**: Read recent emails, search by sender/keyword
- **Calendar Management**: View and create calendar events
- **OAuth Security**: Secure authentication with Microsoft identity platform
- **Flexible Output**: JSON or Markdown formats
- **Single-Tenant**: Configured for your-domain.com domain

## Quick Start

### Prerequisites

- Python 3.10+
- Microsoft Azure app registration (single-tenant)
- Required Graph API permissions:
  - Mail.Read
  - Calendars.ReadWrite
  - User.Read

### Installation

1. Install dependencies:
```bash
cd /path/to/TechCon365Dallas2025/mcp-servers/msgraph-demo
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export TENANT_ID="your-tenant-id"
export CLIENT_ID="your-client-id"
# export CLIENT_SECRET="not-needed-for-device-flow"  # Only needed for client credentials flow  # Optional for delegated auth
```

Or use the existing credentials from `Fabs-Graph-Search` config.

3. Test syntax:
```bash
python -m py_compile server.py
```

### Configuration for Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "msgraph": {
      "command": "/path/to/your/python3",
      "args": [
        "/path/to/TechCon365Dallas2025/mcp-servers/msgraph-demo/server.py"
      ],
      "env": {
        "TENANT_ID": "485a3633-bdd7-4b94-a9d4-1e7e2f9de3e2",
        "CLIENT_ID": "a17fca6a-4062-45ca-9115-7214b2b68de2",
        "CLIENT_ID": "14d82eec-204b-4c2f-b7e8-296a70dab67e" // Note: CLIENT_SECRET not needed for device code flow
      }
    }
  }
}
```

Then restart Claude Desktop.

## Demo Workflow

### The Perfect Demo Flow (MCP Composition!)

**Step 1**: Search sessions (Conference MCP)
```
"Show me all Copilot Studio sessions at TechCon"
```

**Step 2**: Check emails from audience (Graph MCP)
```
"Show me emails from the last hour"
```

**Step 3**: Create calendar event (Graph MCP + Composition!)
```
"Add Session 87 (Building Smart Agents with Copilot Studio) to my calendar for Thursday, November 6 at 9am in Room A"
```

**Step 4**: Verify it worked (Graph MCP)
```
"Show my calendar for November 6"
```

**This demonstrates**:
- Two MCP servers working together
- Read operations (search, list)
- Write operations (calendar create)
- Real enterprise integration
- Practical, immediately useful workflow

## Available Tools

### 1. graph_read_emails
Read recent emails from mailbox.

**Parameters**:
- `limit` (optional): Number of emails (1-50, default 10)
- `folder` (optional): Folder name (default "inbox")
- `response_format` (optional): "markdown" or "json"

**Example queries**:
- "Show me my recent emails"
- "Get the last 20 emails"

### 2. graph_search_emails
Search emails by keyword, sender, or subject.

**Parameters**:
- `query` (required): Search string
- `limit` (optional): Max results (1-50, default 10)
- `response_format` (optional): "markdown" or "json"

**Example queries**:
- "Search emails for 'TechCon'"
- "Find emails from john@example.com"

### 3. graph_create_calendar_event
Create a new calendar event.

**Parameters**:
- `subject` (required): Event title
- `start_datetime` (required): Start time (ISO format or natural)
- `end_datetime` (optional): End time (defaults to +1 hour)
- `location` (optional): Location/room
- `body` (optional): Event description
- `response_format` (optional): "markdown" or "json"

**Example queries**:
- "Add Session 87 to my calendar for Thursday at 9am"
- "Create a meeting tomorrow at 2pm in Room G7"

### 4. graph_get_calendar_events
Get calendar events for a date range.

**Parameters**:
- `start_date` (optional): Start date (defaults to today)
- `end_date` (optional): End date (defaults to +7 days)
- `limit` (optional): Max events (1-100, default 20)
- `response_format` (optional): "markdown" or "json"

**Example queries**:
- "Show my calendar for today"
- "What meetings do I have on November 6?"

## Authentication

### For Demo (Single-Tenant)
Uses existing credentials from Fabs-Graph-Search configuration.

**Account**: your-email@your-domain.com (your tenant)

### Token Storage
Tokens are cached in `~/.msgraph-mcp/token_cache.json` and automatically refreshed.

### First-Time Setup
If authentication is required:
1. Run the server
2. Follow the device code flow instructions
3. Complete authentication in browser
4. Tokens are cached for future use

## Troubleshooting

### Authentication errors
- Verify TENANT_ID, CLIENT_ID, CLIENT_SECRET are set
- Check that app registration has required permissions
- Ensure permissions are admin-consented
- Try deleting token cache: `rm ~/.msgraph-mcp/token_cache.json`

### Permission errors (403)
- Verify Graph API permissions in Azure portal
- Ensure admin consent has been granted
- Check that user has access to mailbox/calendar

### Server not appearing
- Check Claude Desktop config syntax
- Verify environment variables are set in config
- Restart Claude Desktop completely

## Architecture

```
User Query → Claude Desktop → MCP Client → msgraph_mcp
                                              ↓
                                         4 Tools → Graph API
                                         (OAuth)      ↓
                                                Microsoft 365
                                              (Mail + Calendar)
```

## Demo Talking Points

**"See how MCP servers compose?"**
- Conference MCP provides session data (local SQLite)
- Graph MCP creates calendar events (enterprise API)
- AI understands both and connects them naturally
- Same pattern works for ANY API: Salesforce, Jira, ServiceNow

**"This is the art of the possible"**
- Not about implementation details
- About connecting AI to YOUR business data
- Standard protocol, infinite possibilities
- Security through OAuth, simplicity through MCP

## Development

### Project Structure
```
msgraph-demo/
├── server.py        # MCP server with 4 tools
├── graph_auth.py    # OAuth authentication manager
├── requirements.txt # Python dependencies
└── README.md        # This file
```

### Security Notes
- Single-tenant app (your-domain.com only)
- OAuth 2.0 with secure token storage
- No credentials stored in code
- Environment variables for configuration

## License

Built for TechCon365 Dallas 2025 presentation on MCP.
