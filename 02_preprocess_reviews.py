"""
Script 2: Preprocess scraped reviews.
- Remove duplicates
- Handle missing values
- Normalize dates
- Clean text
"""

import pandas as pd
import re
import os

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # keep only letters and spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load
raw = pd.read_csv('../outputs/raw_reviews.csv')
print(f"Raw shape: {raw.shape} - 02_preprocess_reviews.py:23")

# Drop duplicates
raw = raw.drop_duplicates(subset=['review_id'])
print(f"After dedup: {raw.shape} - 02_preprocess_reviews.py:27")

# Drop missing review_text or rating
before = len(raw)
raw = raw.dropna(subset=['review_text', 'rating'])
print(f"Dropped {before  len(raw)} rows with missing text/rating - 02_preprocess_reviews.py:32")

# Clean text
raw['clean_text'] = raw['review_text'].apply(clean_text)

# Ensure date format
raw['review_date'] = pd.to_datetime(raw['review_date']).dt.strftime('%Y-%m-%d')

# Keep required columns
clean_df = raw[['review_id', 'clean_text', 'rating', 'review_date', 'bank', 'source']]
clean_df = clean_df.rename(columns={'clean_text': 'review'})

clean_df.to_csv('../outputs/cleaned_reviews.csv', index=False)
print(f"Saved {len(clean_df)} cleaned reviews - 02_preprocess_reviews.py:45")
print(f"Missing data: {100  (len(clean_df)/len(raw)*100):.2f}% - 02_preprocess_reviews.py:46")