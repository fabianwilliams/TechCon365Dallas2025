# TechCon365 Dallas 2025 - Conference Sessions MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with access to TechCon365 Dallas 2025 conference session data.

## Overview

This MCP server enables LLMs to query and explore conference sessions through 6 specialized tools:
- Search sessions by keyword with filters
- Get detailed session information
- List all tracks and speakers
- Filter by location or difficulty level

## How It Works: Understanding the Architecture

### What is an MCP Server?

An MCP server is like a **translator** between AI and your data. Think of it as a waiter in a restaurant:
- The AI (customer) asks questions in natural language
- The MCP server (waiter) translates those into database queries
- The data source (kitchen) provides the answer
- The server formats it nicely and returns it to the AI

### The Flow (Step by Step)

```
1. User asks: "Show me all Copilot sessions"
   ↓
2. Claude Desktop (MCP Client) receives the query
   ↓
3. Claude decides to use the conference_search_sessions tool
   ↓
4. server.py receives: { query: "Copilot", limit: 20 }
   ↓
5. server.py queries SQLite: SELECT * FROM sessions WHERE ...
   ↓
6. Database returns matching sessions
   ↓
7. server.py formats results as markdown
   ↓
8. Claude Desktop displays: "Found 8 sessions..."
```

### What's Inside server.py?

**FastMCP Framework**: A Python library that makes building MCP servers simple. Instead of handling low-level protocol details, you just write functions with the `@mcp.tool()` decorator.

**Tool Functions**: Each tool (like `conference_search_sessions`) is a Python function that:
1. Receives validated input parameters (thanks to Pydantic models)
2. Queries the SQLite database
3. Formats results (Markdown or JSON)
4. Returns to the AI

**Pydantic Models**: These are like forms with validation rules. They ensure the AI sends the right data types:
```
SearchSessionsInput:
  - query: string (2-200 characters)
  - track: optional string
  - level: must be "Intro/Overview", "Intermediate", or "Advanced"
  - limit: number between 1-100
```

If the AI sends invalid data (like `limit: 500`), Pydantic rejects it automatically.

### Configuration Files Explained

**sessions.db**: A SQLite database file containing all 182 conference sessions. Created by `database.py` and `parser.py` from the PDF schedule.

**requirements.txt**: Lists Python libraries needed:
- `fastmcp` - The MCP framework
- `pydantic` - Data validation
- (SQLite is built into Python)

**Claude Desktop Config**: Tells Claude Desktop where to find this server. Like adding a phone number to contacts - now Claude knows how to call this service.

```json
{
  "mcpServers": {
    "conference-sessions": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### Why This Architecture Matters

**Separation of Concerns**:
- AI handles natural language understanding
- MCP server handles data access logic
- Database handles storage and querying

**Security**: Your data never leaves your machine. The AI runs locally, queries stay local, only results are shown.

**Reusability**: The same MCP server works with Claude Desktop, LM Studio, or any MCP-compatible client.

**Simplicity**: No complex REST APIs, no authentication tokens, no server hosting. Just Python running on your machine.

## Features

- **Full-text search** across 182 conference sessions
- **Multiple filters**: track, level, location
- **Flexible output**: JSON or Markdown formats
- **Character limits**: Automatic truncation for large result sets
- **Comprehensive data**: Speakers, tracks, locations, times, descriptions

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Install dependencies:
```bash
cd /path/to/TechCon365Dallas2025/mcp-servers/conference-sessions
pip install -r requirements.txt
```

2. Verify the database exists:
```bash
ls -la sessions.db
```

If not, build it:
```bash
python database.py
```

3. Test the server syntax:
```bash
python -m py_compile server.py
```

### Configuration for Claude Desktop

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "conference-sessions": {
      "command": "python",
      "args": [
        "/path/to/TechCon365Dallas2025/mcp-servers/conference-sessions/server.py"
      ]
    }
  }
}
```

Then restart Claude Desktop.

### Test Queries

Once configured, try these queries in Claude Desktop:

1. **Search for AI sessions**:
   ```
   Show me all sessions about AI
   ```

2. **Find sessions in your room** (Room G7):
   ```
   What sessions are happening in Room G7?
   ```

3. **List all tracks**:
   ```
   What are all the conference tracks?
   ```

4. **Find beginner sessions**:
   ```
   Show me all Intro/Overview level sessions
   ```

5. **Search by speaker**:
   ```
   What sessions is Fabian Williams speaking at?
   ```

## Available Tools

### 1. conference_search_sessions
Full-text search across sessions with optional filters.

**Parameters**:
- `query` (required): Search string
- `track` (optional): Filter by track
- `level` (optional): Filter by level (Intro/Overview, Intermediate, Advanced, All)
- `location` (optional): Filter by room/location
- `limit` (optional): Max results (1-100, default 20)
- `response_format` (optional): "markdown" or "json"

### 2. conference_get_session
Get detailed information about a specific session by ID.

**Parameters**:
- `session_id` (required): Numeric session ID
- `response_format` (optional): "markdown" or "json"

### 3. conference_list_tracks
List all available conference tracks with session counts.

**Parameters**:
- `response_format` (optional): "markdown" or "json"

### 4. conference_list_speakers
List all speakers with their session counts.

**Parameters**:
- `response_format` (optional): "markdown" or "json"

### 5. conference_get_sessions_by_location
Get all sessions in a specific room/location.

**Parameters**:
- `location` (required): Room name (e.g., "Room G7", "G1")
- `limit` (optional): Max results (1-100, default 20)
- `response_format` (optional): "markdown" or "json"

### 6. conference_get_sessions_by_level
Get all sessions at a specific difficulty level.

**Parameters**:
- `level` (required): "Intro/Overview", "Intermediate", "Advanced", or "All"
- `limit` (optional): Max results (1-100, default 20)
- `response_format` (optional): "markdown" or "json"

## Database Schema

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    speakers TEXT,
    track TEXT,
    level TEXT,
    location TEXT,
    time_slot TEXT,
    day TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Statistics

- **Total sessions**: 182
- **Days**: 5 (Nov 3-7, 2025)
- **Levels**: Intro/Overview (49), Intermediate (88), Advanced (11), All (26)
- **Tracks**: 70+ unique track combinations
- **Locations**: Rooms G1-G7, Expo Hall, Level 4

## Architecture

```
User Query → Claude Desktop → MCP Client → conference_sessions_mcp
                                              ↓
                                         6 Tools → SQLite Database (sessions.db)
                                              ↓
                                         Formatted Results
```

## Development

### Project Structure
```
conference-sessions/
├── server.py        # MCP server with 6 tools
├── database.py      # SQLite database management
├── parser.py        # PDF-to-data parser
├── sessions.db      # SQLite database (401KB)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

### Testing

To test the server manually:

```bash
# Run in background (it will wait for stdin)
python server.py &

# Or test with timeout
timeout 5s python server.py
```

Note: MCP servers are long-running processes that communicate via stdio. They won't output anything when run directly - they wait for MCP protocol messages.

## Troubleshooting

### Server not appearing in Claude Desktop
1. Check config file syntax (valid JSON)
2. Verify the full path to server.py is correct
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

### Database not found
Run the database builder:
```bash
python database.py
```

### Import errors
Install dependencies:
```bash
pip install -r requirements.txt
```

## License

Built for TechCon365 Dallas 2025 presentation on MCP.

## Demo Queries for Presentation

Perfect queries to showcase during the live demo:

1. "Show me all sessions about Copilot"
2. "Who is speaking in Room G7?" *(That's YOUR room!)*
3. "Find all beginner-friendly sessions"
4. "What sessions mention AI or Copilot in the description?"
5. "List all the conference tracks"

These demonstrate:
- Full-text search
- Location filtering
- Level filtering
- Track discovery
- Real conference data
