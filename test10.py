import csv
import time
from playwright.sync_api import sync_playwright

def scrape_google_maps(url):
    """Scrapes business details from a given Google Maps URL."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=15000)
            page.wait_for_timeout(5000)
            
            business_name = page.locator('//div[contains(@class, "qBF1Pd") and contains(@class, "fontHeadlineSmall")]').first.text_content() or "N/A"
            opening_hours = page.locator('//div[contains(@class, "W4Efsd") and contains(text(), "Open") or contains(text(), "Closed")]').first.text_content() or "N/A"
            location = page.locator('//div[contains(@class, "W4Efsd")]').nth(1).text_content() or "N/A"
            contact_info = page.locator('//span[contains(@class, "UsdlK") or contains(@class, "UsdlK ph1")]').first.text_content() or "N/A"
            description = page.locator('//div[contains(@class, "W4Efsd") and not(contains(text(), "Open"))]').first.text_content() or "N/A"
            address = page.locator('//div[contains(@class, "Io6YTe")]').first.text_content() or "N/A"
            
            browser.close()
            return [business_name, opening_hours, location, contact_info, description, address]
        except Exception as e:
            browser.close()
            return None  # Return None if scraping fails

def process_csv(input_csv, output_csv, error_csv):
    """Reads input CSV, scrapes each URL, appends results, and logs errors."""
    with open(input_csv, mode='r', encoding='utf-8') as infile,
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile,
         open(error_csv, mode='w', newline='', encoding='utf-8') as errfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        err_writer = csv.writer(errfile)
        
        headers = next(reader)
        headers.extend(["Business Name", "Opening Hours", "Location", "Contact Info", "Description", "Address"])
        writer.writerow(headers)
        err_writer.writerow(["Failed URL"])
        
        for row in reader:
            url = row[0]  # Assuming URL is in the first column
            print(f"Processing: {url}")
            data = scrape_google_maps(url)
            
            if data:
                writer.writerow(row + data)
            else:
                err_writer.writerow([url])
            time.sleep(2)  # Avoid rapid requests

# Example usage
process_csv("input_urls.csv", "scraped_data.csv", "failed_urls.csv")
