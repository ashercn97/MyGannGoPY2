import asyncio


async def get_cookies(page):
    cookies = await page.context.cookies()
    return cookies
