# MCP Inspector Test Guide

## 🎯 Testing Both MCP Servers

### Current Status
- ✅ **Conference Sessions MCP** running on http://localhost:6274
- ⏳ **Graph MCP** - will start next

---

## Test 1: Conference Sessions MCP

**Inspector URL**: http://localhost:6274

### Tools Available (should see 6):
1. `search_sessions`
2. `get_session_by_id`
3. `list_all_tracks`
4. `list_all_speakers`
5. `filter_by_location`
6. `filter_by_level`

### Test Queries:

#### A. Search for MCP Sessions
**Tool**: `search_sessions`
**Input**:
```json
{
  "query": "MCP",
  "limit": 10,
  "response_format": "markdown"
}
```
**Expected**: Should find Session 127 (your presentation!)

---

#### B. Get Your Session Details
**Tool**: `get_session_by_id`
**Input**:
```json
{
  "session_id": 127,
  "response_format": "markdown"
}
```
**Expected**: Full details of "Getting started with Model Context Protocol"

---

#### C. Find Copilot Studio Sessions
**Tool**: `search_sessions`
**Input**:
```json
{
  "query": "Copilot Studio",
  "limit": 10,
  "response_format": "markdown"
}
```
**Expected**: Session 87 and others about Copilot Studio

---

#### D. What's in Room G7? (Your Room!)
**Tool**: `filter_by_location`
**Input**:
```json
{
  "location": "Room G7",
  "response_format": "markdown"
}
```
**Expected**: All sessions in Room G7, including yours

---

#### E. List All Tracks
**Tool**: `list_all_tracks`
**Input**:
```json
{
  "response_format": "markdown"
}
```
**Expected**: All conference tracks with session counts

---

## Test 2: Graph MCP (Next)

**To Start**: 
```bash
cd /path/to/TechCon365Dallas2025/mcp-servers/msgraph-demo
TENANT_ID="485a3633-bdd7-4b94-a9d4-1e7e2f9de3e2" \
CLIENT_ID="a17fca6a-4062-45ca-9115-7214b2b68de2" \
# CLIENT_SECRET not needed - using device code flow (public client) \
npx @modelcontextprotocol/inspector /path/to/your/python3 server.py
```

### Tools Available (should see 4):
1. `graph_read_emails`
2. `graph_search_emails`
3. `graph_create_calendar_event`
4. `graph_get_calendar_events`

### Test Queries:

#### A. Read Recent Emails
**Tool**: `graph_read_emails`
**Input**:
```json
{
  "limit": 5,
  "folder": "inbox",
  "response_format": "markdown"
}
```
**Expected**: Your 5 most recent emails (including today's!)

---

#### B. Search for TechCon Emails
**Tool**: `graph_search_emails`
**Input**:
```json
{
  "query": "TechCon",
  "limit": 10,
  "response_format": "markdown"
}
```
**Expected**: Emails mentioning TechCon365

---

#### C. View Calendar for November 6
**Tool**: `graph_get_calendar_events`
**Input**:
```json
{
  "start_date": "2025-11-06",
  "end_date": "2025-11-06",
  "limit": 20,
  "response_format": "markdown"
}
```
**Expected**: Your calendar events for demo day

---

#### D. Create Test Calendar Event
**Tool**: `graph_create_calendar_event`
**Input**:
```json
{
  "subject": "Test MCP Event",
  "start_datetime": "2025-11-05T14:00:00",
  "end_datetime": "2025-11-05T15:00:00",
  "location": "Test Room",
  "body": "Testing MCP calendar creation",
  "response_format": "markdown"
}
```
**Expected**: Event created successfully with confirmation

---

#### E. Add Session 87 to Calendar (MCP Composition Prep!)
**Tool**: `graph_create_calendar_event`
**Input**:
```json
{
  "subject": "Session 87: Building Smart Agents with Copilot Studio",
  "start_datetime": "2025-11-06T09:00:00",
  "end_datetime": "2025-11-06T10:00:00",
  "location": "Room A",
  "body": "TechCon365 Dallas 2025 - Copilot Studio session",
  "response_format": "markdown"
}
```
**Expected**: Session 87 added to your calendar for Thursday morning

---

## ✅ Success Criteria

### Conference Sessions MCP:
- [ ] All 6 tools appear in Inspector
- [ ] Search returns Session 127 (your session)
- [ ] Session 127 details show Room G7, Thursday 2:20-3:30 PM
- [ ] Copilot Studio search finds Session 87
- [ ] Room G7 filter works
- [ ] Track list complete

### Graph MCP:
- [ ] All 4 tools appear in Inspector
- [ ] Authentication works (gets access token)
- [ ] Read emails returns TODAY's emails (not old database)
- [ ] Search emails works
- [ ] Calendar view works for Nov 6
- [ ] **Calendar creation works** (write operation!)
- [ ] Can add Session 87 to calendar

---

## 🐛 Troubleshooting

### If Conference Sessions MCP fails:
- Check: Is sessions.db present?
- Check: Python can import mcp, pydantic, sqlite3
- Check: Server is actually running in terminal

### If Graph MCP fails to authenticate:
- Check: Environment variables are set (TENANT_ID, CLIENT_ID, CLIENT_SECRET)
- Check: Token cache folder exists: `~/.msgraph-mcp/`
- May need device code flow (will prompt in terminal)
- Check: MSAL library installed: `pip install msal`

### If emails are old/cached:
- This means it's working! (reading from Graph API)
- Old means database was being used before
- New/today emails = SUCCESS!

---

## 📊 What Success Looks Like

**Conference Sessions MCP**: ✅ Already working, just verifying in Inspector

**Graph MCP**: 
- Gets fresh emails from TODAY (not Oct 27!)
- Can create calendar events (write operation works)
- Authentication successful
- All 4 tools functional

**MCP Composition**: (Manual test later)
- Use Conference MCP data
- Create calendar event with Graph MCP
- Demonstrates two servers working together

---

## 🎬 Demo Flow Preview

Once both work in Inspector:

1. **Search sessions** → Conference MCP → Find Session 87
2. **Read emails** → Graph MCP → See audience suggestions
3. **Create event** → Graph MCP → Add Session 87 to calendar
4. **Verify** → Graph MCP → Show calendar with new event

**This proves MCP composition works!**

---

## Commands Quick Reference

### Start Conference Sessions Inspector:
```bash
cd /path/to/TechCon365Dallas2025/mcp-servers/conference-sessions
npx @modelcontextprotocol/inspector /path/to/your/python3 server.py
```

### Start Graph MCP Inspector:
```bash
cd /path/to/TechCon365Dallas2025/mcp-servers/msgraph-demo
TENANT_ID="485a3633-bdd7-4b94-a9d4-1e7e2f9de3e2" \
CLIENT_ID="a17fca6a-4062-45ca-9115-7214b2b68de2" \
# CLIENT_SECRET not needed - using device code flow (public client) \
npx @modelcontextprotocol/inspector /path/to/your/python3 server.py
```

### Stop Inspector:
- Ctrl+C in the terminal where it's running

---

*Test with MCP Inspector to verify both servers work without Claude Desktop limits!*
