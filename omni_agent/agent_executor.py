from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_task, new_agent_text_message
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, Part, TextPart
from contextlib import asynccontextmanager
import asyncio

from .client import MCPClient

class OmniAgentExecutor(AgentExecutor):

    def __init__(self, status_message: str = "Executing task...", artifact_name: str = "response"):
        self.agent: MCPClient = None
        self.status_message = status_message
        self.artifact_name = artifact_name
        self._cleanup_lock = asyncio.Lock()
        self._is_cleaned_up = False
        
    @classmethod
    async def create(cls):
        self = cls()
        self.agent = await MCPClient.create()
        return self
    
    @asynccontextmanager
    async def _get_agent_context(self):
        """Context manager to ensure proper agent lifecycle management"""
        if self._is_cleaned_up:
            # Recreate agent if it was cleaned up
            self.agent = await MCPClient.create()
            self._is_cleaned_up = False
        
        try:
            yield self.agent
        except Exception as e:
            # Clean up on error
            await self._safe_cleanup()
            raise e
    
    async def _safe_cleanup(self):
        """Thread-safe cleanup method"""
        async with self._cleanup_lock:
            if not self._is_cleaned_up and self.agent:
                try:
                    await self.agent.cleanup()
                except Exception as e:
                    print(f"Warning: Error during cleanup: {e}")
                finally:
                    self._is_cleaned_up = True
                    self.agent = None

    async def cleanup(self):
        """Clean up resources when the executor is destroyed"""
        await self._safe_cleanup()

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
            async with self._get_agent_context() as agent:
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
            await self._safe_cleanup()

    def cancel(self, context, event_queue):
        pass
    
    async def __aenter__(self):
        """Async context manager entry"""
        if not self.agent:
            self.agent = await MCPClient.create()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()