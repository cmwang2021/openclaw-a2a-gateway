import json, subprocess, os

# Check host OpenClaw config
host_cfg = '/home/shrimpclan_ai/.openclaw/openclaw.json'
try:
    with open(host_cfg) as f:
        d = json.load(f)
    g = d.get('gateway', {})
    print("=== HOST OpenClaw gateway config ===")
    print(f"  port: {g.get('port')}")
    print(f"  bind: {g.get('bind')}")
    print(f"  mode: {g.get('mode')}")
    print(f"  auth.mode: {g.get('auth',{}).get('mode')}")
    print(f"  auth.password: {'***set***' if g.get('auth',{}).get('password') else 'not set'}")
    
    # Check A2A plugin config
    a2a = d.get('plugins',{}).get('entries',{}).get('a2a-gateway',{})
    print(f"\n  a2a-gateway enabled: {a2a.get('enabled')}")
    a2a_cfg = a2a.get('config',{})
    print(f"  a2a agentCard.url: {a2a_cfg.get('agentCard',{}).get('url')}")
    print(f"  a2a inboundAuth: {a2a_cfg.get('security',{}).get('inboundAuth')}")
    
    # Check main agent
    agents = d.get('agents',{}).get('list',[])
    for a in agents:
        if a.get('id') == 'main':
            print(f"\n=== HOST main agent ===")
            print(f"  name: {a.get('name')}")
            m = a.get('model', {})
            if isinstance(m, str):
                print(f"  model: {m}")
            else:
                print(f"  primary: {m.get('primary')}")
                print(f"  fallbacks: {m.get('fallbacks')}")
            break
except Exception as e:
    print(f"Error reading host config: {e}")

# Check systemd service
svc = '/home/shrimpclan_ai/.config/systemd/user/openclaw-gateway.service'
try:
    with open(svc) as f:
        print(f"\n=== systemd service file ===")
        print(f.read())
except:
    print(f"\nSystemd service file not found at {svc}")

# Check container config gateway section
container_cfg = '/mnt/shrimp-data/openclaw-docker/aba-v2/.openclaw/openclaw.json'
try:
    with open(container_cfg) as f:
        cd = json.load(f)
    cg = cd.get('gateway', {})
    print("=== CONTAINER OpenClaw gateway config ===")
    print(f"  port: {cg.get('port')}")
    print(f"  bind: {cg.get('bind')}")
    print(f"  mode: {cg.get('mode')}")
except Exception as e:
    print(f"Error reading container config: {e}")
