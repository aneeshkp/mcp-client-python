#!/usr/bin/env python3
"""
Custom MCP Client - Core functionality
"""

import asyncio
import json
import re
import sys
import os
from typing import Any, Dict, List, Optional
import aiohttp
from dataclasses import dataclass

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str


class CustomMCPClient:
    def __init__(self, llm_backend):
        self.session: Optional[ClientSession] = None
        self.llm_backend = llm_backend
        self.tools = {}
        self.conversation_history: List[Message] = []
        self.max_history = 20

    async def load_tools(self):
        """Load available tools from the MCP server"""
        try:
            tools_response = await self.session.list_tools()
            
            print(f"📚 Found {len(tools_response.tools)} tools:")
            for tool in tools_response.tools:
                self.tools[tool.name] = tool
                print(f"  - {tool.name}: {tool.description}")
                
        except Exception as e:
            print(f"❌ Failed to load tools: {e}")

    # Add all other methods from our complete client implementation
    # (This is abbreviated for space - use the full version from our artifacts)
