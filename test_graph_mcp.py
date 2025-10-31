#!/usr/bin/env python3
"""Quick test of Graph MCP server."""

import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_graph_mcp():
    """Test the Microsoft Graph MCP server."""
    
    server_params = StdioServerParameters(
        command="/path/to/your/python3",
        args=["mcp-servers/msgraph-demo/server.py"],
        env={
            "TENANT_ID": "485a3633-bdd7-4b94-a9d4-1e7e2f9de3e2",
            "CLIENT_ID": "a17fca6a-4062-45ca-9115-7214b2b68de2",
            "CLIENT_SECRET": "not-needed-for-device-flow"
        }
    )
    
    print("🚀 Starting Microsoft Graph MCP server...")
    
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
            
            # Test 1: Read recent emails
            print("\n\n📧 TEST 1: Reading recent emails...")
            try:
                result = await session.call_tool(
                    "graph_read_emails",
                    arguments={
                        "params": {
                            "limit": 3,
                            "folder": "inbox",
                            "response_format": "markdown"
                        }
                    }
                )
                print("Result:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text[:800])  # First 800 chars
            except Exception as e:
                print(f"❌ Error: {e}")
                print("(This might be an auth issue - that's OK for now)")
            
            # Test 2: Get calendar events
            print("\n\n📅 TEST 2: Getting calendar events for Nov 6...")
            try:
                result = await session.call_tool(
                    "graph_get_calendar_events",
                    arguments={
                        "params": {
                            "start_date": "2025-11-06",
                            "end_date": "2025-11-06",
                            "limit": 10,
                            "response_format": "markdown"
                        }
                    }
                )
                print("Result:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text[:800])
            except Exception as e:
                print(f"❌ Error: {e}")
                print("(This might be an auth issue - that's OK for now)")
            
            print("\n\n✅ Tool listing worked! Auth may need device flow.")

if __name__ == "__main__":
    asyncio.run(test_graph_mcp())
