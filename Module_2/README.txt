1. Name:
Darren Agapay (dagapay1)

2. Module Info:
Module 2 — Web Scraping Assignment  
Due Date: 5/30/25

3. Approach:
This project implements a web scraper for TheGradCafe's graduate admissions results forum. The scraper collects up to 10,000 individual admission result entries from the paginated survey results pages. The solution consists of three Python modules:

- `scrape.py`: Handles the HTTP requests using urllib3, respects robots.txt, and fetches up to 500 pages of static HTML (each containing 20 entries). It includes a polite delay between requests and user-agent headers to avoid triggering rate limits.
- `clean.py`: Parses each page of HTML using BeautifulSoup, extracting required fields such as program, institution, status, GPA, GRE scores, degree type, and the post URL. Optional fields like term and nationality are pulled from the listing view. Additional data (e.g., GRE details, GPA, and nationality) are extracted from each individual result’s detail page via a follow-up HTTP request.
- `run.py`: Coordinates scraping and cleaning. It loops through all HTML pages fetched, cleans each, and combines the results into a final `applicant_data.json` file.

To match the assignment sample format, each entry is saved as a dictionary with keys including "program", "comments", "date_added", "url", "status", "term", "US/International", "GPA", "GRE", "GRE V", "GRE AW", and "Degree".

A fallback approach was implemented when HTML structure inconsistencies were detected (e.g., flattening all text from cells to extract the term field). The script also logs progress for easier debugging.

4. Known Bugs:
- Term was unable to be captured along with comments

If permitted to use headless browser automation tools, these fields could be reliably extracted in a future version.
