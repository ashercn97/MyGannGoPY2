from playwright.async_api import async_playwright, Playwright
import sys
sys.path.append('./myganngopy')
from utils import login
from utils.nav import NavNested
import asyncio
from runner import main

async def __test__(playwright: Playwright):
    async def run(page, browser):
        config = {'page': page, 'browser': browser, 'log': True, 'test': False}
        navigation = NavNested(config)
        await navigation.report_dropdown.run("View_Assignment_Grades")

    await main(run)
    print("TESTS PASSED SUCCESSFULLY")

if __name__ == "__main__":
    asyncio.run(__test__(async_playwright()))
