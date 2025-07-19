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
        await page.act("click the dropdown menu and click 'one way'")
        await page.act("there are three fields to fill out, from left to right: origin, destination, date")
        await page.act("for the first field, click it and fill in honolulu, second one click it and fill in san diego, third field click departure and click august 1st for the date")
        # await agent.execute("search for one-way flights from honolulu to san diego on august 1st 2025, find me some options")

        result = await page.extract("find me some flight options for august 1st from honolulu to san diego")

        print(f"Extracted: {result.extraction}")

    finally:
        await stagehand.close()

if __name__ == "__main__":
    asyncio.run(main())