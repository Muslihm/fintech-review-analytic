
"""
Script 1: Scrape Google Play reviews for CBE, BOA, and Dashen banks
Target: Minimum 400 reviews per bank
"""

from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime
import time
import os
import sys

# Bank configurations
BANKS = {
    'CBE': 'com.cbe.mobile',
    'BOA': 'com.bankofabyssinia.mobile',
    'Dashen': 'com.dashen.mobile'
}

def scrape_bank_reviews(bank_name, package_name, target_count=400):
    """Scrape reviews for a single bank."""
    all_reviews = []
    
    print(f"\n📱 Scraping {bank_name} (Package: {package_name})... - 01_scrape_reviews.py:25")
    
    try:
        result, continuation_token = reviews(
            package_name,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=target_count
        )
        
        for review in result:
            all_reviews.append({
                'review_id': review['reviewId'],
                'review_text': review['content'],
                'rating': review['score'],
                'review_date': datetime.fromtimestamp(review['at']).strftime('%Y-%m-%d'),
                'bank': bank_name,
                'source': 'Google Play'
            })
            
        print(f"✅ Collected {len(all_reviews)} reviews for {bank_name} - 01_scrape_reviews.py:46")
        
    except Exception as e:
        print(f"⚠️ Error scraping {bank_name}: {e} - 01_scrape_reviews.py:49")
        
    return pd.DataFrame(all_reviews)

def main():
    """Main scraping function."""
    print("= - 01_scrape_reviews.py:55" * 60)
    print("TASK 1: Data Collection from Google Play Store - 01_scrape_reviews.py:56")
    print("= - 01_scrape_reviews.py:57" * 60)
    
    all_data = []
    
    for bank_name, package in BANKS.items():
        df = scrape_bank_reviews(bank_name, package, target_count=400)
        all_data.append(df)
        time.sleep(2)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Go back to project root for data directory
        os.makedirs('../data/raw', exist_ok=True)
        
        output_path = '../data/raw/raw_reviews.csv'
        combined_df.to_csv(output_path, index=False)
        
        print(f"\n📊 SUMMARY: - 01_scrape_reviews.py:75")
        print(f"Total reviews collected: {len(combined_df)} - 01_scrape_reviews.py:76")
        print(f"Per bank: - 01_scrape_reviews.py:77")
        for bank in BANKS.keys():
            count = len(combined_df[combined_df['bank'] == bank])
            print(f"{bank}: {count} reviews - 01_scrape_reviews.py:80")
    else:
        print("\n❌ No data collected. - 01_scrape_reviews.py:82")
    
    return combined_df if all_data else pd.DataFrame()

if __name__ == "__main__":
    main()