"""
Task 3: PostgreSQL Data Storage - Fixed for your setup
"""

import pandas as pd
import psycopg2
import os

print("="*70)
print("TASK 3: POSTGRESQL DATA STORAGE")
print("="*70)

# Database connection - UPDATE THIS PASSWORD
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': 'postgres',  # CHANGE to the password you set during initdb
}

# Bank mapping
BANK_MAPPING = {'CBE': 1, 'BOA': 2, 'Dashen': 3}

def create_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Connected to PostgreSQL database")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nCheck:")
        print("1. PostgreSQL is running: ./pg_ctl status")
        print("2. Password is correct")
        print("3. Database 'bank_reviews' exists")
        return None

def main():
    # Load data
    print("\n📂 Loading cleaned review data...")
    df = pd.read_csv('data/sentiment_theme_results.csv')
    print(f"✓ Loaded {len(df)} reviews")

    # Connect to PostgreSQL
    conn = create_connection()
    if not conn:
        return

    # Create tables
    with conn.cursor() as cur:
        # Create banks table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        
        # Create reviews table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                bank_id INTEGER REFERENCES banks(bank_id),
                review_text TEXT,
                rating INTEGER,
                review_date DATE,
                sentiment_label VARCHAR(20)
            )
        """)
        
        # Insert banks
        for bank in ['CBE', 'BOA', 'Dashen']:
            cur.execute("INSERT INTO banks (bank_name) VALUES (%s) ON CONFLICT DO NOTHING", (bank,))
        
        conn.commit()
        print("✓ Tables created")

    # Insert data
    print("\n💾 Inserting reviews...")
    inserted = 0
    
    with conn.cursor() as cur:
        for idx, row in df.iterrows():
            bank_id = BANK_MAPPING.get(row['bank'])
            cur.execute("""
                INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                bank_id,
                str(row['review'])[:500],
                int(row['rating']),
                row['date'],
                row.get('sentiment_label', 'neutral')
            ))
            inserted += 1
            
            if inserted % 200 == 0:
                print(f"   Inserted {inserted} reviews...")
        
        conn.commit()
    
    print(f"✓ Inserted {inserted} reviews")

    # Verification
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    
    result = pd.read_sql_query("""
        SELECT b.bank_name, COUNT(r.review_id) as count, AVG(r.rating) as avg_rating
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        GROUP BY b.bank_name
    """, conn)
    
    print(result.to_string(index=False))
    
    conn.close()
    print("\n✅ TASK 3 COMPLETED!")

if __name__ == "__main__":
    main()