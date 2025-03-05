from playwright.sync_api import sync_playwright

def scrape_google_maps(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)  # Wait for page load
        
        # Loop for Pagination
        while True:
            print("\nScraping Current Page...")

            # Restaurant Name
            names = page.locator('//div[contains(@class, "qBF1Pd") and contains(@class, "fontHeadlineSmall")]').all_text_contents()
            
            # Ratings
            ratings = page.locator('//span[contains(@aria-label, "stars")]').all_text_contents()

            # Address
            addresses = page.locator('//div[contains(@class, "W4Efsd")]').all_text_contents()

            # Print Results
            for i in range(len(names)):
                print(f"Name: {names[i]}")
                if i < len(ratings):
                    print(f"Rating: {ratings[i]}")
                if i < len(addresses):
                    print(f"Address: {addresses[i]}")
                print("-" * 40)

            # Pagination (Next Page)
            if page.locator('//button[@aria-label="Next page"]').is_visible():
                page.locator('//button[@aria-label="Next page"]').click()
                page.wait_for_timeout(4000)  # Wait for next page to load
            else:
                print("No More Pages 🔚")
                break

        browser.close()

url = "https://www.google.com/maps/search/HashtrustTechnologies"
scrape_google_maps(url)
