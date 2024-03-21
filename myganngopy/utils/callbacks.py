import asyncio

"""
    This function generates the report, downloads the report,
    and saves it to the file path specifiede
"""
async def generate_report(page):
    # click the generate report button
    await page.click("xpath=/html/body/form/div[6]/span/table/tbody/tr/td/div/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div[2]/table[1]/tbody/tr/td[1]/a")
    
    # wait for the download button to appear
        