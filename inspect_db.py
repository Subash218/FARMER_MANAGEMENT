
import sqlite3
import os

DB_FILE = 'farmportal.db'

if not os.path.exists(DB_FILE):
    print(f"Database file {DB_FILE} not found.")
    exit()

try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"Tables found: {[t[0] for t in tables]}")
    print("-" * 20)

    for table_name in tables:
        table = table_name[0]
        print(f"Schema for table '{table}':")
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
        schema = cursor.fetchone()[0]
        print(schema)
        print("-" * 20)
        
        print(f"Data in table '{table}':")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [info[1] for info in cursor.fetchall()]
        print(f"Columns: {columns}")
        
        if not rows:
            print("(No rows found)")
        else:
            for row in rows:
                print(row)
        print("=" * 40)

    conn.close()

except Exception as e:
    print(f"Error: {e}")
