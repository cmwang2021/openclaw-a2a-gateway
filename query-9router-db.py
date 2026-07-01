import json

path = '/root/.9router/db.json'
with open(path) as f:
    d = json.load(f)

# List structure of providerConnections
conn = d.get('providerConnections', [])
print("providerConnections type:", type(conn))
if isinstance(conn, list):
    print("providerConnections length:", len(conn))
    if conn:
        print("First connection keys:", list(conn[0].keys()))
        # Print all unique 'provider' values in providerConnections
        providers = set(c.get('provider') for c in conn if isinstance(c, dict))
        print("Unique providers:", providers)

# Search for "codex" in the entire JSON (case-insensitive)
def search_val(obj, path=""):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'codex' or (isinstance(v, str) and 'codex' in v.lower()):
                results.append((f"{path}.{k}", v))
            results.extend(search_val(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            if isinstance(item, str) and 'codex' in item.lower():
                results.append((f"{path}[{idx}]", item))
            results.extend(search_val(item, f"{path}[{idx}]"))
    return results

print("\n=== Codex search results ===")
res = search_val(d)
for r in res[:20]:
    path_str, val = r
    # mask token
    if any(x in path_str.lower() for x in ['token', 'key', 'password', 'cred', 'secret']):
        val = str(val)[:10] + "..." if isinstance(val, str) else val
    print(f"{path_str}: {val}")
