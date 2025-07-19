from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from omni_client.client import MCPClient
import asyncio

class LittlehorseAgent:

    def __init__(self, host: str = '127.0.0.1', port: int = 9999):
        self.mcp_client = MCPClient()
        self.host = host
        self.port = port

    #this doesn keep the session open
    async def initialize_client(self):

       await self.mcp_client.connect_to_server("sse", url="http://localhost:8081/mcp/sse")


    #TODO: implement auto gen of skills
    async def get_skills(self):
        response = await self.mcp_client.session.list_tools()

        version_skill = AgentSkill(
        id="get_littlehorse_version_skill",
        name="Get Server Version",
        description="Retrievs the version of the Littlehorse server",
        tags=["server", "version", "server version"]
        )

        return [version_skill]
    
    async def get_agent_card(self):

        self.agent_card = AgentCard(
            name="littlehorse_agent",
            description="A Littlehorse agent that can run workflows",
            url=f"http://{self.host}:{self.port}",
            version='0.1.0',
            capabilities=AgentCapabilities(
                streaming=True
            ),
            defaultInputModes=["text", "text/plain"],
            defaultOutputModes=["text", "text/plain"],
            skills= await self.get_skills()
        )