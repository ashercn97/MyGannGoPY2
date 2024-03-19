from playwright.async_api import async_playwright, Playwright
import asyncio
import time
from dotenv import dotenv_values



'''
    Logs into MyGann, returns a page that is logged-in

    page: a playwright page


    it also loads the dotenv file so you can deal with password stuff securly
'''
async def login(page):
    info = dotenv_values(".env")
    #print(info)
    username = info["MYGANN_USERNAME"]
    password = info["MYGANN_PASSWORD"]


    await page.goto("https://gannacademy.myschoolapp.com/app#login", wait_until="load")
    await page.wait_for_selector("#Username", state="visible")
    usernameSelector = await page.query_selector("#Username")
    await usernameSelector.fill(username)
    await page.wait_for_selector("input[type=submit]", state="visible")
    await page.click("input[type=submit]")
    await page.wait_for_selector("#i0118", state="visible")
    await page.fill("#i0118", password)
    await page.click("#idSIButton9")
    await page.click("xpath=/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input")

    await page.click("xpath=/html/body/div[2]/div/form/div/div/div/div/div/div[2]/div[1]/div/div/form/div/span[1]/input")

    # FINALLLY IT WORKED

    # return the page

    return page


