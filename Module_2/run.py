# Import the scraping and data cleaning functions
from scrape import scrape_data         # Function to fetch HTML data from thegradcafe.com
from clean import clean_data, save_data  # Functions to clean and save parsed data

def main():
    # Step 1: Scrape HTML from up to 500 GradCafe pages
    html_pages = scrape_data(max_pages=500, delay=0.5)

    # Step 2: Clean and extract structured data
    all_data = []
    for html in html_pages:
        data = clean_data(html)
        all_data.extend(data)

    # Step 3: Save data to JSON
    save_data(all_data)
    print(f"Saved {len(all_data)} records to applicant_data.json")

# Run the script only if it's being executed directly
if __name__ == "__main__":
    main()
