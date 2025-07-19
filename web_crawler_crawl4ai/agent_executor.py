from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution import RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_task, new_agent_text_message
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState
from agent import Crawl4AIAgent

class Crawl4AIAgentExecutor(AgentExecutor):

    def __init__(self, agent: Crawl4AIAgent, status_message: str="Crawling page...", artifact_name: str="response"):

        self.status_message=status_message
        self.artifact_name=artifact_name
        self.agent = Crawl4AIAgent() if agent is None else agent

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        
        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)

        updater = TaskUpdater(event_queue, task.id, task.contextId)

        try:
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message)
            )

            
        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Execution Error: {e!s}", task.contextId, task.id),
                final=True
            )

    
    def cancel(self, context: RequestContext, event_queue: EventQueue):
        pass