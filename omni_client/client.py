from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters
from anthropic import Anthropic
from config import DefaultMCPClientConfig
from providers.anthropic_provider import AnthropicModelProvider

from dotenv import load_dotenv
import json

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.config = DefaultMCPClientConfig()
        self.provider = AnthropicModelProvider()
        self.anthropic = Anthropic()
        self.model_name = "claude-3-5-haiku-20241022"


        #session group

    async def connect_to_server(self, transport: str, url: str=None, server_script_path: str=None):

        """
        Args:
            transport: Transport type (sse or stdio)

        """
        if transport == "sse":

            sse_transport = await self.exit_stack.enter_async_context(sse_client(url=url))
            self.sse, self.write = sse_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.sse, self.write))
            await self.session.initialize()
            response = await self.session.list_tools()
            tools = response.tools
            available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
            } for tool in response.tools]
            self.provider.tools = available_tools
            print("\nConnected to server with tools:", [tool.name for tool in tools])

        elif transport == "stdio":
            # parse json
            with open(server_script_path) as f:
                config = json.load(f)
            command, args, env = config["mcpServers"].items()
            
            params = StdioServerParameters(command=command, args=args, env=env)
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(params))
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            await self.session.initialize()
            response = await self.session.list_tools()
            tools = response.tools
            print("\nConnected to server with tools:", [tool.name for tool in tools])

        else:
            pass
            #error: must be sse or stdio
        

    async def chat_loop(self):
        print("\nMCP Client Started...")
        print("What can I help you with? Type 'quit' to exit.")


        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.provider.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")


    async def cleanup(self):
        await self.exit_stack.aclose()