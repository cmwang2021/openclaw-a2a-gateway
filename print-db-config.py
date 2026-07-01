import json

path = '/home/shrimpclan_ai/.openclaw/openclaw.json'
with open(path) as f:
    d = json.load(f)

print("Root keys:", list(d.keys()))
if 'database' in d:
    print("Database config:", d['database'])
if 'storage' in d:
    print("Storage config:", d['storage'])
if 'memory' in d:
    print("Memory config:", d['memory'])
