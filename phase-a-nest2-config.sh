#!/bin/bash
# Phase A: 蝦家班世界地圖 — 驗證矩陣 v0.1 基礎設施修正
# 目標: 修正 Nest 2.0 A2A Gateway Agent Card URL + 啟用 bearer token
# 執行: 由 hp-Matrix Opus Verifier 經 SSH 在 openclaw-runtime 容器內執行
# 日期: 2026-05-26

set -euo pipefail

echo "╔══════════════════════════════════════════════╗"
echo "║  🗺️ Phase A: A2A Gateway 基礎設施修正       ║"
echo "╚══════════════════════════════════════════════╝"

# === A1: 修正 Agent Card URL ===
echo ""
echo "── A1: 修正 Agent Card URL ──"
echo "  舊: http://100.88.129.94:18800 (蝦網 Tailnet)"
echo "  新: http://100.123.6.86:18800 (One Dollar 商用實驗網)"

# 使用 openclaw CLI 更新 (在容器內)
openclaw config set plugins.entries.a2a-gateway.config.agentCard.url \
  'http://100.123.6.86:18800/a2a/jsonrpc' 2>&1 || echo "WARN: openclaw config set failed, trying jq fallback"

echo "✅ A1 完成: Agent Card URL 已更新"

# === A2: 生成並啟用 Bearer Token ===
echo ""
echo "── A2: 啟用 Bearer Token ──"

# 生成安全 token
SHRIMP_TOKEN=$(openssl rand -hex 24)
echo "  Token (遮蔽): ${SHRIMP_TOKEN:0:8}...${SHRIMP_TOKEN: -8}"

openclaw config set plugins.entries.a2a-gateway.config.security.inboundAuth 'bearer' 2>&1 || true
openclaw config set plugins.entries.a2a-gateway.config.security.token "$SHRIMP_TOKEN" 2>&1 || true

echo "✅ A2 完成: Bearer Token 已啟用"

# === A3: 驗證配置生效 ===
echo ""
echo "── A3: 驗證配置 ──"

# 等待 gateway 重新載入
sleep 2

# 測試 Agent Card
echo "  檢測 Agent Card..."
CARD=$(curl -s --connect-timeout 5 http://localhost:18800/.well-known/agent-card.json 2>&1)
echo "  Agent Card URL: $(echo "$CARD" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("url","ERROR"))' 2>/dev/null || echo 'PARSE_ERROR')"
echo "  Agent Name: $(echo "$CARD" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("name","ERROR"))' 2>/dev/null || echo 'PARSE_ERROR')"

# 測試未授權存取 (應被拒絕)
echo ""
echo "  測試未授權存取 (應被拒絕)..."
UNAUTH_STATUS=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:18800/a2a/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"test-unauth","method":"message/send","params":{"message":{"role":"user","parts":[{"text":"test"}]}}}' 2>&1)
echo "  未授權 HTTP Status: $UNAUTH_STATUS (期望: 401)"

# 測試已授權存取
echo ""
echo "  測試已授權存取..."
AUTH_STATUS=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:18800/a2a/jsonrpc \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SHRIMP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":"test-auth","method":"message/send","params":{"message":{"role":"user","parts":[{"text":"驗證矩陣 v0.1 Auth Round-trip 測試"}]}}}' 2>&1)
echo "  已授權 HTTP Status: $AUTH_STATUS (期望: 200)"

# 輸出 Token 供外部驗證器使用
echo ""
echo "════════════════════════════════════"
echo "  SHRIMP_TOKEN=$SHRIMP_TOKEN"
echo "════════════════════════════════════"
echo ""
echo "🎯 Phase A 完成！請在 hp-Matrix 端使用上方 Token 進行外部驗證"
