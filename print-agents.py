import json
d = json.load(open("/home/shrimpclan_ai/.openclaw/openclaw.json"))
print("=== AGENTS LIST ===")
agents_list = d.get("agents", {}).get("list", [])
print("Length of agents list:", len(agents_list))
for x in agents_list:
    if isinstance(x, dict):
        print(f"Agent ID: {x.get('id')} | Name: {x.get('name')}")
        print("System Instruction (first 100 chars):")
        print(repr(x.get('systemInstruction', 'None')[:100]))
    else:
        print("Type:", type(x), "Value:", repr(x))
