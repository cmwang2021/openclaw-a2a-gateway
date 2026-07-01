import json
d = json.load(open("/home/shrimpclan_ai/.openclaw/openclaw.json"))
a2a = d.get("plugins",{}).get("entries",{}).get("a2a-gateway",{}).get("config",{})
sec = a2a.get("security",{})
print("inboundAuth:", sec.get("inboundAuth"))
t = sec.get("token","")
print("token:", repr(t))
print("token length:", len(t))
