import sqlite3

conn = sqlite3.connect('/home/user/.openclaw/lcm.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in lcm.db:", tables)

# Search for 100.88 in all tables
for table in tables:
    try:
        cursor.execute(f"PRAGMA table_info({table});")
        cols = [row[1] for row in cursor.fetchall()]
        for col in cols:
            cursor.execute(f"SELECT * FROM {table} WHERE CAST({col} AS TEXT) LIKE '%100.88%';")
            rows = cursor.fetchall()
            if rows:
                print(f"Found in table {table}, column {col}:")
                for r in rows:
                    print(r)
    except Exception as e:
        print(f"Error checking table {table}: {e}")

conn.close()
