# Import the scraping and data cleaning functions
from scrape import scrape_data         # Function to fetch HTML data from thegradcafe.com
from clean import clean_data, save_data  # Functions to clean and save parsed data

def main():
    # Step 1: Scrape HTML from up to 100 pages with a 1-second delay between requests
    html = scrape_data(max_pages=10, delay=.5)
    
    # Step 2: Clean and parse the raw HTML into structured JSON-like records
    print(html[:2000])  # Print the first part of the scraped HTML
    data = clean_data(html)
    
    # Step 3: Save the structured data to a file in JSON format
    save_data(data)

    # Output how many records were saved
    print(f"Saved {len(data)} records to applicant_data.json")

# Run the script only if it's being executed directly (not imported as a module)
if __name__ == "__main__":
    main()

