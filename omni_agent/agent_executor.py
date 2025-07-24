from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_task, new_agent_text_message
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, Part, TextPart
from contextlib import asynccontextmanager
import asyncio

from .client import MCPClient

class OmniAgentExecutor(AgentExecutor):

    def __init__(self, agent: MCPClient, status_message: str = "Executing task...", artifact_name: str = "response"):
        self.agent: MCPClient = agent
        self.status_message = status_message
        self.artifact_name = artifact_name
        
        
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        
        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message) 

        updater = TaskUpdater(event_queue, task.id, task.contextId)

        try:
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message, task.contextId, task.id)
            )

            # Use context manager to ensure proper lifecycle
            async with self.agent as agent:
                response = await agent.process_query(query)
            
            await updater.add_artifact(
                [Part(root=TextPart(text=response))],
                name=self.artifact_name
            )

            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Execution Error: {e!s}", task.contextId, task.id),
                final=True
            )
            # Clean up on error
            await self.agent.cleanup()

    def cancel(self, context, event_queue):
        pass