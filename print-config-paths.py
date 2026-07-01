import json

with open('/home/user/.openclaw/openclaw.json') as f:
    d = json.load(f)

def print_paths(data, current_path=[]):
    if isinstance(data, dict):
        for k, v in data.items():
            new_path = current_path + [k]
            if k == 'a2a-gateway' or 'gateway' in k:
                print(f"Found path: {'.'.join(new_path)}")
            print_paths(v, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print_paths(item, current_path + [str(i)])

print_paths(d)
