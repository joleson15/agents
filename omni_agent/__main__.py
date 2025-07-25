from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from .client import OmniAgentExecutor
import asyncio
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore
import uvicorn

async def main():
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
    
    async with OmniAgentExecutor() as omni_agent_executor:

        app = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=DefaultRequestHandler(
                agent_executor=omni_agent_executor,
                task_store=InMemoryTaskStore()
            )
        )
        config = uvicorn.Config(app.build(), host=host, port=port, loop="asyncio")
        server = uvicorn.Server(config)
        await server.serve()

if __name__ == "__main__":
    asyncio.run(main())