from runner import main
from utils import login, get_cookies
import asyncio
from playwright.async_api import async_playwright, Playwright
import time

async def __test__(playwright: Playwright):
    async def run(page, browser):
        #page = await login(page)
        time.sleep(5)
        cookies = await get_cookies(page)
        print(cookies)

    await main(run)
    print("TESTS PASSED SUCCESSFULLY")

if __name__ == "__main__":
    asyncio.run(__test__(async_playwright()))
