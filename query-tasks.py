#!/usr/bin/env python3
import sqlite3
import json

conn = sqlite3.connect('/home/user/.openclaw/lcm.db')
cursor = conn.cursor()
try:
    cursor.execute("SELECT id, status, createdAt, result FROM tasks ORDER BY createdAt DESC LIMIT 5")
    rows = cursor.fetchall()
    print(f"{'ID':<40} | {'Status':<12} | {'CreatedAt':<25}")
    print("-" * 85)
    for r in rows:
        print(f"{r[0]:<40} | {r[1]:<12} | {r[2]:<25}")
        if r[3]:
            try:
                res = json.loads(r[3])
                msg = res.get('message', {}).get('parts', [{}])[0].get('text', '')
                print(f"  Result: {msg[:100]}")
            except Exception:
                pass
except Exception as e:
    print(f"Error: {e}")
conn.close()
