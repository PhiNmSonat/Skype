import nest_asyncio
import asyncio
from playwright.async_api import async_playwright

# Allow nested event loops
nest_asyncio.apply()


async def run():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        mail = "email"
        password = "password"

        # Start by going to the Skype login page
        page = await context.new_page()
        await page.goto("https://web.skype.com/")

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

        # Wait for the recent chat list to load by waiting for an element with id containing "rx-vlv"
        await page.wait_for_selector('div[role="listitem"][id*="rx-vlv"]', state='visible')
        print("Recent chat list loaded")



        # Check if the 'Got it!' button is present and click it
        # got_it_button = page.locator('button[aria-label="Got it!"]')
        # if await got_it_button.is_visible():
        #     print("Clicking 'Got it!' button")
        #     await got_it_button.click()
        # else:
        #     print("'Got it!' button not found")

        # Wait for the chat list to load
        # await page.wait_for_selector('div[role="listitem"]', state='visible')

        # Find and click on the chat with the title "Bánh tráng Sonat"
        # Locate the chat with the specific label
        chat_locator = page.locator("div[role='listitem'][aria-label*='Bánh tráng Sonat']")

        # Count the number of matching elements
        chat_count = await chat_locator.count()
        
        if chat_count > 1:
            print(f"Multiple ({chat_count}) chats found. Selecting the correct one.")
            # Handle multiple matches here, e.g., by choosing the second one
            chat_locator = chat_locator.nth(1)  # Adjust the index as needed
        elif chat_count == 1:
            print("Single chat found.")
        else:
            print("No matching chats found.")
            return

        # Check visibility of the selected chat
        if await chat_locator.is_visible():
            print("Chat is visible.")
            await chat_locator.click()
        else:
            print("Chat is not visible.")
        # Wait for the chat to open
        # await page.wait_for_load_state('networkidle')

        # Find and click the search button
        search_button = page.locator('button[title="Find"]')
        if await search_button.is_visible():
            print("Clicking search button")
            await search_button.click()
        else:
            print("Search button not found")

        # Wait for the search input field to become visible
        await page.wait_for_selector('input[placeholder="Search"], input[type="text"]', state='visible')

        # Input the search query
        search_query = "LOA LOA, cả nhà ơi Dino sẽ hỗ trợ mn việc đổi tiền và mua sim để tiết kiệm thời gian nha ạ"  # Replace with your search term
        await page.fill('input[placeholder="Search"], input[type="text"]', search_query)
        print(f"Searching for: {search_query}")

        # Wait for the message to appear
        search_result_locator = page.locator(f'div[role="region"][aria-label*="{search_query}"]')
        await search_result_locator.wait_for(state='visible')
        print("Search result found")

        # Find the first matching element
        # Find the first matching element
        if await search_result_locator.count() > 0:
            # Get the first element matching the locator
            message_element = search_result_locator.nth(0)

            # Find the reaction buttons within this message element
        # Assuming `message_element` is already located

        # Locate all reaction buttons
        reaction_buttons = message_element.locator('button[role="button"]')

        # Count total reaction buttons found
        reaction_buttons_count = await reaction_buttons.count()

        # Initialize the total reactions counter
        total_reactions = 0

        if reaction_buttons_count > 0:
            print(f"Found {reaction_buttons_count} reaction buttons")

            # Iterate through each reaction button and check if it's a reaction
            for i in range(reaction_buttons_count):
                button = reaction_buttons.nth(i)
                title = await button.get_attribute('title')
                aria_label = await button.get_attribute('aria-label')

                # Skip "react to this message" and "More options" buttons
                if "reacted with" not in aria_label:
                    continue

                print(f"Reaction Button Title: {title}")
                print(f"Aria Label: {aria_label}")

                # Locate the div that contains the reaction count, if it exists
                count_elements = button.locator('div[data-text-as-pseudo-element]')
                count_elements_count = await count_elements.count()

                if count_elements_count > 0:
                    # Multiple reactions with counts
                    for j in range(count_elements_count):
                        count_element = count_elements.nth(j)
                        count_text = await count_element.inner_text()
                        print(f"Reactions Count: {count_text}")
                        total_reactions += int(count_text)
                else:
                    # Single reaction (no count displayed)
                    print("1 reaction found (no count displayed)")
                    total_reactions += 1
        else:
            print("No reaction buttons found")

        print(f"Total reactions: {total_reactions}")


        await browser.close()

        # Extract reactions and counts
        # reaction_buttons = search_result_locator.locator('div[role="button"][title*="See who reacted with emoticon"]')
        # total_reactions = 0
        # unique_users = set()



        # Await reaction buttons handles
        # reaction_button_handles = await reaction_buttons.element_handles()

        # Loop through each reaction button
        # reaction_buttons_count = await reaction_buttons.count()
        # print(f"Found {reaction_buttons_count} reaction buttons")

        # for i in range(reaction_buttons_count):
        #     reaction_button = reaction_buttons.nth(i)
        #     # Get the reaction count
        #     reaction_count_text = await reaction_button.locator('div[data-text-as-pseudo-element]').inner_text()
        #     if reaction_count_text.isdigit():
        #         total_reactions += int(reaction_count_text)
        #     else:
        #         # If not a digit, handle it as a single reaction
        #         total_reactions += 1

        #     # Get the users who reacted
        #     aria_label = await reaction_button.get_attribute('aria-label')
        #     if aria_label:
        #         users = aria_label.split(' reacted with ')[0].split(' and ')
        #         unique_users.update(users)

        # print(f"Total reactions: {total_reactions}")
        # print(f"Total unique users: {len(unique_users)}")



        # Close browser
        # await browser.close()

# Running the async function in the current event loop
asyncio.get_event_loop().run_until_complete(run())