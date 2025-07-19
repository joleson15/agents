from anthropic import Anthropic
from openai import OpenAI
from google import genai
from providers.default_provider import ModelProvider
from providers.anthropic_provider import AnthropicModelProvider


class DefaultMCPClientConfig:

    def __init__(self, provider: ModelProvider = AnthropicModelProvider()):
        self.provider = provider
        # self.servers = list of MCP servers with various config (its own object? MCPServer()?)


if __name__ == "__main__":

    anthropic = Anthropic()
    openai = OpenAI()
    google = genai()

    # anthropic
    # openai.