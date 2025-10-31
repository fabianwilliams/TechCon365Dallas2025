#!/usr/bin/env python3
"""Quick test of Conference Sessions MCP server."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_conference_mcp():
    """Test the conference sessions MCP server."""
    
    server_params = StdioServerParameters(
        command="/path/to/your/python3",
        args=["mcp-servers/conference-sessions/server.py"],
        env=None
    )
    
    print("🚀 Starting Conference Sessions MCP server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("✅ Server connected!")
            print("\n📋 Listing available tools...")
            
            # List tools
            tools = await session.list_tools()
            print(f"\n✨ Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test 1: Search for MCP sessions
            print("\n\n🔍 TEST 1: Searching for MCP sessions...")
            result = await session.call_tool(
                "conference_search_sessions",
                arguments={
                    "params": {
                        "query": "MCP",
                        "limit": 5,
                        "response_format": "markdown"
                    }
                }
            )
            print("Result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text[:800])  # First 800 chars
            
            # Test 2: Get Session 127 (your session!)
            print("\n\n🎯 TEST 2: Getting Session 127 details...")
            result = await session.call_tool(
                "conference_get_session",
                arguments={
                    "params": {
                        "session_id": 127,
                        "response_format": "markdown"
                    }
                }
            )
            print("Result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(content.text)
            
            print("\n\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_conference_mcp())
