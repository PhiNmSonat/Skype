import nest_asyncio
import asyncio
from playwright.async_api import async_playwright

# Allow nested event loops
nest_asyncio.apply()

async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        
        # Check if auth state file exists
        try:
            await context.add_cookies_from_file('auth_state.json')
        except FileNotFoundError:
            pass
        
        mail = "email"
        password = "password"

        # Start by going to the Skype login page
        page = await context.new_page()
        await page.goto("https://web.skype.com/")

        # Check if already logged in
        if not await page.query_selector('div[data-text-as-pseudo-element="Welcome!"]'):
            # Perform the login steps
            await page.fill('input[type="email"]', mail)
            print("filled")
            await page.click('#idSIButton9')
            print("clicked")

            await page.wait_for_selector('#i0118', state='visible', timeout=60000)
            await page.fill('#i0118', password)
            print("filled pass")
            await page.click('#idSIButton9')
            print("clicked pass")

            await page.click('#acceptButton')

            # Wait for the welcome message or any specific element that signifies the page is fully loaded
            await page.wait_for_selector('div[data-text-as-pseudo-element="Welcome!"]', state='visible')
            print("Logged in successfully, page fully loaded")
            
            # Save the authentication state for future logins
            await context.storage_state(path='auth_state.json')
            print("Authentication state saved")

        # Retrieve x-skypetoken from cookies or network requests
        cookies = await context.cookies()
        x_skypetoken = next((cookie['value'] for cookie in cookies if cookie['name'] == 'x-skypetoken'), None)
        if x_skypetoken:
            print(f"x-skypetoken: {x_skypetoken}")
        else:
            print("x-skypetoken not found")

        # Cleanup
        await browser.close()

asyncio.get_event_loop().run_until_complete(run())
