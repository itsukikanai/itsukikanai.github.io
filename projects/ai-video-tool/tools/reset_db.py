import os
import sys
import argparse

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

from app.core.database import DB_PATH, init_db

def reset_database():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print(f"Deleted existing database at {DB_PATH}")
        except PermissionError:
            print(f"Error: Could not delete {DB_PATH}. Is the application running? Please stop it first.")
            return False
        except Exception as e:
            print(f"Error deleting database: {e}")
            return False
    else:
        print("No existing database found.")

    print("Initializing new database...")
    try:
        init_db()
        print("Database reset complete.")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset the database.")
    parser.add_argument("--force", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    if not args.force:
        confirm = input("This will DELETE ALL DATA in 'data/db.sqlite3'. Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    reset_database()
