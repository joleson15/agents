from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from client import MCPClient
import asyncio
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from agent_executor import LittlehorseAgentExecutor
from a2a.server.tasks import InMemoryTaskStore
from agent import LittlehorseAgent
import uvicorn


# async def init_agent():

#     agent = LittlehorseAgent()
#     # await agent.initialize_client()
#     # await agent.get_agent_card()

#     return agent

    

if __name__ == "__main__":
    # littlehorse_agent = asyncio.run(init_agent())
    host = '127.0.0.1'
    port = 9999

    version_skill = AgentSkill(
        id="get_littlehorse_version_skill",
        name="Get Server Version",
        description="Retrievs the version of the Littlehorse server",
        tags=["server", "version", "server version"]
        )
    
    agent_card = AgentCard(
            name="littlehorse_agent",
            description="A Littlehorse agent that can run workflows",
            url=f"http://{host}:{port}",
            version='0.1.0',
            capabilities=AgentCapabilities(
                streaming=True
            ),
            defaultInputModes=["text", "text/plain"],
            defaultOutputModes=["text", "text/plain"],
            skills=[version_skill]
        )
    # mcp_client = MCPClient()

    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=DefaultRequestHandler(
            agent_executor=LittlehorseAgentExecutor(MCPClient()),
            task_store=InMemoryTaskStore()
        )
    )
    uvicorn.run(app.build(), host=host, port=port)