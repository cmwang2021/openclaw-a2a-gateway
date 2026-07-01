#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('/home/user/.openclaw/lcm.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for t in tables:
    print(f"- {t[0]}")
    # print schema
    cursor.execute(f"PRAGMA table_info({t[0]})")
    cols = cursor.fetchall()
    print("  Columns: " + ", ".join([c[1] for c in cols]))
conn.close()
