#!/usr/bin/env python3
"""Fix Nest 2 A2A Gateway config: set agentCard.url to Tailscale IP."""
import json, shutil, sys

CONFIG_PATH = "/home/shrimpclan_ai/.openclaw/openclaw.json"

with open(CONFIG_PATH, "r") as f:
    data = json.load(f)

# Ensure plugins.entries.a2a-gateway.config exists
plugins = data.setdefault("plugins", {})
entries = plugins.setdefault("entries", {})
a2a = entries.setdefault("a2a-gateway", {})
a2a["enabled"] = True
config = a2a.setdefault("config", {})

# Set agentCard
card = config.setdefault("agentCard", {})
card["name"] = "Nest2-蝦窩"
card["description"] = "蝦家班蝦窩 Nest 2.0 A2A Agent"
card["url"] = "http://100.88.129.94:18800/a2a/jsonrpc"
card["skills"] = [
    {"id": "chat", "name": "chat", "description": "蝦窩 AI Agent Bridge"},
    {"id": "code", "name": "code", "description": "Code review and analysis"},
    {"id": "ops",  "name": "ops",  "description": "DevOps and system operations"}
]

# Ensure server is set
server = config.setdefault("server", {})
server["host"] = "0.0.0.0"
server["port"] = 18800

# No auth needed
security = config.setdefault("security", {})
security["inboundAuth"] = "none"

# Routing
routing = config.setdefault("routing", {})
routing["defaultAgentId"] = "main"

print("=== Before (a2a-gateway entry) ===")
print(json.dumps(entries.get("a2a-gateway", {}), indent=2, ensure_ascii=False))

# Backup
shutil.copy2(CONFIG_PATH, CONFIG_PATH + ".bak.pre-a2a-fix")

# Write
with open(CONFIG_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n=== After (a2a-gateway entry) ===")
print(json.dumps(entries.get("a2a-gateway", {}), indent=2, ensure_ascii=False))
print("\n✅ Config updated and backup saved to", CONFIG_PATH + ".bak.pre-a2a-fix")
