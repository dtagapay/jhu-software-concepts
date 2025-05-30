
import urllib3
from urllib.robotparser import RobotFileParser
import time

def scrape_data(max_pages=100, delay=1):
    '''
    Scrape paginated data from TheGradCafe's survey results page.
    Args:
        max_pages: Maximum number of pages to scrape (default 100).
        delay: Delay between requests in seconds to avoid rate limiting (default 1s).
    Returns:
        Combined HTML content from all pages.
    '''
    base_url = "https://www.thegradcafe.com/survey/?page={}"
    robots_url = "https://www.thegradcafe.com/robots.txt"

    # Load and parse the robots.txt file
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    # Check permission to scrape one of the paginated URLs
    test_url = base_url.format(1)
    if not rp.can_fetch("*", test_url):
        raise PermissionError("Scraping disallowed by robots.txt")

    http = urllib3.PoolManager()
    all_html = ""

    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        response = http.request('GET', url)

        if response.status != 200:
            print(f"Page {page} fetch failed, stopping...")
            break

        html = response.data.decode('utf-8')
        all_html += html

        print(f"Fetched page {page}")
        time.sleep(delay)

    return all_html
