# Graph MCP Troubleshooting Guide

## 🔴 Issue Discovered: MCP Server Conflict

**Date**: October 31, 2025

### The Problem

When testing "show me recent emails" in Claude Desktop, it used the **wrong MCP server**:

- ❌ **Used**: `Fabs-Graph-Search` (database-based, old emails from Oct 27)
- ✅ **Should use**: `msgraph` (live Graph API, current emails)

### Why This Happened

You have **three** email-related MCP servers in your config:
1. `Fabs-Graph-Utils` - General Graph utilities
2. `Fabs-Graph-Search` - **Database search (competes with new server!)**
3. `msgraph` - **Our new live API server**

When Claude Desktop sees ambiguous requests like "show recent emails," it picks one of the available servers. In this case, it picked `Fabs-Graph-Search` instead of `msgraph`.

---

## ✅ Solutions

### Option 1: Temporarily Disable Competing Server (RECOMMENDED for Demo)

**Edit**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Comment out or remove `Fabs-Graph-Search` section**:

```json
{
  "mcpServers": {
    "Fabs-Graph-Utils": {
      "command": "npx",
      "args": ["-y", "@fabianwilliams/graph-utils"]
    },
    // COMMENTED OUT FOR DEMO:
    // "Fabs-Graph-Search": {
    //   "command": "npx",
    //   "args": ["--yes", "@fabianwilliams/graph-search-mcp"],
    //   "env": { ... }
    // },
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

**Then**: Restart Claude Desktop (Cmd+Q, reopen)

**Benefit**: Forces Claude to use your new `msgraph` server for email queries

---

### Option 2: Use Explicit Tool Names

Instead of: "show me recent emails"

**Use**: "Use the **graph_read_emails** tool to show me recent emails"

**Or**: "Using the msgraph server, show me recent emails"

**Benefit**: No config changes needed, explicitly calls the right tool

---

### Option 3: Rename Your MCP Server

Change the server name in config to be more distinct:

```json
"techcon-demo-msgraph": {
  "command": "/path/to/your/python3",
  ...
}
```

**Benefit**: More descriptive, less chance of confusion

---

## 🧪 Testing Steps

### Test 1: Verify Server Loads
```bash
# Should show msgraph in the list
# Check Claude Desktop UI for MCP servers
```

### Test 2: Check Authentication
The server uses client credentials flow with the provided CLIENT_SECRET.

**First time**: May need to authenticate via device flow if client secret doesn't work for delegated permissions.

**Token cache**: `~/.msgraph-mcp/token_cache.json`

### Test 3: Test Each Tool Individually

**Using explicit tool names**:

1. **graph_read_emails**: "Use graph_read_emails to show my last 5 emails"
2. **graph_search_emails**: "Use graph_search_emails to find emails about TechCon"
3. **graph_get_calendar_events**: "Use graph_get_calendar_events for November 6"
4. **graph_create_calendar_event**: "Use graph_create_calendar_event to add 'Test Session' tomorrow at 2pm"

### Test 4: Test MCP Composition

**The Money Shot**:
```
1. "Show me all Copilot Studio sessions" (Conference MCP)
2. "Use graph_read_emails to show emails from the last hour" (Graph MCP)
3. "Add Session 87 (Building Smart Agents with Copilot Studio) to my calendar for Thursday, November 6 at 9am in Room A" (MCP COMPOSITION!)
4. "Show my calendar for November 6" (Graph MCP verification)
```

---

## 🐛 Potential Issues & Fixes

### Issue: "Authentication failed"

**Cause**: Token expired or invalid credentials

**Fix**:
1. Delete token cache: `rm -rf ~/.msgraph-mcp/`
2. Restart Claude Desktop
3. May trigger device flow authentication

### Issue: "Permission denied"

**Cause**: App doesn't have required Graph API permissions

**Fix**: Check Azure AD app registration has these permissions:
- `Mail.Read`
- `Calendars.ReadWrite`
- `User.Read`

### Issue: "Server not found"

**Cause**: Python path or file path incorrect

**Fix**: Verify paths in config:
```bash
ls /path/to/your/python3  # Should exist
ls /path/to/TechCon365Dallas2025/mcp-servers/msgraph-demo/server.py  # Should exist
```

### Issue: Still using Fabs-Graph-Search

**Cause**: Config not reloaded or Claude Desktop cached

**Fix**:
1. Quit Claude Desktop completely (Cmd+Q)
2. Wait 5 seconds
3. Reopen Claude Desktop
4. Check MCP servers list

---

## 📋 Pre-Demo Checklist

### Configuration
- [ ] Decide: Keep or disable `Fabs-Graph-Search`?
- [ ] Claude Desktop config has `msgraph` server
- [ ] Environment variables are set in config
- [ ] Conference Sessions MCP also configured

### Authentication  
- [ ] Token cache exists: `~/.msgraph-mcp/token_cache.json`
- [ ] Pre-authenticate before demo (don't do device flow on stage!)
- [ ] Test auth works: Run any Graph tool

### Testing
- [ ] All 4 Graph tools work individually
- [ ] Conference MCP tools work
- [ ] **MCP composition works** (find session → add to calendar)
- [ ] Practice the full demo flow

### Backup Plan
- [ ] Screenshots of successful runs
- [ ] Know how to use explicit tool names
- [ ] Have fallback to demo separately if composition fails

---

## 🎯 Recommended Demo Flow

### Setup (Before Presentation)
1. Disable `Fabs-Graph-Search` in config temporarily
2. Restart Claude Desktop
3. Pre-authenticate Graph API (run any tool once)
4. Verify both MCPs working
5. Practice the composition at least once

### During Demo
Use explicit tool names to avoid ambiguity:

```
Me: "Show me all MCP and Copilot Studio sessions"
    → Conference Sessions MCP finds sessions

Me: "Use graph_read_emails to show emails from the last hour"
    → Graph MCP shows audience suggestions

Me: "Add Session 87 to my calendar for Thursday, November 6 at 9am"
    → MCP COMPOSITION! AI combines both servers

Me: "Show my calendar for November 6"
    → Verify the session was added
```

### After Demo
- Re-enable `Fabs-Graph-Search` if needed
- Keep `msgraph` server for future use

---

## 📊 Current Status

### Working ✅
- Conference Sessions MCP (tested and confirmed)
- Graph MCP server code (syntax valid)
- Graph MCP auth manager (initializes correctly)
- Configuration (added to Claude Desktop)

### Needs Testing ⏳
- Graph MCP runtime execution
- Authentication flow with Graph API
- Each of the 4 Graph tools
- **MCP composition workflow**

### Known Issue 🔴
- MCP server conflict with `Fabs-Graph-Search`
- Solution: Use explicit tool names OR disable competing server

---

## 💡 Key Insight

**The issue isn't that your `msgraph` server is broken** - it's that Claude Desktop has multiple options for email operations and chose the wrong one!

**Quick fix**: Use explicit tool names in your demo queries OR temporarily disable the competing server.

---

## 📝 Next Steps

1. **Decide**: Disable Fabs-Graph-Search or use explicit tool names?
2. **Test**: Run Graph tools with explicit names
3. **Verify**: MCP composition works
4. **Practice**: Full demo flow timing
5. **Build**: PowerPoint presentation

**Estimated time**: 15-20 minutes to test and verify everything works

---

*This issue was discovered during initial testing on Oct 31, 2025*
*Root cause: Multiple MCP servers with overlapping capabilities*
*Solution: Explicit tool naming or config adjustment*
