import os
import sys
import psycopg2
from psycopg2 import OperationalError

# Ensure we can import config when running from backend/ or repo root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import DB_CONFIG  # fallback when DATABASE_URL is not provided


def apply_schema():
    
    conn = None
    cursor = None

    try:
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(schema_path):
            print(f" Schema file not found at {schema_path}")
            return False

        print(f"📖 Reading schema from {schema_path}...")
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        db_url = os.getenv('DATABASE_URL')
        if db_url:
            print(" Connecting using DATABASE_URL (Render/managed Postgres)...")
            conn = psycopg2.connect(db_url)
        else:
            print(" DATABASE_URL not set. Connecting using DB_CONFIG (local fallback)...")
            # DB_CONFIG must include 'dbname'
            conn = psycopg2.connect(**DB_CONFIG)

        cursor = conn.cursor()
        print(" Applying schema to the connected database...")
        cursor.execute(schema_sql)
        conn.commit()
        print("✅ Schema applied successfully!")

        # Optional: list created tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        tables = [r[0] for r in cursor.fetchall()]
        print(f" Tables present: {tables}")
        return True

    except OperationalError as e:
        print("❌ Connection Error: Could not connect to PostgreSQL.")
        print(f"   Details: {e}")
        return False
    except psycopg2.Error as e:
        # Print server-side SQL error details
        print("❌ Database Error while applying schema:")
        print(f"   PG error: {getattr(e, 'pgerror', None)}")
        print(f"   Diag: {getattr(e, 'diag', None)}")
        print(f"   Details: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if cursor and not cursor.closed:
            cursor.close()
        if conn and not conn.closed:
            conn.close()
            print(" Database connection closed.")


if __name__ == '__main__':
    success = apply_schema()
    if success:
        print("\n Schema setup complete.")
    else:
        print("\n Schema setup failed. Check logs above.")
