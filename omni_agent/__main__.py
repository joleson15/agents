from .client import MCPClient
import asyncio
import signal
import sys

async def main():
    async with MCPClient() as client:
        print(client.tools)

if __name__ == "__main__":
    asyncio.run(main())