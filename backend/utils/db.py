import psycopg2
import os
from config import DB_CONFIG # <-- Import the local config

def get_db_connection():
    
    conn = None
    try:
        # Priority 1: Use DATABASE_URL from environment (for Render, Heroku, etc.)
        db_url = os.environ.get('DATABASE_URL')

        if db_url:
            print("▶️ Connecting via DATABASE_URL...")
            conn = psycopg2.connect(db_url)
        else:
            # Priority 2: Fallback to DB_CONFIG from config.py (for local development)
            print("▶️ DATABASE_URL not found. Connecting via local DB_CONFIG...")
            conn = psycopg2.connect(**DB_CONFIG)
        
        print("✅ Database connection successful!")
        return conn

    except psycopg2.OperationalError as err:
        print(f"❌ Database connection error: {err}")
        return None
    except Exception as err:
        print(f"❌ An unexpected error occurred: {err}")
        return None