import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://www.google.com/travel/flights/search?tfs=CBwQAholEgoyMDI1LTA4LTAxag4IAhIKL20vMDJocmgwX3IHCAESA1NBTkABSAFwAYIBCwj___________8BmAEC",
            config=run_conf
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
