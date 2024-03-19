import requests
import sys
sys.path.append('./myganngopy')
from utils import get_cookies
import asyncio
from runner import main
from playwright.async_api import async_playwright, Playwright
import json
import base64
import time

# ty chatgpt
async def download_pdf(page, url, save_path):
    # Navigate to the PDF URL
    await page.goto(url)

    # Use JavaScript to fetch the PDF and convert it to a base64 string
    pdf_base64 = await page.evaluate("""
        async (url) => {
            const response = await fetch(url);
            const blob = await response.blob();
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            });
        }
    """, url)

    # Decode the base64 string and write the PDF binary to a file
    with open(save_path, "wb") as f:
        f.write(base64.b64decode(pdf_base64.split(",")[1]))




async def get_pdf(page, file_path):
    cookies = await get_cookies(page)
    request_verification_token = await page.evaluate("""document.getElementsByName("__RequestVerificationToken")[0].value""")

    cookies_dict = {}
    
    for c in cookies:
        cookies_dict[c['name']] = c['value']
    



    headers = {
        'authority': 'gannacademy.myschoolapp.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,la;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://gannacademy.myschoolapp.com',
        'referer': 'https://gannacademy.myschoolapp.com/app/student',
        'requestverificationtoken': request_verification_token,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320',
        'wh-version': '2024.03.11.3',
        'x-requested-with': 'XMLHttpRequest',
    }



    json_data = {
        'ReportId': '215',
        'ReportParameters': '7574746:,:15992:,:7574746:,:',
        'Format': 'pdf',
        'GeneralReport': True,
    }



    response = requests.post(
        'https://gannacademy.myschoolapp.com/api/Report/ReportJob',
        cookies=cookies_dict,
        headers=headers,
        json=json_data
    )


    job_id = response.text
    print("JOB ID: ", job_id)

    new_url = f"https://gannacademy.myschoolapp.com/api/Report/ReportJob/{job_id}"
    print("URL NAVIGATING TO: ", new_url)


    time.sleep(3)

    # go to the new url
    await page.goto(new_url)

    # download it!

    await download_pdf(page, new_url, filepath)
    

    
    





async def __test__(playwright):
    async def run(page, browser):
        await get_pdf(page, "output.pdf")

    await main(run)

if __name__ == "__main__":
    asyncio.run(__test__(async_playwright()))