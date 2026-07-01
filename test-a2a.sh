#!/bin/bash
# A2A round-trip test — complete message format
echo "=== A2A ROUND-TRIP TEST (complete format) ==="
echo "Time: $(date -u)"

MSG_ID=$(cat /proc/sys/kernel/random/uuid)

curl -s --max-time 180 \
  -X POST http://localhost:18800/a2a/jsonrpc \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": \"final-v04\",
    \"method\": \"message/send\",
    \"params\": {
      \"message\": {
        \"kind\": \"message\",
        \"messageId\": \"$MSG_ID\",
        \"role\": \"user\",
        \"parts\": [{\"kind\": \"text\", \"text\": \"A2A round-trip test. Reply briefly: Pong!\"}]
      }
    }
  }"

echo ""
echo "Finished: $(date -u)"
