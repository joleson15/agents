import asyncio
from client import MCPClient

littlehorse_mcp = 'http://localhost:8081/mcp/sse'

async def main():
    client = MCPClient()
    try:
        await client.connect_to_server(transport="sse", url=littlehorse_mcp)
        await client.chat_loop()

    except:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())