import asyncio
from playwright.async_api import async_playwright, Playwright
import sys
sys.path.append('./myganngopy')
from utils import login

async def run(playwright: Playwright, function):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()

    page = await login(page)

    await function(page, browser)

    await browser.close()

async def main(function):
    async with async_playwright() as playwright:
        await run(playwright, function)
