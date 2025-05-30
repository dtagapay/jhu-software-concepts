
Name: Darren Agapay, dagapay1

Module Info: Module 2 – Web Scraping Assignment, Due [Insert Due Date]

Approach:
The project uses urllib3 and urllib.robotparser to verify and make HTTP requests to thegradcafe.com. 
BeautifulSoup and regex methods are used to parse HTML and extract relevant application data. 
Extracted data includes program, university, decision, test scores, etc., and is stored in a structured 
JSON format for later use. Functions are modularized into scrape.py and clean.py as required.

Known Bugs:
None currently. In production, code should handle HTML changes and failed fetches gracefully.
