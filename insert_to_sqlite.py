"""
Task 3: Store Cleaned Data in SQLite
"""

import sqlite3
import pandas as pd
import os

print("="*60)
print("TASK 3: SQLITE DATABASE CREATION")
print("="*60)

# Check if data exists
if not os.path.exists('data/sentiment_theme_results.csv'):
    print("❌ sentiment_theme_results.csv not found!")
    print("Please run Task 2 first: python scripts/sentiment_textblob.py")
    exit()

# Load data
print("\n📂 Loading cleaned review data...")
df = pd.read_csv('data/sentiment_theme_results.csv')
print(f"✓ Loaded {len(df)} reviews")

# Create database
print("\n💾 Creating SQLite database...")
conn = sqlite3.connect('data/bank_reviews.db')
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_text TEXT,
        rating INTEGER,
        review_date TEXT,
        bank TEXT,
        sentiment_label TEXT,
        sentiment_score REAL,
        identified_theme TEXT
    )
""")

# Insert data
print("\n📝 Inserting reviews...")
for idx, row in df.iterrows():
    cursor.execute("""
        INSERT INTO reviews (review_text, rating, review_date, bank, sentiment_label, sentiment_score, identified_theme)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(row['review'])[:500],
        int(row['rating']),
        row['date'],
        row['bank'],
        row.get('sentiment_label', 'neutral'),
        float(row.get('sentiment_score', 0.5)) if pd.notna(row.get('sentiment_score')) else 0.5,
        row.get('identified_theme', 'Other')
    ))

conn.commit()
print(f"✓ Inserted {len(df)} reviews")

# Verification
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

result = pd.read_sql_query("""
    SELECT bank, COUNT(*) as review_count, 
           ROUND(AVG(rating), 2) as avg_rating,
           SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_count
    FROM reviews
    GROUP BY bank
""", conn)

print("\n📊 Reviews per bank:")
print(result.to_string(index=False))

conn.close()
print("\n✅ Database saved to: data/bank_reviews.db")
print("="*60)