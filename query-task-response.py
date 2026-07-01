import sqlite3

db_path = '/home/shrimpclan_ai/.openclaw/lcm.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in database:", tables)

# Get recent conversations
if 'conversations' in tables:
    cursor.execute("SELECT id, summary, updated_at FROM conversations ORDER BY updated_at DESC LIMIT 5;")
    conversations = cursor.fetchall()
    print("\n=== Recent Conversations ===")
    for c in conversations:
        print(c)

# Get recent messages
if 'messages' in tables:
    cursor.execute("SELECT id, conversation_id, role, text, created_at FROM messages ORDER BY created_at DESC LIMIT 10;")
    messages = cursor.fetchall()
    print("\n=== Recent Messages ===")
    for m in messages:
        print(m)

conn.close()
