import asyncio
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

from .agent_executor import OmniAgentExecutor
from .client import MCPClient

async def main():
    # Define your agent card
    agent_card = AgentCard(
        name="omni_agent",
        description="An MCP-powered agent with multiple tool capabilities",
        url="http://127.0.0.1:9999",
        version='0.1.0',
        capabilities=AgentCapabilities(
            streaming=True
        ),
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        skills=[]
    )

    # Option 1: Direct context manager usage (as you requested)
    async with OmniAgentExecutor(MCPClient) as executor:
        app = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=DefaultRequestHandler(
                agent_executor=executor,
                task_store=InMemoryTaskStore()
            )
        )
        
        # Run the application
        uvicorn.run(app.build(), host="127.0.0.1", port=9999)

async def main_alternative():
    """Alternative approach using the class method"""
    agent_card = AgentCard(
        name="omni_agent",
        description="An MCP-powered agent with multiple tool capabilities",
        url="http://127.0.0.1:9999",
        version='0.1.0',
        capabilities=AgentCapabilities(
            streaming=True
        ),
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        skills=[]
    )

    # Option 2: Using the class method for even cleaner syntax
    async with OmniAgentExecutor.with_mcp_client() as executor:
        app = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=DefaultRequestHandler(
                agent_executor=executor,
                task_store=InMemoryTaskStore()
            )
        )
        
        # Run the application
        uvicorn.run(app.build(), host="127.0.0.1", port=9999)

if __name__ == "__main__":
    # Use either approach
    asyncio.run(main())
    # or: asyncio.run(main_alternative()) 