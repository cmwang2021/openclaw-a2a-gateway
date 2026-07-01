#!/usr/bin/env python3
"""Fix gateway.auth.token: replace env var literal with actual value, then verify."""
import json
import subprocess
import sys

CONFIG_PATH = '/home/shrimpclan_ai/.openclaw/openclaw.json'
ACTUAL_TOKEN = '93cb49768b1fed50bfcb0aeda0c9a852ba44bc995a218b05cd8d0ecc1c2acaa7'

# Step 1: Read current config
with open(CONFIG_PATH) as f:
    d = json.load(f)

old_token = d.get('gateway', {}).get('auth', {}).get('token', '')
print(f"[BEFORE] gateway.auth.token = {repr(old_token)}")

if old_token == ACTUAL_TOKEN:
    print("[SKIP] Token already matches actual value, no change needed.")
    sys.exit(0)

# Step 2: Update token
d['gateway']['auth']['token'] = ACTUAL_TOKEN

# Step 3: Write back
with open(CONFIG_PATH, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

# Step 4: Verify
with open(CONFIG_PATH) as f:
    d2 = json.load(f)
new_token = d2.get('gateway', {}).get('auth', {}).get('token', '')
print(f"[AFTER]  gateway.auth.token = {new_token[:12]}...{new_token[-4:]}")
print(f"[OK]     Token matches: {new_token == ACTUAL_TOKEN}")
print(f"\n[WARN]   openclaw doctor 將會對明碼 token 產生 CRITICAL 警示 (已知)")
