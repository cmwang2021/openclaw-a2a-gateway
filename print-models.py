import json

path = '/home/shrimpclan_ai/.openclaw/openclaw.json'
with open(path) as f:
    d = json.load(f)

if 'models' in d:
    print("=== MODELS ===")
    print(json.dumps(d['models'], indent=2))

if 'agents' in d:
    print("\n=== AGENTS ===")
    print(json.dumps(d['agents'], indent=2))
