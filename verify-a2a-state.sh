#!/bin/bash
# verify-a2a-state.sh — Post-Phase-A verification
echo "=== Gateway Processes ==="
ps aux | grep -i gateway | grep -v grep
echo ""
echo "=== Listening Ports ==="
ss -tlnp | grep -E '188'
echo ""
echo "=== A2A Config (from openclaw.json) ==="
python3 -c "
import json
with open('/home/user/.openclaw/openclaw.json') as f:
    d = json.load(f)
a2a = d['plugins']['entries']['a2a-gateway']
print(json.dumps(a2a, indent=2))
"
echo ""
echo "=== Live Agent Card ==="
curl -s http://localhost:18800/.well-known/agent-card.json | python3 -m json.tool 2>/dev/null || echo "Agent Card not available"
echo ""
echo "=== Test Unauth Access ==="
curl -s -o /dev/null -w 'HTTP %{http_code}' -X POST http://localhost:18800/a2a/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"t","method":"message/send","params":{"message":{"role":"user","parts":[{"text":"test"}]}}}' 2>&1
echo ""
