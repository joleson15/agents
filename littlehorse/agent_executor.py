from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.utils import new_task, new_agent_text_message
from a2a.types import TaskState, Part, TextPart
from omni_client.client import MCPClient


class LittlehorseAgentExecutor(AgentExecutor):

    def __init__(self, agent: MCPClient, status_message: str ="Executing task...", artifact_name: str = "response"):
        self.agent = agent
        self.status_message=status_message
        self.artifact_name=artifact_name
        # self.runner = ...(need memory for context)



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
            #littlhorse checkpoint 1 here
            try:
                await self.agent.connect_to_server("sse", url="http://localhost:8081/mcp/sse")
            except:
                await updater.update_status(
                    TaskState.failed,
                    new_agent_text_message(f"Error: Could not connect to the MCP Server"),
                    final=True
                )

            response = await self.agent.process_query(query)
            print(response)
            await updater.add_artifact(
                [Part(root=TextPart(text=response))],
                name=self.artifact_name
            )
            await self.agent.cleanup()
            await updater.complete()


        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Execution Error: {e!s}", task.contextId, task.id),
                final=True
            )

    def cancel(self, context: RequestContext, event_queue: EventQueue):
        pass