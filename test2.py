from playwright.sync_api import sync_playwright

def scrape_google_maps(search_query):
    # Construct the Google Maps search URL
    base_url = "https://www.google.com/maps/search/"
    url = base_url + search_query.replace(" ", "+")  # Replace spaces with '+' for URL

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible browser for debugging
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)  # Wait for initial page load

        # Store scraped data
        all_data = []

        # Loop for Pagination
        while True:
            print("\nScraping Current Page...")

            # Extract data from current page
            names = page.locator('//div[contains(@class, "qBF1Pd") and contains(@class, "fontHeadlineSmall")]').all_text_contents()
            ratings = page.locator('//span[contains(@aria-label, "stars")]').all_text_contents()
            addresses = page.locator('//div[contains(@class, "W4Efsd")]').all_text_contents()

            # Combine results into a list of dictionaries
            for i in range(len(names)):
                business = {
                    "Name": names[i] if i < len(names) else "N/A",
                    "Rating": ratings[i] if i < len(ratings) else "N/A",
                    "Address": addresses[i] if i < len(addresses) else "N/A"
                }
                all_data.append(business)

                # Print current result
                print(f"Name: {business['Name']}")
                print(f"Rating: {business['Rating']}")
                print(f"Address: {business['Address']}")
                print("-" * 40)

            # Check for next page and paginate
            next_button = page.locator('//button[@aria-label="Next page"]')
            if next_button.is_visible():
                next_button.click()
                page.wait_for_timeout(4000)  # Wait for next page to load
            else:
                print("No More Pages 🔚")
                break

        browser.close()
        return all_data

def main():
    # Get user input for the search query
    search_query = input("Enter the location or business to search on Google Maps (e.g., 'restaurants in New York'): ")
    if not search_query.strip():
        print("No input provided. Exiting.")
        return

    # Scrape data and display summary
    print(f"\nStarting scrape for: '{search_query}'")
    scraped_data = scrape_google_maps(search_query)
    
    # Summary
    print(f"\nTotal businesses scraped: {len(scraped_data)}")
    print("Scraping completed!")

if __name__ == "__main__":
    main()