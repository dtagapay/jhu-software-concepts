import urllib3
import time
from urllib.robotparser import RobotFileParser

def scrape_data(max_pages=100, delay=1):
    """
    Scrape multiple pages of TheGradCafe survey results.

    Args:
        max_pages (int): Number of pages to scrape.
        delay (int): Delay in seconds between requests to avoid throttling.

    Returns:
        List[str]: A list of raw HTML strings, one for each page.
    """
    base_url = "https://www.thegradcafe.com/survey/?page={}"
    robots_url = "https://www.thegradcafe.com/robots.txt"

    # Parse robots.txt to check if scraping is allowed
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    # Test one URL to verify permission
    test_url = base_url.format(1)
    if not rp.can_fetch("*", test_url):
        raise PermissionError("Scraping disallowed by robots.txt")

    http = urllib3.PoolManager()
    headers = {"User-Agent": "Mozilla/5.0"}
    all_html_pages = []

    # Loop over each page and fetch its HTML
    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        print(f"Fetching page {page}...")

        try:
            response = http.request('GET', url, headers=headers)
            if response.status != 200:
                print(f"Page {page} fetch failed with status {response.status}, stopping.")
                break

            # Decode response content and add to list
            html = response.data.decode('utf-8')
            all_html_pages.append(html)

            # Special logging for debugging at page 500
            if page == 500:
                print("Successfully fetched page 500 — scraper is still running...")

        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

        time.sleep(delay)

    return all_html_pages