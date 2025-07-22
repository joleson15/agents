from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_task, new_agent_text_message
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, Part, TextPart
from contextlib import asynccontextmanager

from .client import MCPClient

class OmniAgentExecutorPerRequest(AgentExecutor):
    """
    Alternative executor that creates a new MCP client for each request.
    This ensures proper cleanup but may be less efficient for multiple requests.
    """

    def __init__(self, status_message: str = "Executing task...", artifact_name: str = "response"):
        self.status_message = status_message
        self.artifact_name = artifact_name
        
    @asynccontextmanager
    async def _get_client_for_request(self):
        """Create a new MCP client for each request"""
        client = None
        try:
            client = await MCPClient.create()
            yield client
        finally:
            if client:
                await client.cleanup()

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

            # Create a new client for this request
            async with self._get_client_for_request() as client:
                response = await client.process_query(query)
            
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

    def cancel(self, context, event_queue):
        pass 