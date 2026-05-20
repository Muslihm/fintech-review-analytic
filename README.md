## Task 3: PostgreSQL Database Integration

### Database Setup

1. **Install PostgreSQL** (Windows):
   - Download from: https://www.postgresql.org/download/windows/
   - During installation, remember your password
   - Default port: 5432

2. **Create Database**:
   ```sql
   CREATE DATABASE bank_reviews;
3. Install Python Package:
    bash

    pip install psycopg2-binary

4. Update Configuration:

        Open scripts/insert_to_postgresql.py

        Change password to your PostgreSQL password

5. Run the Script:
    bash

    python scripts/insert_to_postgresql.py

Schema Design

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

    source (VARCHAR(50)
## Step 76: Run the Complete Task 3

```bash
# Step 1: First, create the database manually in pgAdmin or psql
# CREATE DATABASE bank_reviews;

# Step 2: Update the password in insert_to_postgresql.py
# Change: 'password': 'your_password_here' to your actual password

# Step 3: Run the insertion script
python scripts/insert_to_postgresql.py