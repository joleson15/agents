from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import asyncio

class Crawl4AIAgent:

    def __init__(self, host: str='127.0.0.1', port: int=9998):
        self.host = host
        self.port = port

        crawl_skill = AgentSkill(
            id="standard_web_crawl",
            name="Standard Web Crawl",
            description="Can access a webpage and extract the content in the form of markdown",
            tags=["web", "crawl", "scrape"]
        )

        adaptive_crawl_skill = AgentSkill(
            id="adaptive_web_crawl",
            name="Adaptive Web Crawl",
            description="Performs an adaptive web crawl, using intelligence to determine when the web crawl has obtained sufficient information",
            tags=["adaptive", "intelligent crawl"]
        )

        self.skills = [crawl_skill, adaptive_crawl_skill]
        
        self.agent_card = AgentCard(
            name="crawl4ai_agent",
            description="""Web Crawler, can access web pages and extract information in the form of markdown.
                Can perform a fast crawl to quickly extract real-time infromation or an adaptive crawl to 
                intelligently determine when the level of information gathered is sufficient. Adaptive crawl great for research tasks.""",
            url=f"https://{self.host}:{self.port}",
            capabilities=AgentCapabilities(streaming=True),
            version="0.1.0",
            defaultInputModes=["text", "text/plain"],
            defaultOutputModes=["text", "text/plain"],
            skills = self.skills
        )

    
    async def web_crawl(url: str="https://example.com"):
        
        browser_config = BrowserConfig()
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig()
            )

            print(result.markdown)

    def adaptive_crawl():
        pass


async def main():
    browser_config = BrowserConfig()  # Default browser configuration
    run_config = CrawlerRunConfig()   # Default crawl run configuration

    # config = CrawlerRunConfig(
    #     markdown_generator=DefaultMarkdownGenerator(
    #         content_filter=PruningContentFilter(threshold=0.6),
    #         options={"ignore_links": True}
    #     )
    # )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.cnbc.com/",
            config=run_config
        )
        print(result.markdown)  # Print clean markdown content


if __name__ == "__main__":
    asyncio.run(main())