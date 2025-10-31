# TechCon365 Dallas 2025 - MCP Demo Architecture

## Project Overview
Building two MCP servers to demonstrate the power and versatility of Model Context Protocol at TechCon365 Dallas 2025.

**Key Innovation**: Local AI models (via LM Studio) accessing enterprise APIs through MCP - combining privacy of local processing with power of cloud services. Your prompts never leave your machine, but your AI can still access Microsoft 365, databases, and any other API.

## Demo 1: Conference Sessions MCP Server

### Purpose
Allow AI assistants to query TechCon365 Dallas conference session data through MCP tools.

### Data Source
PDF document with ~9000 lines of conference session data including:
- Session titles and descriptions
- Speakers
- Tracks (Copilot/AI, Business Value, SharePoint, etc.)
- Levels (Intro/Overview, Intermediate, Advanced)
- Time slots and locations
- Detailed descriptions

### Implementation Approach
**Technology**: Python with MCP Python SDK

**Data Storage**: SQLite database
- Parse extracted markdown sessions data
- Store in normalized SQLite tables
- Enable fast querying and filtering

**MCP Tools to Provide**:
1. `search_sessions` - Search by keyword, speaker, track, or level
2. `get_session_by_id` - Get detailed info about a specific session
3. `list_tracks` - List all available tracks
4. `list_speakers` - List all speakers
5. `get_sessions_by_time` - Find sessions in a specific time slot
6. `get_sessions_by_location` - Find sessions in a specific room

**Why This Demo Works**:
- Real, relevant data from the actual conference
- Demonstrates practical business value
- Shows how MCP makes AI contextually aware of domain-specific data
- Audience can relate to it immediately
- **Local AI processing** - conference data never sent to cloud providers

---

## Demo 2: Microsoft Graph MCP Server

### Purpose
Demonstrate enterprise integration AND MCP composition by connecting AI to Microsoft 365 services (Calendar, Email).

### Data Source
Microsoft Graph API with OAuth2 authentication (single-tenant: your-domain.com)

### Implementation Approach
**Technology**: Python with MCP Python SDK

**Authentication**: OAuth2 Client Credentials Flow
- Single-tenant only (your domain)
- Pre-authenticated before demo (no live OAuth flow on stage)
- Reuse patterns from existing Graph integrations
- Secure token storage and refresh

**MCP Tools to Provide** (4 tools - simplified for demo):
1. `graph_read_emails` - Get recent emails from inbox (show audience emails)
2. `graph_search_emails` - Search emails by sender/keyword (find suggestions)
3. `graph_create_calendar_event` - Create calendar event (add suggested session)
4. `graph_get_calendar_events` - Get calendar events for date range (verify it worked)

**Why This Demo Works**:
- Shows real enterprise integration
- **Demonstrates MCP composition** (Conference MCP → Graph MCP)
- Both read and write operations
- OAuth security without complexity
- Practical, immediately useful workflow
- Directly relevant to Microsoft conference audience
- **Privacy-first**: Local AI model orchestrates, only API data travels (OAuth-protected)
- **Compliance-friendly**: Your prompts stay on your machine, auditable API access

---

## Presentation Architecture

### PowerPoint Structure
Using Claude's PPTX skill with html2pptx workflow

**Slide Outline** (15-20 slides):

1. **Title Slide**: Getting Started with MCP and Why Should You Care
2. **Who Am I**: Quick intro
3. **The Problem**: AI assistants without real data are limited
4. **The Privacy Problem**: Sending enterprise data to cloud AI providers
5. **What is MCP?**: Simple explanation with diagram
6. **MCP Architecture**: How it works (Local AI ↔ MCP Server ↔ Data Source)
7. **The Local AI Advantage**: Your model, your data, your control
8. **Live Demo #1 - Simple**: Conference Sessions MCP
   - Show querying conference data
   - Demonstrate contextual awareness
   - Emphasize: "This prompt never left my laptop"
   - Quick win to hook the audience
9. **MCP vs A2A (Agent-to-Agent)**: Comparison table
10. **MCP vs ACP (Agent Communication Protocol)**: Key differences
11. **Anthropic Skills**: The evolution of MCP
   - How Skills build on MCP
   - Skills as packaged MCP capabilities
12. **Why Local Models + MCP Matter**:
    - Privacy: Prompts stay local
    - Security: Only API calls travel (OAuth-protected)
    - Cost: Pay once for hardware, not per-token
    - Compliance: Data residency requirements met
13. **Audience Participation**: "Send an email to your-email@your-domain.com"
    - Large text with email address
    - Subject: "Hello from TechCon365"
    - 30 second pause for participation
14. **Live Demo #2 - Detailed**: Microsoft Graph Integration
    - Show calendar events
    - Show emails FROM THE AUDIENCE
    - Create calendar event
    - Emphasize: "Local AI reads emails, creates events - no cloud AI sees this"
    - Demonstrate enterprise capabilities
15. **Real-World Use Cases**:
    - Customer support with CRM data (privacy-compliant)
    - DevOps with deployment systems (air-gapped possible)
    - Business analytics with data warehouses (local processing)
16. **Why MCP Matters for M365/Graph**: Security, standardization, simplicity, **privacy**
17. **Getting Started**: Resources and next steps
18. **Key Takeaways**: 3-5 bullet points (include privacy/local advantage)
19. **Q&A**: Contact info and resources

**Design Approach**:
- Clean, modern, professional
- Microsoft-inspired color palette (blues, teals, white)
- Minimal text, maximum impact
- Code examples where relevant (but keep simple)
- Diagrams to explain concepts visually

---

## Technical Stack

### Development Environment
- **Language**: Python 3.12
- **Virtual Environment**: venv (isolated dependencies)
- **IDE**: VS Code
- **Database**: SQLite
- **MCP SDK**: Python MCP SDK / FastMCP
- **OAuth**: MSAL (Microsoft) + Google Auth libraries
- **Presentation**: html2pptx via Claude PPTX skill

### Dependencies
```
# MCP Server
mcp
pydantic
sqlite3 (built-in)

# Microsoft Graph
msal
requests

# Data Processing
markitdown[pdf]

# Presentation
(Node.js packages via pptx skill)
```

### Project Structure
```
TechCon365Dallas2025/
├── JOURNEY.md                    # Development journey log
├── ARCHITECTURE.md              # This file
├── README.md                    # Project overview
├── Sessions-TechCon365Dallas2025.pdf
├── sessions-extracted.md        # Extracted session data
├── presentation/
│   ├── slides/                  # HTML slides
│   ├── scripts/                 # Presentation generation
│   └── output/                  # Generated .pptx
└── mcp-servers/
    ├── conference-sessions/
    │   ├── server.py           # MCP server
    │   ├── database.py         # SQLite operations
    │   ├── parser.py           # Parse session data
    │   ├── sessions.db         # SQLite database
    │   └── requirements.txt
    └── msgraph-demo/
        ├── server.py           # MCP server
        ├── oauth_manager.py    # OAuth handling
        ├── graph_client.py     # Graph API wrapper
        └── requirements.txt
```

---

## Comparison: MCP vs A2A vs ACP vs Skills

### MCP (Model Context Protocol)
**What**: Open protocol for connecting AI assistants to data sources
**Focus**: Tool-based data access
**Architecture**: Client ↔ MCP Server ↔ Data Source
**Use Case**: AI needs to query/interact with external systems
**Example**: AI assistant querying conference sessions database

### A2A (Agent-to-Agent)
**What**: Protocol for autonomous agents to communicate
**Focus**: Inter-agent communication and coordination
**Architecture**: Agent ↔ Agent (peer-to-peer)
**Use Case**: Multiple AI agents collaborating on complex tasks
**Example**: Planning agent coordinating with execution agent

### ACP (Agent Communication Protocol)
**What**: Standardized messaging between AI agents
**Focus**: Message passing and state synchronization
**Architecture**: Hub-and-spoke or mesh network of agents
**Use Case**: Multi-agent systems with complex workflows
**Example**: Swarm of specialized agents solving distributed problems

### Anthropic Skills
**What**: Packaged capabilities that extend Claude's functionality
**Focus**: Reusable, composable AI enhancements
**Architecture**: Skill → MCP (often) → Data/Tools
**Use Case**: Adding domain-specific knowledge or capabilities to Claude
**Example**: Email-reader skill providing email management via scripts
**Evolution**: Skills often leverage MCP under the hood for data access

**Key Insight for Presentation**:
- **MCP** = AI accessing YOUR data
- **A2A/ACP** = AIs talking to EACH OTHER
- **Skills** = Packaged capabilities (often using MCP)

---

## Demo Execution Plan

### Pre-Demo Setup
1. Build and test both MCP servers
2. Create sample queries that showcase capabilities
3. Ensure OAuth is pre-authenticated for Graph demo
4. Pre-populate calendar with a test event
5. Have fallback screenshots/videos
6. Set up audience participation slide with your-email@your-domain.com

### Demo Flow - Two-Part Approach

**PART 1: Simple Demo - Conference Sessions (3-4 min)**

*Goal: Quick win, show MCP basics with relatable data*

Show in Claude Desktop/CLI:
1. "Show me all sessions about Copilot"
2. "Who is speaking in Room G7?" (that's YOUR room!)
3. "Find all beginner-friendly sessions"
4. "What sessions mention AI or Copilot in the description?"

**Key Talking Points**:
- This is YOUR conference data, accessible to AI
- No complex setup - just tools and data
- MCP makes AI contextually aware
- Same pattern works for ANY data source
- **"My prompts never left my laptop - local AI processed everything"**
- **"No OpenAI, no Anthropic needed for basic reasoning"**

**Transition**: "That was simple. Now let's see something more powerful..."

---

**PART 2: Detailed Demo - Microsoft Graph (5-7 min)**

*Goal: Show enterprise integration, security, read/write capabilities*

**Audience Participation Setup** (during presentation):
- Show slide: "Send an email to your-email@your-domain.com suggesting a session I should attend"
- Subject: "Check out Session [number]!" or session name
- Give 30 seconds for people to send

**Live Demo in Claude Desktop/CLI**:
1. "Show me all Copilot Studio sessions"
   - Uses Conference Sessions MCP
   - Shows multiple options
2. "Show me emails from the last hour"
   - Uses Graph MCP
   - Shows emails from audience members!
3. "What session did [name] suggest?"
   - Read the email content
4. "Add Session 87 to my calendar for Thursday, November 6 at 9am"
   - **MCP Composition!** Takes session data + creates calendar event
   - Demonstrates write capability
5. "Show my calendar for November 6"
   - Verify the session was added
   - Shows the complete workflow worked

**Key Talking Points**:
- OAuth provides enterprise-grade security
- Same MCP pattern, different data source
- AI can READ and WRITE (with permissions)
- This is how you connect AI to YOUR enterprise systems
- Works with any API: Salesforce, Jira, ServiceNow, etc.
- **"Local AI model orchestrated this - my prompts stayed private"**
- **"Only API calls went over the network - secured with OAuth"**
- **"Best of both worlds: privacy + power"**

**Visual Impact**:
- Audience sees THEIR emails appear in the demo
- Shows real-time integration
- Makes it tangible and memorable

---

## Success Criteria

### Technical
- Both MCP servers working reliably
- Clean, readable code (Level 100/200 appropriate)
- Proper error handling
- OAuth flow works smoothly

### Presentation
- Slides are clear and engaging
- Live demos execute without issues
- Audience understands "why MCP matters"
- Clear takeaways and next steps

### Educational
- Audience leaves understanding MCP basics
- They see practical value for their work
- They know how to get started
- They understand how MCP fits with other protocols

---

## Timeline & Milestones

1. **Architecture & Planning** ✅
2. **Parse & Store Conference Data** - Next
3. **Build Conference Sessions MCP Server**
4. **Build Microsoft Graph MCP Server**
5. **Test Both Servers**
6. **Create PowerPoint Presentation**
7. **Practice Demo**
8. **Final Polish**

---

*This architecture will be updated as we build and learn*
