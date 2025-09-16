from playwright.sync_api import sync_playwright
import csv

def run():
    with sync_playwright() as p:
        # ✅ Use your installed Chrome browser
        # Change this path if Chrome is installed somewhere else
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        browser = p.chromium.launch(
            headless=False,  # show the browser so you can see it
            executable_path=chrome_path
        )

        page = browser.new_page()
        page.goto("https://www.w3schools.com/html/html_tables.asp")

        print("[DEBUG] Page loaded:", page.title())

        # ✅ Scrape the table rows
        rows = page.query_selector_all("#customers tr")

        data = []
        for row in rows:
            cells = row.query_selector_all("td")
            if cells:  # skip header
                data.append([cell.inner_text().strip() for cell in cells])

        # ✅ Save to CSV in your project folder
        output_file = "scraped_table.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Company", "Contact", "Country"])  # header
            writer.writerows(data)

        print(f"[DEBUG] Data saved to {output_file}")

        browser.close()

if __name__ == "__main__":
    run()
