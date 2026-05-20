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
## Task 3: PostgreSQL Database Integration

### Database Setup

1. **Install PostgreSQL** (Windows):
   - Download from: https://www.postgresql.org/download/windows/
   - During installation, remember your password
   - Default port: 5432

2. **Create Database**:
   ```sql
   CREATE DATABASE bank_reviews;
3.Install Python Package:

 pip install psycopg2-binary

4.Update Configuration:

        Open scripts/insert_to_postgresql.py

        Change password to your PostgreSQL password

5. Run the Script:
    
    python scripts/insert_to_postgresql.py

6. Schema Design

Banks Table:

    bank_id (SERIAL PRIMARY KEY)

    bank_name (VARCHAR(50) UNIQUE)

    app_name (VARCHAR(100))

    app_id (VARCHAR(100))

Reviews Table:

    review_id (SERIAL PRIMARY KEY)

    original_review_id (VARCHAR(100) UNIQUE)

    bank_id (FOREIGN KEY)

    review_text (TEXT)

    cleaned_review (TEXT)

    rating (INTEGER, 1-5)

    review_date (DATE)

    sentiment_label (VARCHAR(20))

    sentiment_score (DECIMAL)

    identified_theme (VARCHAR(50))

    source (VARCHAR(50))
## Step 7: Run the Complete Task 3

# Step 1: First, create the database manually in pgAdmin or psql
# CREATE DATABASE bank_reviews;

# Step 2: Update the password in insert_to_postgresql.py
# Change: 'password': 'your_password_here' to your actual password

# Step 3: Run the insertion script
python scripts/insert_to_postgresql.py
