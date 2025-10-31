# TechCon365 Dallas 2025 - MCP Demo Project
**Session**: Getting Started with Model Context Protocol (MCP) and Why Should You Care  
**Speaker**: Fabian Williams  
**Room**: G7  
**Time**: Thursday, November 6, 2025 - 2:20 PM to 3:30 PM

---

## 🎯 Project Overview

This repository contains two production-ready MCP servers demonstrating **MCP composition** - where multiple independent servers work together through AI orchestration. 

### 🔒 The Local AI Advantage

**Key Innovation**: Local AI models (via LM Studio) accessing enterprise APIs through MCP - combining **privacy of local processing** with **power of cloud services**.

- ✅ Your prompts **never leave your machine**
- ✅ AI reasoning happens **100% locally**
- ✅ Only OAuth-secured API calls travel over network
- ✅ **Zero data sent to OpenAI, Anthropic, or any cloud AI provider**

---

## 🚀 What We Built

### 1. Conference Sessions MCP
**Purpose**: Query TechCon365 Dallas 2025 conference session data  
**Data**: 182 sessions in SQLite database with FTS5 full-text search  
**Tools**: 6 tools for searching, filtering, and browsing sessions

### 2. Microsoft Graph MCP
**Purpose**: Enterprise integration with Microsoft 365 (Calendar, Email)  
**Auth**: OAuth 2.0 device code flow with token caching  
**Tools**: 4 tools for reading emails, searching, creating calendar events

---

## 🎊 Verified MCP Composition

**Status**: ✅ **WORKING IN PRODUCTION**

**Demo Flow**:
1. Search conference sessions → **Local AI + Conference MCP**
2. Add session to calendar → **Local AI + Graph MCP**
3. Verify in Outlook → **Real calendar event created!**

**Privacy Guarantee**:
- User prompts processed by local LLM (LM Studio)
- Conference data queried from local database
- Only Microsoft Graph API calls traveled over network (OAuth-protected)
- **No prompts, reasoning, or context sent to cloud AI providers**

---

## 📊 Key Benefits

### Privacy & Compliance
- ✅ Prompts stay on-premise
- ✅ Meet HIPAA, PCI-DSS, GDPR requirements
- ✅ No AI training on your data
- ✅ Audit trail of API access only

### Cost Control
- ✅ Pay once for hardware, not per-token
- ✅ No recurring cloud AI costs
- ✅ ROI in months with heavy usage

### Performance
- ✅ No cloud latency for AI reasoning
- ✅ Local database queries: < 1 second
- ✅ Your hardware, your control

### Flexibility
- ✅ Works offline (for local data)
- ✅ Any local model (Llama, Mistral, DeepSeek, etc.)
- ✅ Any API (via MCP standard protocol)
- ✅ No vendor lock-in

---

## 📁 Repository Structure

```
├── mcp-servers/
│   ├── conference-sessions/     # Search TechCon sessions
│   │   ├── server.py           # 6 MCP tools
│   │   ├── sessions.db         # 182 sessions
│   │   └── requirements.txt
│   └── msgraph-demo/           # Microsoft Graph integration
│       ├── server.py           # 4 MCP tools
│       ├── graph_auth.py       # OAuth manager
│       └── requirements.txt
├── presentation/               # PowerPoint slides (TBD)
├── ARCHITECTURE.md             # Technical design
├── JOURNEY.md                  # Development journey
├── MCP-COMPOSITION-SUCCESS.md  # Demo verification
├── LOCAL-AI-MCP-BENEFITS.md    # Privacy/cost benefits
└── FINAL-STATUS.md             # Current status
```

---

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- LM Studio (or Claude Desktop)
- Microsoft account (for Graph MCP)

### 1. Clone Repository
```bash
git clone https://github.com/fabianwilliams/TechCon365Dallas2025.git
cd TechCon365Dallas2025
```

### 2. Install Dependencies
```bash
# Conference Sessions MCP
cd mcp-servers/conference-sessions
pip install -r requirements.txt
cd ..

# Microsoft Graph MCP
cd msgraph-demo
pip install -r requirements.txt
cd ../..
```

### 3. Setup Authentication (One-time)
```bash
# Authenticate with Microsoft Graph using device code flow
python setup_graph_auth.py
```

### 4. Configure LM Studio
```bash
# Create local config from template
cp lmstudio-mcp-config.json.template lmstudio-mcp-config.json

# Edit the file to update paths:
# - Replace "/path/to/your/python" with your Python executable
# - Replace "/path/to/TechCon365Dallas2025" with your clone path
```

**Example LM Studio config** (after updating paths):
```json
{
  "mcpServers": {
    "conference-sessions": {
      "command": "/usr/local/bin/python3",
      "args": ["/Users/yourname/TechCon365Dallas2025/mcp-servers/conference-sessions/server.py"]
    },
    "msgraph": {
      "command": "/usr/local/bin/python3", 
      "args": ["/Users/yourname/TechCon365Dallas2025/mcp-servers/msgraph-demo/server.py"],
      "env": {
        "TENANT_ID": "common",
        "CLIENT_ID": "14d82eec-204b-4c2f-b7e8-296a70dab67e"
      }
    }
  }
}
```

### 5. Load in LM Studio
- Copy your `lmstudio-mcp-config.json` to LM Studio's config directory
- Restart LM Studio
- Both MCPs will be available

---

## 🎬 Live Demo

### Try This in LM Studio
```
1. "Show me all sessions about Model Context Protocol"
   → Conference MCP searches 182 sessions

2. "Add the first result to my calendar"
   → Graph MCP creates calendar event

3. "Show my calendar for November 6"
   → Verify event created
```

**Watch**: Your prompts never leave your machine, but you get full enterprise integration!

---

## 📚 Learn More

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical design and demo flow
- **[LOCAL-AI-MCP-BENEFITS.md](LOCAL-AI-MCP-BENEFITS.md)** - Privacy, cost, and compliance advantages
- **[MCP-COMPOSITION-SUCCESS.md](MCP-COMPOSITION-SUCCESS.md)** - Verified demo results
- **[JOURNEY.md](JOURNEY.md)** - Development story from start to finish

---

## 🎯 Presentation Topics

1. **MCP Basics** - What it is and why it matters
2. **Local AI Advantage** - Privacy + power without cloud dependency
3. **Live Demo** - Conference search + calendar creation
4. **MCP vs A2A vs ACP** - Protocol comparison
5. **Real-World Use Cases** - Healthcare, finance, legal, enterprise
6. **Getting Started** - Resources and next steps

---

## 🏆 Success Metrics

- ✅ Both MCP servers: **100% functional**
- ✅ MCP composition: **Verified working**
- ✅ Real calendar event: **Created in Outlook**
- ✅ Local AI privacy: **Zero cloud exposure**
- ✅ Demo reliability: **Repeatable and fast**

---

## 🤝 Connect

**Fabian Williams**  
Session: Getting Started with MCP  
Room G7, Thursday Nov 6, 2025, 2:20-3:30 PM

Questions? Feedback? Let's talk about MCP!

---

*Built with: FastMCP, Python, SQLite, Microsoft Graph API, OAuth 2.0, LM Studio*  
*Privacy-first architecture: Local AI + Enterprise APIs = Best of both worlds*

