#!/bin/bash
# phase-b1-full-roundtrip.sh — 完整 A2A v0.3.0 合規 Round-trip
TOKEN="57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4"
HOST="http://localhost:18800"
MSG_ID="verify-matrix-v01-$(date +%s)"

echo "╔══════════════════════════════════════════════╗"
echo "║  Phase B1: 完整 A2A v0.3.0 Round-trip       ║"
echo "╚══════════════════════════════════════════════╝"
echo "  Message ID: $MSG_ID"
echo "  Timestamp:  $(date -Iseconds)"
echo ""

# A2A v0.3.0 compliant message/send
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
        \"parts\": [{\"kind\": \"text\", \"text\": \"蝦家班驗證矩陣 v0.1 Phase B1 完整 Round-trip 測試。我是 hp-Matrix Opus Verifier，請確認你是 shrimp-01 (Nest2-蝦窩) 節點。\"}]
      }
    }
  }")

HTTP_CODE=$(echo "$RESULT" | tail -1)
BODY=$(echo "$RESULT" | head -n -1)

echo "── 結果 ──"
echo "  HTTP: $HTTP_CODE"
echo "  Body: $(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")"

if [ "$HTTP_CODE" = "200" ]; then
  echo ""
  echo "  ✅ ROUNDTRIP_OK — shrimp-01 完成帶認證的最小合法往返"
else
  echo ""
  echo "  ❌ ROUNDTRIP FAIL — HTTP $HTTP_CODE"
fi
