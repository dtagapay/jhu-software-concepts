import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.thegradcafe.com/survey/?page=1"
page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(page.content, "html.parser")

# Find all result rows
rows = soup.find_all("tr", class_="tw-border-none")

for i, row in enumerate(rows):
    # Get all divs in the row
    divs = row.find_all("div")

    # Try to find the one with a term like "Fall 2025"
    term = ""
    for div in divs:
        text = div.get_text(strip=True)
        if re.match(r"^(Fall|Spring|Summer|Winter)\s+\d{4}$", text):
            term = text
            break

    if term:
        print(f"Row {i}: TERM = {term}")
