# Quick Test Guide - Conference Sessions MCP

## 🚀 Ready to Test!

All setup is complete. Follow these steps to test the MCP server.

---

## Step 1: Restart Claude Desktop

**IMPORTANT**: You must restart Claude Desktop to load the new MCP server.

1. Quit Claude Desktop completely (Cmd+Q)
2. Reopen Claude Desktop
3. Wait for it to fully load

---

## Step 2: Verify Server is Loaded

Look for the MCP icon or check if tools from "conference-sessions" are available.

If you see errors:
- Check Claude Desktop logs
- Verify the config file syntax is valid JSON
- Ensure the path to server.py is correct

---

## Step 3: Run Test Queries

### Test 1: Basic Search ⭐
**Try this first!**

```
Show me all sessions about Copilot
```

**Expected**: Should return multiple sessions mentioning Copilot in title/description

**What this tests**: Full-text search, markdown formatting

---

### Test 2: Location Filter (YOUR ROOM!) 🎯
**Super relevant!**

```
What sessions are happening in Room G7?
```

**Expected**: Should show YOUR session "Getting started with Model Context Protocol (MCP) and Why Should You Care"

**What this tests**: Location filtering, seeing yourself in the data

---

### Test 3: List All Tracks 📋

```
What are all the conference tracks?
```

**Expected**: Should list 70+ tracks with session counts

**What this tests**: Enumeration tool, data aggregation

---

### Test 4: Level Filtering 🎓

```
Show me all beginner-friendly sessions
```

**Expected**: Should return 49 Intro/Overview level sessions

**What this tests**: Level filtering, result count handling

---

### Test 5: Speaker Search 🎤

```
What sessions is Fabian Williams speaking at?
```

**Expected**: Should find your MCP session in Room G7

**What this tests**: Speaker search, personal relevance

---

### Test 6: Complex Query with Filters 🔍

```
Find intermediate level sessions about AI in Room G1
```

**Expected**: Should filter by level AND track AND location

**What this tests**: Multiple filters working together

---

## Step 4: Document Results

After each test, update `TESTING.md` with:
- ✅ Success or ❌ Failure
- What worked well
- What needs improvement
- Any errors or unexpected behavior

---

## Common Issues & Fixes

### Server not appearing
- **Fix**: Check config file is valid JSON (no trailing commas!)
- **Fix**: Verify full path to server.py
- **Fix**: Restart Claude Desktop completely

### Database errors
- **Fix**: Verify sessions.db exists in the same folder as server.py
- **Fix**: Run `python database.py` to rebuild if needed

### Import errors
- **Fix**: Install dependencies: `pip install mcp pydantic`
- **Fix**: Use the correct Python path (miniforge3 in your case)

---

## Success Criteria ✅

The server is ready for the demo if:

- [x] All 6 tools load without errors
- [ ] Search returns relevant results
- [ ] Location filter finds Room G7 sessions
- [ ] Markdown output is readable
- [ ] Error messages are clear
- [ ] Response times are fast (<2 seconds)

---

## What to Look For

### Good Signs ✅
- Quick responses (under 2 seconds)
- Clean markdown formatting
- Relevant results for queries
- Clear error messages for invalid input
- All 6 tools available

### Red Flags ❌
- Timeouts or crashes
- No results for valid queries
- Malformed output
- Missing tools
- Unclear error messages

---

## After Testing

1. Document results in `TESTING.md`
2. Update `JOURNEY.md` with findings
3. Note any improvements needed
4. Prepare demo queries for presentation

---

## Demo-Ready Queries 🎬

Once testing is complete, these are your go-to queries for the live demo:

1. **"Show me all sessions about Copilot"**
   - Quick, impressive results
   - Relevant to conference theme

2. **"Who is speaking in Room G7?"**
   - **YOU!** Great moment for the audience
   - Shows location filtering

3. **"Find all beginner-friendly sessions"**
   - Shows level filtering
   - Useful for attendees

4. **"What sessions mention AI or Copilot in the description?"**
   - Demonstrates full-text search depth
   - Multiple results

5. **"List all the conference tracks"**
   - Shows data enumeration
   - Helps attendees understand conference scope

---

## Next Steps After Testing

Depending on results:

**If everything works**: ✅
- Document successes
- Prepare demo script
- Move to building Graph MCP or Presentation

**If issues found**: 🔧
- Document problems
- Fix critical bugs
- Re-test
- Then proceed

---

**Ready? Restart Claude Desktop and start testing!** 🚀
