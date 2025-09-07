import os
import sys
import psycopg2
from psycopg2 import OperationalError

# --- Correctly locate the project's root directory ---
# This ensures that we can import the 'config' module regardless of where the script is run from.
# It goes up one level from /database to the /backend directory.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now the import will work correctly
from config import DB_CONFIG

def setup_database():
    """Setup PostgreSQL database and tables"""
    db_params = DB_CONFIG.copy()
    db_name = db_params.pop('dbname')
    
    conn = None
    cursor = None

    try:
        # --- Step 1: Connect to the default 'postgres' database to create our new DB ---
        print(f"📡 Connecting to PostgreSQL server at {db_params.get('host')}...")
        conn = psycopg2.connect(**db_params, dbname='postgres')
        conn.autocommit = True
        cursor = conn.cursor()

        print(f"Checking for database '{db_name}'...")
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()

        # --- Step 2: Connect to the new database to set up tables ---
        print(f"\nConnecting to database '{db_name}' to set up schema...")
        conn = psycopg2.connect(**db_params, dbname=db_name)
        cursor = conn.cursor()

        # Correctly locate schema.sql relative to this script's location
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        print(f"📖 Reading schema from {schema_path}...")
        
        if not os.path.exists(schema_path):
            print(f"❌ Schema file not found at {schema_path}")
            return False
            
        with open(schema_path, 'r') as file:
            schema_sql = file.read()
        
        print("🚀 Creating tables...")
        cursor.execute(schema_sql)
        conn.commit()
        print("✅ Schema and tables created successfully!")
        
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        print(f"✨ Created tables: {[table[0] for table in tables]}")
        
        return True
        
    except OperationalError as e:
        print(f"❌ Connection Error: Could not connect to PostgreSQL. Is the server running?")
        print(f"   Details: {e}")
        return False
    except psycopg2.Error as e:
        print(f"❌ Database Error: {e}")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False
    finally:
        if conn and not conn.closed:
            if cursor and not cursor.closed:
                cursor.close()
            conn.close()
            print("\n🔌 Database connection closed.")

if __name__ == "__main__":
    success = setup_database()
    if success:
        print("\n🎉 You can now start the Flask application!")
    else:
        print("\n🔴 Database setup failed. Please check the errors above.")