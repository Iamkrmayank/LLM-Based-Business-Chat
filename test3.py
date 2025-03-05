from playwright.sync_api import sync_playwright
import csv

# Function to scrape business details
def scrape_google_maps(url, output_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True for headless
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)  # Allow time for content to load
        
        # Open CSV File for Writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Business Name", "Rating", "Opening Hours", "Location", "Contact Info", "Description"])
            
            # Pagination Loop
            while True:
                print("Scraping Page...")
                
                # Extract Business Name
                business_names = page.locator('//div[contains(@class, "qBF1Pd") and contains(@class, "fontHeadlineSmall")]').all_text_contents()
                
                # Extract Ratings
                ratings = page.locator('//span[contains(@aria-label, "stars")]').all_text_contents()
                
                # Extract Location
                locations = page.locator('//div[contains(@class, "W4Efsd")]').all_text_contents()
                
                # Extract Opening Hours (If Available)
                opening_hours = page.locator('//div[contains(@class, "W4Efsd") and contains(text(), "Open") or contains(text(), "Closed")]').all_text_contents()
                
                # Extract Contact Info (If Available)
                contact_info = page.locator('//span[contains(@class, "UsdlK") or contains(@class, "UsdlK ph1")]/text()').all_text_contents()
                
                # Extract Description
                descriptions = page.locator('//div[contains(@class, "W4Efsd") and not(contains(text(), "Open"))]').all_text_contents()
                
                # Writing Data to CSV File
                for i in range(len(business_names)):
                    writer.writerow([
                        business_names[i] if i < len(business_names) else "N/A",
                        ratings[i] if i < len(ratings) else "N/A",
                        opening_hours[i] if i < len(opening_hours) else "N/A",
                        locations[i] if i < len(locations) else "N/A",
                        contact_info[i] if i < len(contact_info) else "N/A",
                        descriptions[i] if i < len(descriptions) else "N/A"
                    ])
                    print(f"Scraped: {business_names[i]}")
                
                # Next Page Handling
                if page.locator('//button[@aria-label="Next page"]').is_visible():
                    page.locator('//button[@aria-label="Next page"]').click()
                    page.wait_for_timeout(4000)  # Wait for Next Page to Load
                else:
                    print("Scraping Complete")
                    break
        
        browser.close()

# URL Example
url = "https://www.google.com/maps/search/Restaurants+near+me"
output_file = "business_details.csv"
scrape_google_maps(url, output_file)
