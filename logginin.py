

from playwright.async_api import async_playwright, Playwright
import asyncio
from myganngopy import login
from myganngopy import nav

async def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()

    page = await login(page)

    config = {'page': page, 'log': True, 'test': False, 'browser': browser}

    navigation = nav.NavNested(config)

    await navigation.progress_navbar.run("Progress_Button_List")

    

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())