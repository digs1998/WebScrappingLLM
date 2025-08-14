# WebScrappingLLM

A modular Python project for web scraping LinkedIn job postings and processing them with LLM-based insights. Built with async scraping, Streamlit dashboard, and structured for maintainability and scalability.

## Repo Structure
WebScrappingLLM/
│
├─ scrapeLinkedIn/              # Scraper module
│   ├─ __init__.py
│   ├─ scraper.py # main async linkedin scraper
|   ├─ routes.py  # asynchronously fetch job postings and their details
|   ├─ gptDomainExtractor.py # using GPT 4 to extract domain insights
│
├─ app.py                       # Streamlit dashboard / main entry point
├─ requirements.txt             # Python dependencies
└─ README.md

## Details:

scrapeLinkedIn/: Contains the LinkedIn scraping logic using Playwright/Crawlee. scraper.py defines scrapeLinkedin(role, location, data_name) which returns a DataFrame.

app.py: Streamlit app for user input (role, location), running the scraper in a safe process, and displaying results along with metrics and charts.

requirements.txt: Python packages required (e.g., streamlit, pandas, playwright, crawlee, nest_asyncio).

## Installation

Clone the repository:

``
git clone https://github.com/digs1998/WebScrappingLLM.git
cd WebScrappingLLM
``

Create a virtual environment (optional but recommended):

``
conda activate env_name
``

Install dependencies:

``
pip install -r requirements.txt
``

Install Playwright browsers:

``
playwright install
``

Usage
Run the Streamlit Dashboard

``
streamlit run app.py
``

Enter Job Role and Location.

Click Run Scraper.

The app will scrape LinkedIn asynchronously and display:

Job postings in a DataFrame

Top Companies and Locations charts

Summary metrics (Total Jobs, Unique Companies, Unique Locations)