import json

path = '/home/shrimpclan_ai/.openclaw/openclaw.json'
with open(path) as f:
    d = json.load(f)

for agent in d.get('agents', {}).get('list', []):
    if agent.get('id') == 'main':
        print("=== Agent 'main' Configuration ===")
        print(json.dumps(agent, indent=2))
