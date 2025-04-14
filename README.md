# Lead Generation Scraper – BHCOE ABA Therapy Directory

This script scrapes clinic information from the [BHCOE ABA Therapy Directory](https://www.bhcoe.org/aba-therapy-directory/) to gather structured lead data for enrichment via platforms like [Clay](https://clay.run/).

## 🔍 What It Does

- Automatically scrolls and clicks "Load More" until at least 50 **unique** clinics are loaded.
- Visits each clinic's detail page to extract:
  - Name
  - Location (City, State)
  - Address (from embedded Google Maps link)
  - Website (clean URL from BHCOE tracking)
- Exports the data to a clean **CSV file** for enrichment and lead generation.

## 📦 Output

The resulting `clinics.csv` file contains the following columns:

| Name | Location | Address | URL |
|------|----------|---------|-----|

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone git@github.com:CarlosSalasCarpio/Lead-gen-Engineering-Take-Home.git
cd Lead-gen-Engineering-Take-Home
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

> If `requirements.txt` is missing, you can install manually:

```bash
pip install playwright pandas
playwright install
```

### 3. Run the script

```bash
python main.py
```

This will generate a file named `clinics.csv` with at least 50 deduplicated clinic records.

## 🛠️ Tech Stack

- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- `pandas` and `csv` for structured output

After the .csv file was generated using the scraper, it was uploaded to Clay. Contact information was then enriched (Full Name, Job Title, Location, Company Domain, LinkedIn Profile, Work Email), and companies were categorized by size: Small, Medium, or Large.

You can find the final Google Sheets document here:
https://docs.google.com/spreadsheets/d/1fxpAjbLxFXI10ARoq8pRmKAxn18sR6OI5JrdeRm7hlk/edit?usp=sharing