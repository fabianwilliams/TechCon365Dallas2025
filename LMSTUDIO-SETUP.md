# LM Studio MCP Configuration Guide

## 📍 LM Studio MCP Config Location

LM Studio looks for MCP configuration in:
```
~/Library/Application Support/LM Studio/mcp_config.json
```

## 🚀 Setup Instructions

### Option 1: Copy the Config File (Recommended)

```bash
# Copy the config to LM Studio
cp /path/to/TechCon365Dallas2025/lmstudio-mcp-config.json \
   ~/Library/Application\ Support/LM\ Studio/mcp_config.json

# Restart LM Studio
```

### Option 2: Manual Setup

1. Open LM Studio
2. Go to **Settings** → **MCP Servers**
3. Add the configuration from `lmstudio-mcp-config.json`
4. Restart LM Studio

---

## ✅ Configuration Details

### Conference Sessions MCP
- **Name**: `conference-sessions`
- **Command**: Python 3 from miniforge
- **Script**: Conference sessions server
- **Purpose**: Search and query TechCon365 sessions

### Microsoft Graph MCP
- **Name**: `msgraph`
- **Command**: Python 3 from miniforge
- **Script**: Microsoft Graph server
- **Purpose**: Access emails and calendar
- **Auth**: Uses cached token from `~/.msgraph-mcp/token_cache.json`

---

## 🧪 Testing in LM Studio

### Test Conference Sessions MCP

**Prompt**: "Show me all sessions about MCP at the conference"

**Expected**: Should find Session 127 and other MCP-related sessions

**Tools Used**: `conference_search_sessions`

---

### Test Graph MCP

**Prompt**: "Show me my recent emails"

**Expected**: Should display your recent inbox emails

**Tools Used**: `graph_read_emails`

**Note**: Uses the token you already cached via device code flow

---

### Test MCP Composition

**Prompt**: "Find Copilot Studio sessions at TechCon, then add Session 87 to my calendar for Thursday, November 6 at 9am"

**Expected**: 
1. Conference MCP finds sessions
2. Graph MCP creates calendar event
3. Both MCPs work together!

**Tools Used**: `conference_search_sessions` + `graph_create_calendar_event`

---

## 🔧 Troubleshooting

### MCPs Don't Appear in LM Studio

**Solution**:
1. Check config file exists: `ls ~/Library/Application\ Support/LM\ Studio/mcp_config.json`
2. Verify JSON is valid: `cat ~/Library/Application\ Support/LM\ Studio/mcp_config.json | python3 -m json.tool`
3. Restart LM Studio completely
4. Check LM Studio console/logs for errors

---

### Graph MCP Authentication Errors

**Solution**: Token should already be cached from our setup. If you get auth errors:

```bash
# Re-run the auth setup
cd /path/to/TechCon365Dallas2025
python3 setup_graph_auth.py
```

---

### Python Path Issues

**Solution**: If LM Studio can't find Python:

```bash
# Verify Python path
which python3
# Should show: /path/to/your/python3

# If different, update the config file with the correct path
```

---

### Conference Sessions Database Not Found

**Solution**: Verify database exists:

```bash
ls -lh /path/to/TechCon365Dallas2025/mcp-servers/conference-sessions/sessions.db
# Should show ~401KB file
```

---

## 🎯 Quick Command Reference

### Copy Config to LM Studio
```bash
cp lmstudio-mcp-config.json ~/Library/Application\ Support/LM\ Studio/mcp_config.json
```

### View Current LM Studio Config
```bash
cat ~/Library/Application\ Support/LM\ Studio/mcp_config.json
```

### Test Conference MCP Directly
```bash
cd /path/to/TechCon365Dallas2025
python3 test_conference_mcp.py
```

### Test Graph MCP Directly
```bash
cd /path/to/TechCon365Dallas2025
python3 test_graph_mcp.py
```

### Re-authenticate Graph API
```bash
cd /path/to/TechCon365Dallas2025
python3 setup_graph_auth.py
```

---

## 📊 Available Tools

### Conference Sessions (6 tools)
1. `conference_search_sessions` - Search by keyword
2. `conference_get_session` - Get session by ID
3. `conference_list_tracks` - List all tracks
4. `conference_list_speakers` - List all speakers
5. `conference_get_sessions_by_location` - Filter by room
6. `conference_get_sessions_by_level` - Filter by difficulty

### Microsoft Graph (4 tools)
1. `graph_read_emails` - Read recent emails
2. `graph_search_emails` - Search emails by keyword
3. `graph_create_calendar_event` - Create calendar event
4. `graph_get_calendar_events` - View calendar

---

## ✨ Example Prompts for LM Studio

### Conference Sessions
- "Show me all Copilot sessions"
- "What sessions are in Room G7?"
- "Find beginner-friendly sessions"
- "Who is speaking about AI?"
- "Get details for Session 127"

### Graph Integration
- "Show my recent emails"
- "Search my emails for TechCon"
- "Show my calendar for November 6"
- "Add 'Test Meeting' to my calendar tomorrow at 2pm"

### MCP Composition
- "Find Power Platform sessions and add the first one to my calendar"
- "Show me SharePoint sessions, then show my calendar for next week"
- "Search for Azure sessions and tell me if I have any conflicts on Thursday"

---

## 🎬 Demo-Ready Status

✅ **Both MCPs configured**  
✅ **Authentication complete** (token cached)  
✅ **All 10 tools available**  
✅ **Live data access working**  
✅ **Ready to use in LM Studio!**

---

## 📝 Notes

- **Token Location**: `~/.msgraph-mcp/token_cache.json`
- **Token Auto-Refresh**: Yes (MSAL handles it)
- **Multi-Tenant**: Yes (using 'common' endpoint)
- **Permissions**: Mail.Read, Calendars.ReadWrite, User.Read

---

*Created: October 31, 2025*  
*Both MCPs tested and verified working*
