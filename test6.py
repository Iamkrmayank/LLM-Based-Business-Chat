from playwright.sync_api import sync_playwright
import csv

def scrape_google_maps(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        new_data = []  # Store new scraped data

        while True:
            print("Scraping Page...")

            # Business Names
            business_names = page.locator('//div[contains(@class, "qBF1Pd") and contains(@class, "fontHeadlineSmall")]').all_text_contents()

            # Ratings
            ratings = page.locator('//span[contains(@aria-label, "stars")]').all_text_contents()

            # Number of Reviews
            reviews = page.locator('//span[contains(@class, "UY7F9")]').all_text_contents()

            # Category
            categories = page.locator('//div[contains(@class, "W4Efsd")][1]').all_text_contents()

            # Address
            addresses = page.locator('//div[contains(@class, "W4Efsd")][2]').all_text_contents()

            # Opening Hours and Status
            statuses = page.locator('//div[contains(text(), "Open") or contains(text(), "Closed")]').all_text_contents()

            # Website Links
            websites = page.locator('//a[contains(text(), "Website")]/@href').all_text_contents()

            # Directions Links
            directions = page.locator('//a[contains(text(), "Directions")]/@href').all_text_contents()

            # Collect new data
            for i in range(len(business_names)):
                row = [
                    business_names[i] if i < len(business_names) else "N/A",
                    ratings[i] if i < len(ratings) else "N/A",
                    reviews[i] if i < len(reviews) else "N/A",
                    categories[i] if i < len(categories) else "N/A",
                    addresses[i] if i < len(addresses) else "N/A",
                    statuses[i] if i < len(statuses) else "N/A", 
                    websites[i] if i < len(websites) else "N/A",
                    directions[i] if i < len(directions) else "N/A"
                ]
                new_data.append(row)
                print(f"Scraped: {business_names[i]}")

            # Check for Next Page
            if page.locator('//button[@aria-label="Next page"]').is_visible():
                page.locator('//button[@aria-label="Next page"]').click()
                page.wait_for_timeout(5000)
            else:
                print("Scraping Complete")
                break

        # Write all scraped data to CSV (Overwrite Mode)
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Business Name", "Rating", "Reviews", "Category", "Address", "Opening Hours", "Website", "Directions Link"])
            writer.writerows(new_data)

        print(f"All data replaced in {output_file} successfully!")

        browser.close()

# Example usage
search_query = input("Enter your search query: ")
url = f"https://www.google.com/maps/search/{search_query}"
output_file = "business_data.csv"
scrape_google_maps(url, output_file)
