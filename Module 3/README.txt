# GradCafe Admissions Data Loader and Analyzer

Darren Agapay (dagapay1@jh.edu)
DueDate: 6/8/2025

This project loads self-reported graduate school admissions data from The GradCafe into a PostgreSQL database and performs basic SQL-driven analysis on GPA, GRE scores, term stats, and acceptance rates for Fall 2025 applicants.

## Features

- Parses and loads data from `applicant_data.json`
- Cleans out previous data before inserting new entries
- Skips non-numeric and placeholder scores like `"0.00"` or `""`
- Performs SQL-based analysis of:
  - Total entries for Fall 2025
  - % international students
  - Average GPA, GRE, GRE V, GRE AW
  - Avg GPA for American applicants
  - % accepted for Fall 2025
  - Avg GPA of accepted applicants
  - Total JHU CS Master's entries

## File Overview

| File            | Description |
|-----------------|-------------|
| `load_data.py`  | Connects to PostgreSQL, creates table, and loads clean JSON data |
| `query_data.py` | Runs SQL queries on the loaded data and prints labeled results |
| `applicant_data.json` | The raw scraped data (must be in same folder) |
| `requirements.txt` | Required libraries for this project |

## Setup Instructions

1. Make sure you have PostgreSQL (done through pgAdmin4) and a database created (e.g. `gradcafe_data`).
2. Create a user (e.g. `gradcafe`) and grant it full access to the database.
3. Install Python dependencies:

```bash
pip install -r requirements.txt
