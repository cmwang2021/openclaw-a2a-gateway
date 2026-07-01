import json

path = '/root/.9router/db.json'
with open(path) as f:
    d = json.load(f)

conn = d.get('providerConnections', [])
print("=== Codex Connections ===")
for idx, c in enumerate(conn):
    if c.get('provider') == 'codex':
        print(f"\nIndex: {idx}")
        print(f"ID: {c.get('id')}")
        print(f"Name: {c.get('name')}")
        print(f"Email: {c.get('email')}")
        print(f"IsActive: {c.get('isActive')}")
        print(f"Priority: {c.get('priority')}")
        print(f"Test Status: {c.get('testStatus')}")
        print(f"Last Error: {c.get('lastError')}")
        print(f"Last Error At: {c.get('lastErrorAt')}")
        print(f"Expires At: {c.get('expiresAt')}")
