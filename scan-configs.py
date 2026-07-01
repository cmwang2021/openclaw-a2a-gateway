import os

root_dir = '/home/user/.openclaw'
search_str = '100.88.129.94'

print(f"Searching for '{search_str}' in {root_dir}...")
for root, dirs, files in os.walk(root_dir):
    # Exclude node_modules and cache
    if 'node_modules' in root or 'cache' in root or 'a2a-tasks' in root:
        continue
    for file in files:
        if file.endswith(('.sqlite', '.db', '.png', '.jpg', '.jpeg', '.zip', '.gz')):
            continue
        path = os.path.join(root, file)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if search_str in content:
                    print(f"Found in: {path}")
                    for i, line in enumerate(content.splitlines()):
                        if search_str in line:
                            print(f"  Line {i+1}: {line.strip()}")
        except Exception as e:
            pass
