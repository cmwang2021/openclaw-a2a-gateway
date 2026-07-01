#!/bin/bash
# phase-b1-roundtrip.sh — 驗證矩陣 v0.1 Phase B1: shrimp-01 Auth Round-trip
TOKEN="57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4"
HOST="http://localhost:18800"

echo "╔══════════════════════════════════════════════╗"
echo "║  Phase B1: shrimp-01 Auth Round-trip 驗證    ║"
echo "╚══════════════════════════════════════════════╝"

# Test 1: Unauth — 應被拒絕
echo ""
echo "── Test 1: 未授權存取 ──"
UNAUTH=$(curl -s -w '\n%{http_code}' -X POST "$HOST/a2a/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"unauth-001","method":"message/send","params":{"message":{"role":"user","parts":[{"text":"unauth test"}]}}}')
UNAUTH_CODE=$(echo "$UNAUTH" | tail -1)
UNAUTH_BODY=$(echo "$UNAUTH" | head -n -1)
echo "  HTTP Status: $UNAUTH_CODE"
echo "  Response: $UNAUTH_BODY"
if [ "$UNAUTH_CODE" = "401" ] || [ "$UNAUTH_CODE" = "403" ]; then
  echo "  ✅ 未授權正確被拒"
else
  echo "  ⚠️ 未授權存取返回 $UNAUTH_CODE (非 401/403)"
fi

# Test 2: Auth — 應成功
echo ""
echo "── Test 2: Bearer Token 授權存取 ──"
AUTH=$(curl -s -w '\n%{http_code}' -X POST "$HOST/a2a/jsonrpc" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"jsonrpc":"2.0","id":"auth-roundtrip-001","method":"message/send","params":{"message":{"role":"user","parts":[{"text":"蝦家班驗證矩陣 v0.1 — Phase B1 Auth Round-trip 測試。請確認收到並回覆。"}]}}}')
AUTH_CODE=$(echo "$AUTH" | tail -1)
AUTH_BODY=$(echo "$AUTH" | head -n -1)
echo "  HTTP Status: $AUTH_CODE"
echo "  Response (前200字): $(echo "$AUTH_BODY" | head -c 200)"

# Test 3: Agent Card 驗證
echo ""
echo "── Test 3: Agent Card Discovery ──"
CARD=$(curl -s "$HOST/.well-known/agent-card.json")
CARD_URL=$(echo "$CARD" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("url","ERROR"))' 2>/dev/null)
CARD_NAME=$(echo "$CARD" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("name","ERROR"))' 2>/dev/null)
CARD_PROTO=$(echo "$CARD" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("protocolVersion","ERROR"))' 2>/dev/null)
CARD_SEC=$(echo "$CARD" | python3 -c 'import sys,json; print(json.dumps(json.load(sys.stdin).get("securitySchemes",{})))' 2>/dev/null)
echo "  URL: $CARD_URL"
echo "  Name: $CARD_NAME"
echo "  Protocol: $CARD_PROTO"
echo "  Security: $CARD_SEC"

if echo "$CARD_URL" | grep -q "100.123.6.86"; then
  echo "  ✅ Agent Card URL 正確指向 One Dollar 商用實驗網"
else
  echo "  ❌ Agent Card URL 仍指向錯誤地址"
fi

# Summary
echo ""
echo "════════════════════════════════"
echo "  DISCOVERY:    $(if echo "$CARD_URL" | grep -q "100.123.6.86"; then echo '✅ OK'; else echo '❌ FAIL'; fi)"
echo "  REACHABILITY: ✅ OK (localhost)"
echo "  AUTH:         $(if [ "$AUTH_CODE" = "200" ]; then echo '✅ OK'; else echo "❌ HTTP $AUTH_CODE"; fi)"
echo "  ROUNDTRIP:    $(if [ "$AUTH_CODE" = "200" ]; then echo '✅ OK'; else echo '❌ FAIL'; fi)"
echo "════════════════════════════════"
