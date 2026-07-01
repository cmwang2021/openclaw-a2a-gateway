# Walkthrough: Playground → Nest 2 A2A 溝通管道

## 目標

從本地 Playground 透過 A2A v0.3.0 協定，向蝦家班蝦窩 Nest 2.0（`http://100.88.129.94:18800`）傳送訊息並接收回應。

## 變更

### 1. 本地：安裝 npm 依賴

```bash
cd openclaw-a2a-gateway && npm install
```

安裝了 `@a2a-js/sdk`、Express、gRPC 等 800 個套件，讓 `a2a-ping.mjs` 和 `a2a-send.mjs` 腳本可正常運作。

---

### 2. Nest 2：修正 A2A Gateway 設定

> [!NOTE]
> Nest 2 原本 A2A Gateway 只有 `"enabled": true`，所有 URL 指向 `localhost`、無 skills、無 agent name。

透過 SSH 上傳 `fix-nest2-a2a.py` 修正 `openclaw.json` 中的 `plugins.entries.a2a-gateway.config`：

| 設定 | 修正前 | 修正後 |
|------|--------|--------|
| `agentCard.name` | `OpenClaw A2A Gateway` | `Nest2-蝦窩` |
| `agentCard.description` | `A2A bridge for OpenClaw agents` | `蝦家班蝦窩 Nest 2.0 A2A Agent` |
| `agentCard.url` | `http://localhost:18800/a2a/jsonrpc` | `http://100.88.129.94:18800/a2a/jsonrpc` |
| `agentCard.skills` | `[]` | `[chat, code, ops]` |
| `routing.defaultAgentId` | (預設) | `main` |

```diff:fix-nest2-a2a.py
===
#!/usr/bin/env python3
"""Fix Nest 2 A2A Gateway config: set agentCard.url to Tailscale IP."""
import json, shutil, sys

CONFIG_PATH = "/home/shrimpclan_ai/.openclaw/openclaw.json"

with open(CONFIG_PATH, "r") as f:
    data = json.load(f)

# Ensure plugins.entries.a2a-gateway.config exists
plugins = data.setdefault("plugins", {})
entries = plugins.setdefault("entries", {})
a2a = entries.setdefault("a2a-gateway", {})
a2a["enabled"] = True
config = a2a.setdefault("config", {})

# Set agentCard
card = config.setdefault("agentCard", {})
card["name"] = "Nest2-蝦窩"
card["description"] = "蝦家班蝦窩 Nest 2.0 A2A Agent"
card["url"] = "http://100.88.129.94:18800/a2a/jsonrpc"
card["skills"] = [
    {"id": "chat", "name": "chat", "description": "蝦窩 AI Agent Bridge"},
    {"id": "code", "name": "code", "description": "Code review and analysis"},
    {"id": "ops",  "name": "ops",  "description": "DevOps and system operations"}
]

# Ensure server is set
server = config.setdefault("server", {})
server["host"] = "0.0.0.0"
server["port"] = 18800

# No auth needed
security = config.setdefault("security", {})
security["inboundAuth"] = "none"

# Routing
routing = config.setdefault("routing", {})
routing["defaultAgentId"] = "main"

print("=== Before (a2a-gateway entry) ===")
print(json.dumps(entries.get("a2a-gateway", {}), indent=2, ensure_ascii=False))

# Backup
shutil.copy2(CONFIG_PATH, CONFIG_PATH + ".bak.pre-a2a-fix")

# Write
with open(CONFIG_PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n=== After (a2a-gateway entry) ===")
print(json.dumps(entries.get("a2a-gateway", {}), indent=2, ensure_ascii=False))
print("\n✅ Config updated and backup saved to", CONFIG_PATH + ".bak.pre-a2a-fix")
```

---

### 3. Nest 2：重啟 OpenClaw

使用 systemd user unit 重啟（避免 `openclaw gateway restart` 產生重複 process 的 bug）：

```bash
sudo -u shrimpclan_ai XDG_RUNTIME_DIR=/run/user/$(id -u shrimpclan_ai) \
  systemctl --user restart openclaw
```

---

## 驗證結果

### ✅ Agent Card 探索

```
✅ http://100.88.129.94:18800 — online (820ms) — Nest2-蝦窩
  version: 1.0.0
```

### ✅ A2A 訊息傳送

```bash
node skill/scripts/a2a-send.mjs \
  --peer-url http://100.88.129.94:18800 \
  --non-blocking --wait --timeout-ms 120000 --poll-ms 2000 \
  --message "Hello from Playground! 蝦家班報到 🦐 請簡短回覆確認收到。"
```

**回應：** `🍤 蝦仁收到！Playground 連線正常，蝦家班待命就緒 🦐✨`

### ✅ Metrics 驗證

| 指標 | 值 |
|------|-----|
| `messages_received` | 15 |
| `tasks.started` | 1 |
| `tasks.completed` | 1 |
| `tasks.failed` | 0 |
| `average_duration_ms` | 38,264 ms |

## 日後使用方式

從 Playground 發送訊息到蝦窩：

```bash
cd c:\Users\ellio\Code\cursor\Playground\openclaw-a2a-gateway

# 快速 ping
node skill/scripts/a2a-ping.mjs --peer-url http://100.88.129.94:18800

# 傳送訊息（同步，適合短訊息）
node skill/scripts/a2a-send.mjs \
  --peer-url http://100.88.129.94:18800 \
  --message "你的訊息"

# 傳送訊息（非同步+輪詢，適合長任務）
node skill/scripts/a2a-send.mjs \
  --peer-url http://100.88.129.94:18800 \
  --non-blocking --wait --timeout-ms 120000 \
  --message "需要比較久的任務"

# 指定路由到特定 agent（如 perplexity）
node skill/scripts/a2a-send.mjs \
  --peer-url http://100.88.129.94:18800 \
  --agent-id perplexity \
  --message "幫我搜尋..."
```
