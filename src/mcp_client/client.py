#!/usr/bin/env python3
"""
Custom MCP Client with Python
Supports multiple LLM backends and Kubernetes environments
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
        self.max_history = 20  # Keep last 20 messages for context
    
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
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a specific MCP tool"""
        try:
            print(f"🔧 Calling tool: {tool_name} with args: {arguments}")
            
            result = await self.session.call_tool(tool_name, arguments)
            
            # Format the result
            output = ""
            for content in result.content:
                if hasattr(content, 'text'):
                    output += content.text + "\n"
                elif hasattr(content, 'type') and content.type == 'text':
                    output += str(content) + "\n"
            
            return output.strip()
            
        except Exception as e:
            print(f"❌ Tool call failed: {e}")
            return f"Error calling tool {tool_name}: {str(e)}"
    
    def format_tools_for_prompt(self) -> str:
        """Format available tools for the LLM prompt"""
        if not self.tools:
            return ""
        
        tools_desc = "\n\nYou have access to the following tools:\n"
        for name, tool in self.tools.items():
            tools_desc += f"- {name}: {tool.description}\n"
            
            # Add parameter info if available
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                schema = tool.inputSchema
                if 'properties' in schema:
                    params = list(schema['properties'].keys())
                    tools_desc += f"  Parameters: {', '.join(params)}\n"
        
        tools_desc += "\nTo use a tool, respond with exactly this format:\n"
        tools_desc += "TOOL_USE: tool_name\n"
        tools_desc += "PARAMETERS: {\"param1\": \"value1\", \"param2\": \"value2\"}\n"
        tools_desc += "\nOnly use tools when they're needed to answer the user's question.\n"
        
        return tools_desc
    
    def build_conversation_context(self) -> str:
        """Build conversation context for the LLM"""
        context = "You are a helpful AI assistant with access to various tools.\n"
        context += self.format_tools_for_prompt()
        
        if self.conversation_history:
            context += "\nConversation history:\n"
            # Use recent history to avoid token limits
            recent_messages = self.conversation_history[-self.max_history:]
            for msg in recent_messages:
                context += f"{msg.role}: {msg.content}\n"
        
        return context
    
    async def process_user_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Add user message to history
        self.conversation_history.append(Message("user", user_input))
        
        # Build context and get LLM response
        context = self.build_conversation_context()
        context += f"\nuser: {user_input}\nassistant: "
        
        print("🤖 Thinking...")
        response = await self.llm_backend.generate(context)
        
        # Check if response contains tool use
        if "TOOL_USE:" in response:
            return await self.handle_tool_use(response, user_input)
        
        # Add assistant response to history
        self.conversation_history.append(Message("assistant", response))
        return response
    
    async def handle_tool_use(self, response: str, original_input: str) -> str:
        """Handle tool use in LLM response"""
        try:
            # Parse tool use
            tool_match = re.search(r'TOOL_USE:\s*(\w+)', response)
            param_match = re.search(r'PARAMETERS:\s*({.*?})', response, re.DOTALL)
            
            if not tool_match:
                return "I tried to use a tool but couldn't parse the tool name."
            
            tool_name = tool_match.group(1).strip()
            
            # Parse parameters
            parameters = {}
            if param_match:
                try:
                    param_str = param_match.group(1).strip()
                    parameters = json.loads(param_str)
                except json.JSONDecodeError as e:
                    return f"I tried to use {tool_name} but the parameters were malformed: {e}"
            
            # Check if tool exists
            if tool_name not in self.tools:
                available_tools = list(self.tools.keys())
                return f"Tool '{tool_name}' not found. Available tools: {', '.join(available_tools)}"
            
            # Call the tool
            tool_result = await self.call_tool(tool_name, parameters)
            
            # Generate final response based on tool result
            final_prompt = f"""
User asked: {original_input}

I used the tool '{tool_name}' and got this result:
{tool_result}

Please provide a natural, helpful response to the user based on this information.
Don't mention the technical details of tool usage - just give a clear answer.
"""
            
            final_response = await self.llm_backend.generate(final_prompt)
            
            # Add to conversation history
            self.conversation_history.append(Message("assistant", final_response))
            return final_response
            
        except Exception as e:
            print(f"❌ Error handling tool use: {e}")
            return f"I encountered an error while using the tool: {str(e)}"
    
    async def interactive_session(self):
        """Start interactive chat session"""
        print("\n🎉 Custom MCP Client is ready!")
        print("💡 Ask me anything and I'll help using the available tools.")
        print("📝 Commands: 'quit' to exit, 'tools' to list tools, 'history' to show conversation")
        print("🔄 'clear' to clear conversation history\n")
        
        while True:
            try:
                user_input = input("🚀 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'tools':
                    print("\n📚 Available tools:")
                    for name, tool in self.tools.items():
                        print(f"  - {name}: {tool.description}")
                    print()
                    continue
                
                if user_input.lower() == 'history':
                    print("\n📜 Conversation History:")
                    for i, msg in enumerate(self.conversation_history[-10:], 1):
                        print(f"  {i}. {msg.role}: {msg.content[:100]}...")
                    print()
                    continue
                
                if user_input.lower() == 'clear':
                    self.conversation_history.clear()
                    print("🧹 Conversation history cleared!")
                    continue
                
                if not user_input:
                    continue
                
                # Process the input
                response = await self.process_user_input(user_input)
                print(f"\n🤖 Assistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
