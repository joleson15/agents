from anthropic import Anthropic
from .default_provider import ModelProvider
from typing import Union

class AnthropicModelProvider(ModelProvider):

    def __init__(
            self,
            model: str="claude-3-5-haiku-20241022",
            tools: list = []
            ):
        
        self.anthropic = Anthropic()
        self.model=model
        self.tools=tools

        #context module
        self.memory_module = [] #basic list for now

    def add_to_memory(message):
        pass


    def send_message(self, query: Union[str, None] = None, role: str = "user"):

        if query is not None:
            message = {
                    "role": role,
                    "content": query
                }
            

            self.memory_module.append(message)

        response = self.anthropic.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=self.memory_module,
            tools=self.tools
        )

        return response
    

    async def process_query(self, query: str) -> str:

        response = self.send_message(query)

        final_text = []
        assistant_message_content = []
        for content in response.content:
            
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)

            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)

                self.memory_module.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })

                self.memory_module.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                response = self.send_message()

                final_text.append(response.content[0].text)

        return "\n".join(final_text)
    