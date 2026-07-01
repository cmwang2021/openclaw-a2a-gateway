import json

path = '/home/shrimpclan_ai/.openclaw/openclaw.json'
with open(path) as f:
    d = json.load(f)

print("=== ALL PROVIDERS ===")
providers = d.get('models', {}).get('providers', {})
for k, v in providers.items():
    print(f"\nProvider: {k}")
    # Mask apiKey or other credentials
    masked = {}
    for pk, pv in v.items():
        if 'key' in pk.lower() or 'secret' in pk.lower() or 'token' in pk.lower():
            masked[pk] = str(pv)[:10] + "..." if isinstance(pv, str) else pv
        else:
            masked[pk] = pv
    print(json.dumps(masked, indent=2))
