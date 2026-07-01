# 建立 Playground ↔ 蝦窩 Nest 2 A2A 溝通管道

## 背景

在 Playground 端有 `openclaw-a2a-gateway` 外掛原始碼（v1.4.0），而蝦窩 Nest 2（`http://100.88.129.94:18800`，Tailscale IP）已經有一個運作中的 A2A Gateway 實例。目標是讓兩端透過 A2A v0.3.0 協定建立雙向溝通。

## 現況評估

### ✅ Nest 2 端 (已完成)

探測結果顯示 Nest 2 的 A2A Gateway **已正常運作**：

| 項目 | 狀態 | 備註 |
|------|------|------|
| Agent Card | ✅ 可存取 | `http://100.88.129.94:18800/.well-known/agent-card.json` |
| 協定版本 | A2A v0.3.0 | 相容 |
| 名稱 | `OpenClaw A2A Gateway` | 預設值，建議改名 |
| Skills | `[]` 空 | 尚未設定 |
| Security | `none` | 無 inbound auth，沒有 bearer token |
| Peers | `{}` 空 | 尚未配對任何 peer |
| URL | `localhost:18800` | ⚠️ 需改為 Tailscale IP |
| Metrics | ✅ 正常 | 所有計數器為 0（全新狀態） |

### ❌ Playground 端 (待完成)

Playground 只有 `openclaw-a2a-gateway` 的原始碼，**但沒有運行中的 OpenClaw 實例**。需要確認本地是否有 OpenClaw 運行環境。

## User Review Required

> [!IMPORTANT]
> **本地 OpenClaw 運行環境**：Playground 端需要有一個運行中的 OpenClaw 實例才能完整使用 A2A Gateway 外掛（因為外掛需要 OpenClaw Plugin API 來註冊端點和路由至 Agent）。請確認：
> 1. 你的本地（Windows）是否有安裝並運行 OpenClaw？
> 2. 還是你想用**獨立模式**（不依賴 OpenClaw，用 `a2a-send.mjs` 腳本直接呼叫 Nest 2）？

> [!WARNING]  
> **Nest 2 的 agentCard.url 設定有誤**：目前 Nest 2 的 Agent Card 中 `url` 指向 `http://localhost:18800/a2a/jsonrpc`，如果從外部呼叫會失敗（localhost 指的是本地）。需要 SSH 進 Nest 2 修改為 `http://100.88.129.94:18800/a2a/jsonrpc`。

## Open Questions

> [!IMPORTANT]
> 1. **你本地有 OpenClaw 嗎？** 如果有，可以做完整雙向 peer 配對。如果沒有，可以先用腳本做**單向溝通**（Playground → Nest 2）。
> 2. **Nest 2 的 SSH 存取**：是否可以用 migration-master skill 中的 SSH 配置（`TARGET_HOST=35.209.51.82`）來修改 Nest 2 的 A2A 設定？
> 3. **需要 auth 嗎？** 目前 Nest 2 的 inbound auth 為 `none`，開發階段可先不啟用，但如果長期使用建議加上 bearer token。
> 4. **Playground 端的 Tailscale IP 是什麼？** 需要讓 Nest 2 知道如何回連（如果做雙向的話）。

## Proposed Changes

### 方案 A：單向溝通（Playground → Nest 2）— 最小可行

不需要本地 OpenClaw 實例，直接用現有腳本呼叫 Nest 2。

#### Step 1: 安裝 A2A Gateway 依賴

```bash
cd c:\Users\ellio\Code\cursor\Playground\openclaw-a2a-gateway
npm install
```

#### Step 2: 測試 Agent Card 探索

```bash
node skill/scripts/a2a-ping.mjs --peer-url http://100.88.129.94:18800
```

#### Step 3: 傳送測試訊息

```bash
node skill/scripts/a2a-send.mjs \
  --peer-url http://100.88.129.94:18800 \
  --message "Hello from Playground! 蝦家班報到 🦐"
```

> 因為 Nest 2 沒有 auth，所以不需要 `--token`。

---

### 方案 B：雙向溝通（完整 Peer 配對）— 需要兩端 OpenClaw

#### Nest 2 端設定（SSH 遠端）

1. 修正 agentCard.url：

```bash
openclaw config set plugins.entries.a2a-gateway.config.agentCard.url 'http://100.88.129.94:18800/a2a/jsonrpc'
openclaw config set plugins.entries.a2a-gateway.config.agentCard.name 'Nest2-蝦窩'
openclaw config set plugins.entries.a2a-gateway.config.agentCard.skills '[{"id":"chat","name":"chat","description":"蝦窩 AI Agent Bridge"}]'
```

2. 產生安全 token：

```bash
NEST2_TOKEN=$(openssl rand -hex 24)
openclaw config set plugins.entries.a2a-gateway.config.security.inboundAuth 'bearer'
openclaw config set plugins.entries.a2a-gateway.config.security.token "$NEST2_TOKEN"
```

3. 新增 Playground 為 peer：

```bash
openclaw config set plugins.entries.a2a-gateway.config.peers '[{"name":"Playground","agentCardUrl":"http://<PLAYGROUND_TAILSCALE_IP>:18800/.well-known/agent-card.json","auth":{"type":"bearer","token":"<PLAYGROUND_TOKEN>"}}]'
```

4. 重啟：

```bash
openclaw gateway restart
```

#### Playground 端設定（本地）

1. 設定 Agent Card、Security、Peer（指向 Nest 2）
2. 重啟閘道
3. 驗證雙向通訊

---

## Verification Plan

### Automated Tests

1. **Agent Card 探索**：`a2a-ping.mjs --peer-url http://100.88.129.94:18800` — 應回傳有效的 Agent Card
2. **訊息傳送**：`a2a-send.mjs --peer-url http://100.88.129.94:18800 --message "test"` — 應取得 agent 回應
3. **Metrics 檢查**：確認 `messages_received` 計數器遞增

### Manual Verification

- 確認 Nest 2 的 OpenClaw 日誌中有收到 A2A 請求的記錄
- 如果做雙向，從 Nest 2 傳訊息到 Playground 並確認收到
