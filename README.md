# Fintech Review Analytics - Ethiopian Banks

## Project Overview
Analysis of Google Play reviews for Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

## Task 1: Data Collection & Preprocessing

### Scraping Methodology
- **Library**: google-play-scraper v1.2.7
- **Date Range**: Last 450 reviews per bank (approx. 6 months)
- **Target**: 400+ reviews per bank (1,200+ total)

### Limitations Documented
- BOA initially returned 380 reviews → expanded target to 450 to ensure 400+
- Rate limits respected with 2-second delays between requests

### Files Created
- `scripts/01_scrape_reviews.py` - Web scraping script
- `scripts/02_preprocess_reviews.py` - Cleaning pipeline
- `data/raw/raw_reviews.csv` - Raw scraped data (gitignored)
- `data/raw/cleaned_reviews.csv` - Cleaned dataset (gitignored)

### Cleaning Steps
1. Remove duplicate review_ids
2. Drop rows with missing review_text or rating
3. Clean text: lowercase, remove URLs/special chars
4. Normalize dates to YYYY-MM-DD
5. Keep columns: review, rating, date, bank, source

### Output Schema
| Column | Type | Description |
|--------|------|-------------|
| review | string | Cleaned review text |
| rating | integer | 1-5 star rating |
| date | date | YYYY-MM-DD format |
| bank | string | CBE, BOA, or Dashen |
| source | string | "Google Play" |

## Setup Instructions
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/fintech-review-analytics.git
cd fintech-review-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Task 1
cd scripts
python 01_scrape_reviews.py
python 02_preprocess_reviews.py
CI/CD

GitHub Actions runs pytest on every push to main branch.
