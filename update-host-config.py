import json

path = '/home/shrimpclan_ai/.openclaw/openclaw.json'

with open(path, 'r') as f:
    d = json.load(f)

# Navigate to plugins -> entries -> a2a-gateway -> config
# Wait! In host openclaw.json, it was:
# "a2a-gateway": {
#   "enabled": true,
#   "config": { ... }
# }
# Let's verify the path of the keys in host config.
# Let's print them first or just modify both possible paths!
# In the sed output earlier:
#       "a2a-gateway": {
#         "enabled": true,
#         "config": {
#           "agentCard": { ... }

def update_config(obj):
    if not isinstance(obj, dict):
        return
    for k, v in obj.items():
        if k == 'a2a-gateway' and isinstance(v, dict):
            config = v.get('config', {})
            if isinstance(config, dict):
                # 1. Update agentCard.url
                card = config.get('agentCard', {})
                if isinstance(card, dict):
                    card['url'] = "http://100.123.6.86:18800/a2a/jsonrpc"
                    config['agentCard'] = card
                # 2. Update security
                sec = config.get('security', {})
                if not isinstance(sec, dict):
                    sec = {}
                sec['inboundAuth'] = "bearer"
                sec['token'] = "57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4"
                config['security'] = sec
                v['config'] = config
        else:
            update_config(v)

update_config(d)

with open(path, 'w') as f:
    json.dump(d, f, indent=2)

print("Host openclaw.json updated successfully!")
