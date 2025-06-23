from google.adk.agents import Agent
from google.adk.tools import google_search
from . import prompt


MODEL = "gemini-2.5-pro-preview-05-06"

trend_spotter_agent = Agent(
    model= MODEL,
    name="trend_spotter",
    description="An agent that finds and reports on AI agent trends",
    instruction=prompt.TREND_SPOTTER_PROMPT,
    tools=[google_search]
)

root_agent = trend_spotter_agent