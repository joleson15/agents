from .client import MCPClient
import asyncio
import signal
import sys

async def main():
    async with MCPClient() as client:
        await client.chat_loop()
        
if __name__ == "__main__":
    asyncio.run(main())