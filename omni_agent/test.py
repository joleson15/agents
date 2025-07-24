from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from .client import MCPClient
import asyncio
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from .agent_executor import OmniAgentExecutor
from a2a.server.tasks import InMemoryTaskStore
import uvicorn
import signal
import sys

omni_agent_executor = None

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

    # Create executor with proper async context management
    # omni_agent_executor = await OmniAgentExecutor.create()

    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=DefaultRequestHandler(
            agent_executor=omni_agent_executor,
            task_store=InMemoryTaskStore()
        )
    )
    
    return app.build(), host, port, omni_agent_executor


if __name__ == "__main__":

    try:
        app, host, port, executor = asyncio.run(main())
        print(f"Starting server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\nReceived interrupt signal")