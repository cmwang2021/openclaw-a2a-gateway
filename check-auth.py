import json
d = json.load(open("/home/shrimpclan_ai/.openclaw/openclaw.json"))
g = d.get("gateway", {})
a = g.get("auth", {})
print("gateway.port:", g.get("port"))
print("gateway.bind:", g.get("bind"))
print("gateway.mode:", g.get("mode"))
print("gateway.auth.mode:", a.get("mode"))
print("gateway.auth.token set:", bool(a.get("token")))
print("gateway.auth.token value:", str(a.get("token",""))[:12] + "..." if a.get("token") else "EMPTY")
print("gateway.auth.password set:", bool(a.get("password")))
print("gateway.auth.password value:", str(a.get("password",""))[:12] + "..." if a.get("password") else "EMPTY")

# Also check OPENCLAW_GATEWAY_TOKEN from systemd env vs config
import os
env_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
print("\nOPENCLAW_GATEWAY_TOKEN env:", env_token[:12] + "..." if env_token else "NOT SET")

# Check the remote password in a2a plugin config
plugins = d.get("plugins", {}).get("entries", {})
a2a = plugins.get("a2a-gateway", {}).get("config", {})
remote = a2a.get("remote", {})
print("\na2a-gateway.remote.password set:", bool(remote.get("password")))
print("a2a-gateway.remote.password value:", str(remote.get("password",""))[:12] + "..." if remote.get("password") else "EMPTY")
