#!/bin/bash
# phase-b1-simple-ping.sh — Send simple message to avoid workspace grep
TOKEN="57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4"
HOST="http://localhost:18800"
MSG_ID="simple-ping-$(date +%s)"

echo "╔══════════════════════════════════════════════╗"
echo "║  Phase B1: A2A Simple Ping (No Grep Trigger) ║"
echo "╚══════════════════════════════════════════════╝"
echo "  Message ID: $MSG_ID"
echo ""

RESULT=$(curl -s -w '\n%{http_code}' -X POST "$HOST/a2a/jsonrpc" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": \"$MSG_ID\",
    \"method\": \"message/send\",
    \"params\": {
      \"message\": {
        \"messageId\": \"$MSG_ID\",
        \"role\": \"user\",
        \"parts\": [{\"kind\": \"text\", \"text\": \"ping\"}]
      }
    }
  }")

HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | head -n -1)

echo "── 結果 ──"
echo "  HTTP: $HTTP_CODE"
echo "  Body: $(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")"
