from anthropic import Anthropic
from providers.default_provider import ModelProvider

class AnthropicModelProvider(ModelProvider):

    def __init__(
            self,
            model: str="claude-3-5-haiku-20241022",
            tools: list = []
            ):
        
        self.anthropic = Anthropic()
        self.model=model
        self.tools=tools


    def send_message(self, user_query: str):

        message = [
            {
                "role": "user",
                "content": user_query
            }
        ]

        response = self.anthropic.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=message,
            tools=self.tools
        )

        return response