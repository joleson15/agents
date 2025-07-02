from client import MCPClient
import asyncio
import json


async def main():
    
    client = MCPClient()

    try:
        await client.connect_to_server(transport="stdio", server_script_path="./mcp.json")
        # result = await client.process_query("test")
        # print(result)
        await client.chat_loop()
    finally:
        await client.cleanup()
    
if __name__ == "__main__":
    
    
    asyncio.run(main())

    # with open("mcp.json") as f:
    #     config = json.load(f)
    
    # servers = config.get("mcpServers", {})
    
    # for server_name, server_config in servers.items():

    #     command = server_config.get("command")
    #     args = server_config.get("args")
    #     env = server_config.get("env")
        
        
    #     print(command, args, env)
    #     print(server_name)