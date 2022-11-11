import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) # p.webkit -> safari    p.chromium -> chrome/opera/edge  p.firefox
    # The default headless's value is true meaning no browser UI will open up.
    page = browser.new_page()
    page.goto('https://www.youtube.com/')
    
    #page.locator('xpath=/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/div/div[2]/input').click()
    page.fill('xpath=/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/div/div[2]/input', 'Blackfriday')
    page.locator('xpath=/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/button').click()
    time.sleep(5)
    