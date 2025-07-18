import os
from dotenv import load_dotenv
import asyncio
from stagehand import Stagehand, StagehandConfig

load_dotenv("../.env")

async def main():
    config = StagehandConfig(
        env="LOCAL",
        model_name="openai/gpt-4.1-mini",
        model_api_key = os.getenv("OPENAI_API_KEY")
    )

    stagehand = Stagehand(config)

    try:

        await stagehand.init()
        page = stagehand.page

        agent = stagehand.agent(
            model="computer-use-preview",
            instructions="You are a helpful assistant that can use a web browser.",
            options={
            "apiKey": os.getenv("OPENAI_API_KEY"),
            },
        )

        await page.goto("https://www.google.com/travel/flights")
        await agent.execute("search for one-way flights from honolulu to san diego on august 1st 2025, find me some options")

        result = await page.extract("find me some options")

        print(f"Extracted: {result.extraction}")

    finally:
        await stagehand.close()

if __name__ == "__main__":
    asyncio.run(main())