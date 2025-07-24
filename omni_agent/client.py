from typing import Optional, Dict, Any, Union
from contextlib import AsyncExitStack
import asyncio

from mcp import ClientSession
from mcp.client.session_group import ClientSessionGroup, SseServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters
from anthropic import Anthropic
from .config import DefaultMCPClientConfig
from .providers.anthropic_provider import AnthropicModelProvider
import json

from contextlib import asynccontextmanager
from dotenv import load_dotenv
import json

load_dotenv()

class MCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.config = DefaultMCPClientConfig()
        self.provider = AnthropicModelProvider()
        
        self.anthropic = Anthropic() #temp
        self.session_group = ClientSessionGroup()
        self.tools = []
        self.sessions = []
        
    def get_server_parameters(self):
            
        server_parameters: Dict[str, Union[SseServerParameters, StdioServerParameters]] = {} #streamable http not yet supported

        file_path = "/home/joleson/work/agents/omni_agent/mcp.json"

        with open(file_path) as f:
            server_json = json.load(f)

        if not isinstance(server_json, dict):
            raise TypeError(f"Unable to parse {file_path}")

        server_dict: Dict[str, Any] = server_json
        server_config: Dict[str, dict] = server_dict.get("mcpServers")

        if not isinstance(server_config, dict):
            raise TypeError(f"Unable to parse mcp servers")
        
        for name, params in server_config.items():

            if params.get("type") == "sse":
                server_parameters[name] = SseServerParameters(
                    url=params.get("url")
                )
            
            elif params.get("type") == "stdio":
                server_parameters[name] = StdioServerParameters(
                    command=params.get("command"),
                    args=params.get("args"),
                    env=params.get("env")
                )
            
            else:
                raise TypeError(f"Field 'type' not properly set for item: {name}")
        
        return server_parameters
    

    @asynccontextmanager
    async def connect(self, serverparams: Union[StdioServerParameters, SseServerParameters]):

        if isinstance(serverparams, StdioServerParameters):
            client = stdio_client(serverparams)
            
        elif isinstance(serverparams, SseServerParameters):
            client = sse_client(
                url=serverparams.url,
                )

            # elif transport == "streamable-http":
            #     client = streamablehttp_client(**serverparams)
            # else:
            #     raise ValueError(
            #         f"Invalid transport, expected sse or streamable-http found `{transport}`"
            #     )
        else:
            raise ValueError(
                f"Invalid serverparams, expected StdioServerParameters or dict found `{type(serverparams)}`"
            )

        timeout = None
        # if isinstance(client_session_timeout_seconds, float):
        #     timeout = timedelta(seconds=client_session_timeout_seconds)
        # elif isinstance(client_session_timeout_seconds, timedelta):
        #     timeout = client_session_timeout_seconds

        async with client as (read, write, *_):
            async with ClientSession(
                read,
                write,
                timeout,
            ) as session:
                # Initialize the connection and get the tools from the mcp server
                await session.initialize()
                tools = await session.list_tools()
                yield session, tools.tools
                

    async def __aenter__(self):
        self._ctxmanager = AsyncExitStack()

        connections = [
            await self._ctxmanager.enter_async_context(
                self.connect(params)
            )
            for params in self.get_server_parameters().values()
        ]

        self.sessions, self.mcp_tools = [list(c) for c in zip(*connections)]

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._ctxmanager.__aexit__(exc_type, exc_val, exc_tb)
        
    async def process_query(self, query: str) -> str:

        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for _, tool in self.session_group.tools.items()]

        messages = [
            {
                "role": "user",
                "content": query
            }
        ]
        
        response = self.anthropic.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        final_text = []
        assistant_message_content = []
        for content in response.content:
            
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)

            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                result = await self.session_group.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)

                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                response = self.anthropic.messages.create(
                            model="claude-3-5-haiku-20241022",
                            max_tokens=1000,
                            messages=messages,
                            tools=available_tools
                        )
                
                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def chat_loop(self):
        print("\nMCP Client Started...")
        print("What can I help you with? Type 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")


    async def cleanup(self):
        await self.exit_stack.aclose()


if __name__ == "__main__":

    client = MCPClient()

    print([value for value in client.get_server_parameters().values()])
    