# Building an MCP Demo with AI Assistance - The Journey

**Session**: Getting started with Model Context Protocol (MCP) and Why Should You Care
**Speaker**: Fabian Williams
**Conference**: TechCon365 Dallas 2025
**Date Started**: October 31, 2025

## Project Goals
- Build an MCP demo that showcases conference session data queries
- Integrate Microsoft Graph API to demonstrate enterprise integration
- Create a PowerPoint presentation deck
- Compare MCP with A2A, ACP, and Anthropic Skills
- Keep it simple and educational (Level 100/200)
- Document this AI-assisted development journey

## Development Environment
- MacBook Pro M3 Max, 128GB RAM, 40 Core GPU
- Ollama + LM Studio (local models)
- OpenAI subscription
- VS Code IDE
- .NET and Python (prefer venvs)
- SQLite
- Docker
- Claude Code with Skills enabled

---

## Session Log

### Session 1: Initial Planning (Oct 31, 2025)

**Context**: Starting the project. Fabian wants to create both a demo and presentation, documenting the AI collaboration process.

**Key Decisions**:
1. Build TWO MCP demos:
   - Conference session data MCP server (query sessions from PDF)
   - Microsoft Graph integration (calendar/email) - leverage existing repos
2. Use whatever language is easier to understand (Python likely for clarity)
3. Compare MCP vs A2A vs ACP + Anthropic Skills evolution
4. Real-time journey documentation to manage context windows
5. Explore using Claude Skills to build components

**Actions Taken**:
- Created todo list for project phases
- Created this JOURNEY.md file
- Discovered available Claude Skills:
  - `mcp-builder`: Guide for creating MCP servers (Python/TypeScript)
  - `pptx`: PowerPoint creation using html2pptx workflow
  - `skill-creator`: For creating custom skills if needed

**Skills Available**:
- mcp-builder will guide us through creating quality MCP servers
- pptx will help generate the PowerPoint presentation programmatically

**Current Status**: Architecture designed! Ready to build.

**Architecture Decisions Made**:
1. **Language**: Python (clearer for Level 100/200 audience)
2. **Conference MCP**: SQLite-backed server with 6 tools for querying session data
3. **Graph MCP**: OAuth-based server with 5 tools for email/calendar
4. **Presentation**: 15-20 slides using html2pptx workflow
5. **Comparisons**: Clear explanations of MCP vs A2A vs ACP vs Skills

**Key Insight**: MCP is about AI accessing YOUR data. A2A/ACP are about AIs talking to EACH OTHER. Skills are packaged capabilities that often use MCP.

See ARCHITECTURE.md for full details!

**Demo Flow Refinement**:
- **Simple first**: Conference Sessions (quick, relatable, hook audience)
- **Detailed second**: Microsoft Graph (enterprise, OAuth, audience participation!)
- **Audience participation**: Ask attendees to email your-email@your-domain.com during session
- **Show THEIR emails** in the live demo - makes it memorable and tangible
- **Tone**: Technical and accessible (not too business-y, not too deep)

---

---

### Session 2: Building the Conference Sessions Database (Oct 31, 2025)

**Context**: Starting to build the first demo - Conference Sessions MCP.

**Actions Taken**:
- Created project structure (mcp-servers/conference-sessions/)
- Built `parser.py` to extract sessions from PDF markdown
- Built `database.py` to create SQLite database with full-text search
- Successfully parsed 182 sessions
- Created database with indexes and FTS for fast queries

**Stats**:
- 182 total sessions across 5 days (Nov 3-7, 2025)
- 4 levels: Intro/Overview (49), Intermediate (88), Advanced (11), All (26)
- Multiple tracks: Copilot/AI, Power Platform, SharePoint, etc.
- Locations: Rooms G1-G7, Expo Hall, etc.

**Challenges & Solutions**:
- **Challenge**: PDF extraction had UI noise (e.g., "Search sessions...All DaysAll TracksTrack:")
- **Solution**: Used regex to extract Track from embedded text
- **Challenge**: Parser wasn't finding Location field
- **Solution**: Rewrote metadata parsing to handle fields in any order

**Current Status**: Database ready! Moving to MCP server implementation.

---

### Session 3: Building the Conference Sessions MCP Server (Oct 31, 2025)

**Context**: Using the mcp-builder skill to create a high-quality MCP server.

**Actions Taken**:
- Invoked mcp-builder skill and read Python implementation guide
- Read MCP best practices documentation
- Created `server.py` with FastMCP following all best practices:
  - 6 tools for querying conference data
  - Pydantic models for input validation
  - Support for both JSON and Markdown output formats
  - Character limits and truncation handling
  - Comprehensive docstrings
  - Proper tool annotations (readOnlyHint, etc.)

**Tools Implemented**:
1. `conference_search_sessions` - Full-text search with filters (track, level, location)
2. `conference_get_session` - Get detailed session info by ID
3. `conference_list_tracks` - List all conference tracks
4. `conference_list_speakers` - List all speakers
5. `conference_get_sessions_by_location` - Filter by room
6. `conference_get_sessions_by_level` - Filter by difficulty level

**Quality Checks**:
- ✅ Server name follows Python convention: `conference_sessions_mcp`
- ✅ Tool names use snake_case with service prefix
- ✅ All tools have comprehensive docstrings
- ✅ Pydantic models with Field descriptions and constraints
- ✅ Async/await patterns for I/O
- ✅ Error handling with clear messages
- ✅ CHARACTER_LIMIT with truncation support
- ✅ Python syntax validated successfully

**Current Status**: Conference Sessions MCP server complete and ready for testing!

---

### Session 4: Testing Setup (Oct 31, 2025)

**Context**: Preparing to test the Conference Sessions MCP server in Claude Desktop.

**Actions Taken**:
- Created comprehensive README.md with setup instructions and demo queries
- Added server to Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json`
- Installed MCP dependencies (mcp, pydantic)
- Created TESTING.md template to document test results
- Verified all prerequisites:
  - ✅ Python syntax valid
  - ✅ Database exists (182 sessions, 401KB)
  - ✅ Dependencies installed
  - ✅ Config file updated

**Test Queries Prepared**:
1. "Show me all sessions about Copilot"
2. "What sessions are happening in Room G7?" (Your room!)
3. "What are all the conference tracks?"
4. "Show me all beginner-friendly sessions"
5. "What sessions is Fabian Williams speaking at?"

**Next Step**: Restart Claude Desktop and test the MCP server!

**Current Status**: Ready for live testing! All setup complete.

---

### Session 5: Building Microsoft Graph MCP Server (Oct 31, 2025)

**Context**: Working autonomously while Fabian stepped away. Building the Graph MCP to demonstrate MCP composition.

**Actions Taken**:
- Updated ARCHITECTURE.md with simplified scope (4 tools, single-tenant)
- Created `graph_auth.py` - Simplified OAuth manager using MSAL
- Created `server.py` - 4 tools for email and calendar operations
- Created `requirements.txt` with dependencies
- Created comprehensive README.md
- Validated Python syntax successfully

**Microsoft Graph MCP Tools** (4 tools):
1. `graph_read_emails` - Read recent emails from inbox
2. `graph_search_emails` - Search by sender/keyword
3. `graph_create_calendar_event` - **Create calendar events (write operation!)**
4. `graph_get_calendar_events` - View calendar for date range

**Key Features**:
- Single-tenant OAuth (your-domain.com domain only)
- Uses existing credentials from Fabs-Graph-Search config
- Token caching and automatic refresh
- Both JSON and Markdown output formats
- Comprehensive error handling with clear messages
- Ready for MCP composition demo!

**Demo Workflow Designed**:
1. Search sessions → Conference MCP
2. Read audience emails → Graph MCP
3. **Add session to calendar → MCP Composition!**
4. Verify event created → Graph MCP

**Quality Checks**:
- ✅ Server name: `msgraph_mcp`
- ✅ Tool names with `graph_` prefix
- ✅ Pydantic models with validation
- ✅ Async/await patterns
- ✅ OAuth with MSAL
- ✅ Error handling
- ✅ Python syntax validated

  **Current Status**: Graph MCP server complete! Ready to configure and test.
  
  ---
  
  ### Session 6: Testing & Troubleshooting (Oct 31, 2025)
  
  **Context**: Fabian returned from break and tested both MCP servers in Claude Desktop.
  
  **Test Results**:
  - ✅ Conference Sessions MCP: **Working perfectly!** Successfully found sessions, including Session 127 (Fabian's MCP presentation)
  - ❌ Graph MCP: **Revealed MCP server conflict issue**
  
  **Issue Discovered**: 
  When asking "show me recent emails," Claude Desktop used the existing `Fabs-Graph-Search` server (database-based, old emails) instead of the new `msgraph` server (live Graph API, current emails).
  
  **Root Cause**:
  - User has 3 email-related MCP servers in config
  - Claude Desktop chose `Fabs-Graph-Search` over `msgraph`
  - Competing servers with similar capabilities
  - Tool names weren't distinct enough
  
  **Solutions Identified**:
  1. Use explicit tool names: "Use graph_read_emails to..." (immediate fix)
  2. Temporarily disable `Fabs-Graph-Search` during demo (clean fix)
  3. Rename MCP server to be more distinct (optional)
  
  **Actions Taken**:
  - Created `GRAPH-MCP-TROUBLESHOOTING.md` with detailed analysis
  - Documented all 3 solution options
  - Created testing checklist
  - Updated demo flow with explicit tool names
  - Verified auth manager works correctly
  - Confirmed server imports successfully
  
  **Key Learnings**:
  - MCP servers can conflict when tools overlap
  - Explicit tool naming gives control
  - Testing reveals real-world integration issues
  - Having multiple MCP servers requires careful management
  
  **Next Steps**:
  - Decide: Disable competing server or use explicit names
  - Test Graph MCP with explicit tool calls
  - Verify MCP composition works
  - Build PowerPoint presentation
  
  **Current Status**: Issue diagnosed and solutions ready. Graph MCP is functional, just needs proper invocation.
  
  ---
  
  ### Session 7: MCP Composition Success! (Oct 31, 2025)
  
  **Context**: Testing both MCPs working together in LM Studio to demonstrate true MCP composition.
  
  **The Big Achievement**: 🎉 **MCP COMPOSITION WORKING!**
  
  **What Happened**:
  - Used LM Studio with both MCPs configured
  - Prompt: "Show me all sessions about Model Context Protocol"
  - Conference Sessions MCP found 4 MCP-related sessions
  - Follow-up: "add the 1st result from Prashant to my calendar please"
  - **Graph MCP successfully created calendar event!**
  - Event appeared in Outlook calendar immediately
  
  **Sessions Found by Conference MCP**:
  1. Hands-On: Azure, ChatGPT, DeepSeek, Azure OpenAI - Prashant G Bhoyar (Room C, Monday Nov 3)
  2. Building Smart Agents with Copilot Studio - Luc Labelle (Room A, Thursday Nov 6)
  3. **Getting Started with MCP (Fabian's session!)** - Room G7, Thursday Nov 6, 2:20-3:30 PM
  4. Integrating AI Applications with Copilot Studio Using MCP - Prashant G Bhoyar (Room B, Thursday Nov 6)
  
  **Calendar Event Created**:
  - ✅ Subject: "Hands-On: Azure, ChatGPT, DeepSeek, Azure OpenAI For Power Platform Developers Masterclass"
  - ✅ Speaker: Prashant G Bhoyar
  - ✅ Date & Time: November 3, 2025 - 09:00 AM to 05:00 PM
  - ✅ Location: Room C
  - ✅ Verified in Outlook calendar!
  
  **Technical Flow**:
  1. User query → LM Studio → Conference Sessions MCP
  2. Conference MCP searches SQLite database with FTS5
  3. Returns 4 matching sessions with full details
  4. User requests calendar addition → LM Studio → Graph MCP
  5. Graph MCP uses cached OAuth token
  6. Creates event via Microsoft Graph API
  7. Event syncs to Outlook calendar
  8. **TWO MCP SERVERS COORDINATING PERFECTLY!**
  
  **Key Learnings**:
  - MCP composition works seamlessly - AI orchestrates multiple servers
  - Data flows between MCPs through natural language
  - Read operation (Conference search) + Write operation (Calendar create)
  - LM Studio handles MCP protocol perfectly
  - Token caching makes Graph API smooth (no re-auth needed)
  
  **Files Referenced**:
  - LM Studio conversation: `~/local-lm-studio-logs/conversation.json`
  - Token cache: `~/.msgraph-mcp/token_cache.json`
  - Session database: `mcp-servers/conference-sessions/sessions.db`
  
  **Demo Significance**:
  This is the **EXACT demo flow** for TechCon365:
  - Shows simple MCP (local data, read-only)
  - Shows complex MCP (enterprise API, OAuth, write operations)
  - Shows MCP composition (two servers working together)
  - Shows real business value (search → action)
  
  **Current Status**: 🚀 **DEMO-READY! Both MCPs working, composition verified, calendar event created!**
  
  ---
  
## Notes & Learnings### What Worked Well
- Python's `markitdown[pdf]` handled PDF extraction well
- SQLite FTS5 provides excellent full-text search out of the box
- Dataclass pattern for Session model keeps code clean
- State machine approach for parsing unstructured text worked well

### Challenges & Solutions
- PDF extraction quality varies - needed flexible parser
- Regex patterns needed for embedded metadata extraction

### Key Insights
- (To be filled as we progress)

---

*This document is updated in real-time as we build the demo together*
