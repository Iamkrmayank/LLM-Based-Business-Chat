from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import csv
import os
from time import sleep

def scrape_google_maps(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Setting True Status for headless mode
        page = browser.new_page()

        try:
            print(f"Navigating to {url}...")
            page.goto(url, timeout=60000)  # Increasing the timeout to 60 seconds
            page.wait_for_timeout(5000)  # Waiting for the pages to load

            new_data = []  # Storing scraped data

            while True:
                print("Scraping current page...")

                # Scroll to load all listings (Google Maps often lazy-loads content)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                sleep(2)  # Give time for lazy-loaded content

                # Locate all business listing containers
                listings = page.locator('//div[contains(@class, "Nv2PK")]').all()

                if not listings:
                    print("No listings found on this page.")
                    break

                for listing in listings:
                    try:
                        business_name = listing.locator('.qBF1Pd.fontHeadlineSmall').text_content(timeout=5000).strip() or "N/A"
                    except PlaywrightTimeoutError:
                        business_name = "N/A"

                    try:
                        rating = listing.locator('span[aria-label*="stars"]').text_content(timeout=2000).strip() or "N/A"
                    except PlaywrightTimeoutError:
                        rating = "N/A"

                    try:
                        reviews = listing.locator('.UY7F9').text_content(timeout=2000).strip('()').strip() or "N/A"
                    except PlaywrightTimeoutError:
                        reviews = "N/A"

                    try:
                        category = listing.locator('.W4Efsd >> nth=0').text_content(timeout=2000).strip() or "N/A"
                    except PlaywrightTimeoutError:
                        category = "N/A"

                    try:
                        address = listing.locator('.W4Efsd >> nth=1').text_content(timeout=2000).strip() or "N/A"
                    except PlaywrightTimeoutError:
                        address = "N/A"

                    try:
                        status_locator = listing.locator('div:text-matches("Open|Closed")')
                        status = status_locator.text_content(timeout=2000).strip() if status_locator.count() > 0 else "N/A"
                    except PlaywrightTimeoutError:
                        status = "N/A"

                    try:
                        website_locator = listing.locator('a:text("Website")')
                        website = website_locator.get_attribute('href', timeout=2000) if website_locator.count() > 0 else "N/A"
                    except PlaywrightTimeoutError:
                        website = "N/A"

                    try:
                        directions_locator = listing.locator('a:text("Directions")')
                        directions = directions_locator.get_attribute('href', timeout=2000) if directions_locator.count() > 0 else "N/A"
                    except PlaywrightTimeoutError:
                        directions = "N/A"

                    # Structure the row
                    row = [
                        business_name, rating, reviews, category, address, status, website, directions
                    ]
                    new_data.append(row)
                    print(f"Scraped: {business_name}")

                # Check for next page and paginate
                next_button = page.locator('//button[@aria-label="Next page"]')
                if next_button.is_visible() and next_button.is_enabled():
                    print("Moving to next page...")
                    next_button.click()
                    page.wait_for_timeout(5000)
                else:
                    print("No more pages. Scraping complete.")
                    break

            # Append to CSV if it exists, otherwise create new
            file_exists = os.path.exists(output_file)
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Business Name", "Rating", "Reviews", "Category", "Address", "Opening Hours", "Website", "Directions Link"])
                writer.writerows(new_data)

            print(f"Data saved to {output_file} successfully!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            browser.close()

# Example usage
if __name__ == "__main__":
    search_query = input("Enter your search query (e.g., 'hotels in New York'): ")
    url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
    output_file = "business_data.csv"
    scrape_google_maps(url, output_file)