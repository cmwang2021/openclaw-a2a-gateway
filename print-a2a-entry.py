import json

with open('/home/user/.openclaw/openclaw.json') as f:
    d = json.load(f)

print(json.dumps(d.get('plugins', {}).get('entries', {}).get('a2a-gateway', {}), indent=2))
