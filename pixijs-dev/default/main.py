"""
Default browser-use example using ChatBrowserUse

The simplest way to use browser-use - capable of any web task
with minimal configuration.
"""

import asyncio

from dotenv import load_dotenv

from browser_use import Agent, Browser, ChatGoogle

load_dotenv()

async def main():
    llm = ChatGoogle(model="gemini-flash-latest")
    task = "Find the number 1 post on Show HN"
    agent = Agent(task=task, llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())


