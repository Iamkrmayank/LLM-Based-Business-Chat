from playwright.sync_api import sync_playwright
import csv
from time import sleep

def scrape_google_maps(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()
        
        try:
            print(f"Navigating to {url}...")
            page.goto(url)
            page.wait_for_timeout(5000)  # Wait for page to load
            
            new_data = []  # Store scraped data

            while True:
                print("Scraping current page...")

                # Scroll to load all listings (Google Maps often lazy-loads content)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                sleep(2)  # Give time for lazy-loaded content

                # Locate all business listing containers
                listings = page.locator('//div[contains(@class, "Nv2PK")]').all()

                for listing in listings:
                    # Extract each field's text content or default to "N/A"
                    business_name = listing.locator('.qBF1Pd.fontHeadlineSmall').text_content() or "N/A"
                    rating = listing.locator('span[aria-label*="stars"]').text_content() or "N/A"
                    reviews = listing.locator('.UY7F9').text_content().strip('()') or "N/A"
                    category = listing.locator('.W4Efsd >> nth=0').text_content() or "N/A"
                    address = listing.locator('.W4Efsd >> nth=1').text_content() or "N/A"
                    status = listing.locator('div:text-matches("Open|Closed")').text_content() or "N/A"
                    website = listing.locator('a:text("Website")').get_attribute('href') or "N/A"
                    directions = listing.locator('a:text("Directions")').get_attribute('href') or "N/A"

                    # Structure the row
                    row = [
                        business_name.strip(),
                        rating.strip(),
                        reviews.strip(),
                        category.strip(),
                        address.strip(),
                        status.strip(),
                        website.strip(),
                        directions.strip()
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

            # Write structured data to CSV
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
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