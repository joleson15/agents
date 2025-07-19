from client import MCPClient
import asyncio



async def main():

    mcp_client = MCPClient()

    try:
        await mcp_client.connect_to_server("sse", "http://localhost:8081/mcp/sse")
        await mcp_client.chat_loop()

    finally:
        await mcp_client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())