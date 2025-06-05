import json
from bs4 import BeautifulSoup
import re
import urllib3

http = urllib3.PoolManager()

# Helper function to get extra info like GPA, GRE, etc. from individual result page
def _fetch_optional_fields(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "GPA": "",
        "GRE": "",
        "GRE V": "",
        "GRE AW": "",
        "US/International": "",
        "comments": ""
    }
    try:
        response = http.request('GET', url, headers=headers)
        if response.status != 200:
            return data

        soup = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

        # Extract comment from <dt>Notes</dt> → <dd>Comment</dd>
        try:
            for dt in soup.find_all("dt"):
                if dt.get_text(strip=True).lower() == "notes":
                    dd = dt.find_next_sibling("dd")
                    if dd:
                        comment_text = dd.get_text(separator="\n", strip=True)
                        if comment_text and "Details and information" not in comment_text:
                            data["comments"] = comment_text
                            break
        except Exception as e:
            print(f"Notes extraction failed: {e}")

        # ✅ Extract GPA, GRE, AW, Nationality
        divs = soup.find_all('div')
        for div in divs:
            text = div.get_text(strip=True)

            # GPA
            if "GPA" in text and not data["GPA"]:
                match = re.search(r"(\d\.\d{1,2})", text)
                if match:
                    data["GPA"] = match.group(1)

            # GRE General
            if "GRE General" in text and not data["GRE"]:
                match = re.search(r"GRE General[:\s]+(\d{2,3})", text)
                if match:
                    data["GRE"] = match.group(1)

            # GRE Verbal
            if "GRE Verbal" in text and not data["GRE V"]:
                match = re.search(r"GRE Verbal[:\s]+(\d{2,3})", text)
                if match:
                    data["GRE V"] = match.group(1)

            # Analytical Writing
            if "Analytical Writing" in text and not data["GRE AW"]:
                match = re.search(r"Analytical Writing[:\s]+(\d\.\d{1,2})", text)
                if match:
                    data["GRE AW"] = match.group(1)

            # Nationality
            if "Degree's Country of Origin" in text and not data["US/International"]:
                if "International" in text:
                    data["US/International"] = "International"
                elif "American" in text or "US Citizen" in text:
                    data["US/International"] = "American"

        return data
    except Exception as e:
        print(f"fetch_optional_fields error: {e}")
        return data

# Main function to parse each HTML page into structured applicant data
def clean_data(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    applicants = []

    table = soup.find('table')
    entries = table.find_all(['tr']) if table else []
    for entry in entries:
        # print(entry)
        cells = entry.find_all('td')
        if len(cells) < 5:
            for cell in entry.find_all("div"):
                term = ""
                text = cell.get_text(strip=True)
                if re.match(r"^(Fall|Spring|Summer|Winter)\s+\d{4}$", text):
                    term = text
                    break
            continue

        # Extract university and program name
        university = cells[0].get_text(strip=True)
        program_line = cells[1].get_text(strip=True)

        degree = None
        program_name = program_line
        if "PhD" in program_line:
            degree = "PhD"
            program_name = program_line.replace("PhD", "")
        elif "Masters" in program_line:
            degree = "Masters"
            program_name = program_line.replace("Masters", "")
        elif "Other" in program_line:
            degree = "Other"
            program_name = program_line.replace("Other", "")

        program_name = program_name.strip()
        program_full = f"{program_name}, {university}"

        # Other fields
        post_date = cells[2].get_text(strip=True)
        status = cells[3].get_text(strip=True)

        # Construct result URL
        url = ""
        span_with_id = entry.find('span', attrs={'data-id': True})
        if span_with_id and span_with_id.has_attr('data-id'):
            result_id = span_with_id['data-id']
            url = f"https://www.thegradcafe.com/result/{result_id}"

        # Build the main record
        applicant = {
            "program": program_full,
            "comments": "",
            "date_added": post_date,
            "url": url,
            "status": status,
            "term": term,
            "US/International": "",
            "GPA": "",
            "GRE": "",
            "GRE V": "",
            "GRE AW": "",
            "Degree": degree
        }

        # Fetch extra fields if we have a URL
        if url:
            optional = _fetch_optional_fields(url)
            applicant.update(optional)

        applicants.append(applicant)

    return applicants

# Save final list of applicants to a JSON file
def save_data(data, filename="applicant_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
