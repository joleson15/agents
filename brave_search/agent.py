from omni_client.client import MCPClient
import asyncio
import json


async def main():

    client = MCPClient()

    try:
        await client.connect_to_server(transport="stdio", server_script_path="./mcp.json")
        await client.chat_loop()
    finally:
        await client.cleanup()
    
if __name__ == "__main__":
    
    asyncio.run(main())