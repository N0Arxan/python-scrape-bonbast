#!/usr/bin/env python3
"""
Scraper using Playwright to get dynamic data from bonbast.com.
"""

from playwright.sync_api import sync_playwright
import sys
from bs4 import BeautifulSoup # Used to prettify the final HTML

URL = "https://www.bonbast.com/"

def fetch_dynamic_data(debug_id: str = "eur1"):
    """
    Fetches the page with a real browser, waits for JS to load,
    and extracts the data.
    """
    with sync_playwright() as p:
        print(f"Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print(f"Navigating to {URL}...")
            page.goto(URL, timeout=60000)
            
            print("Page loaded. Waiting for dynamic content...")
   
            eur1_selector = "#eur1"
            eur2_selector = "#eur2"
            usd1_selector = "#usd1"
            usd2_selector = "#usd2"
            
            page.wait_for_selector(eur1_selector, state="visible", timeout=30000)
            page.wait_for_selector(eur2_selector, state="visible", timeout=30000)
            page.wait_for_selector(usd1_selector, state="visible", timeout=30000)
            page.wait_for_selector(usd2_selector, state="visible", timeout=30000)
            
            print("Dynamic content found. Extracting data...")
            
            eur1_text = page.locator(eur1_selector).text_content()
            eur2_text = page.locator(eur2_selector).text_content()
            usd1_text = page.locator(usd1_selector).text_content()
            usd2_text = page.locator(usd2_selector).text_content()
            
            # --- Get the parent table for debugging ---
            # We find the element by the debug_id, then ask for its ancestor <table>
            debug_element = page.locator(f"id={debug_id}")
            parent_table = debug_element.locator("xpath=./ancestor::table[1]")
            table_html = parent_table.inner_html()

            browser.close()
            
            return {
                "eur1": eur1_text.strip() if eur1_text else None,
                "eur2": eur2_text.strip() if eur2_text else None,
                "usd1": usd1_text.strip() if usd1_text else None,
                "usd2": usd2_text.strip() if usd2_text else None,
                "table_html_for_debug": table_html
            }
        
        except Exception as e:
            print(f"\n--- An Error Occurred ---", file=sys.stderr)
            print(f"{e}", file=sys.stderr)
            print("This could be a timeout. The site might be slow or blocking.", file=sys.stderr)
            browser.close()
            return None

def main():
    data = fetch_dynamic_data(debug_id="eur1")
    
    if data:
        
        print("\n --- Extracted Data --- \n")
        print(f"EUR€ Sell: {format_with_commas(data['eur1'])} Toman")
        print(f"EUR€ Buy: {format_with_commas(data['eur2'])} Toman")
        
        print(f"USD$ Sell: {format_with_commas(data['usd1'])} Toman")
        print(f"USD$ Buy: {format_with_commas(data['usd2'])} Toman")
        
        # print(f"\n📄 --- Debug Parent Table for 'eur1' --- 📄")
        # if data['table_html_for_debug']:
        #     soup = BeautifulSoup(data['table_html_for_debug'], "html.parser")
        #     print(soup.prettify())
        # else:
        #     print("Could not extract table HTML.")
    else:
        print("Failed to fetch data.", file=sys.stderr)



def format_with_commas(num_str: str | None) -> str | None:
    """
    Converts a number string (e.g., "58000") 
    to a comma-formatted string (e.g., "58,000").
    
    If input is not a valid number, it returns the original string.
    """
    if not num_str:
        return None
    
    try:
        number = int(num_str)
        return f"{number:,}"
    except ValueError:
        return num_str
if __name__ == "__main__":
    main()