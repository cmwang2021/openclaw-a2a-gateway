import urllib.request
import json
import uuid
import ssl

# 透過 Tailscale Shared Node 被分配到的映射 IP (100.83.105.34) 發起 A2A 跨節點握手
url = "https://100.83.105.34/a2a/jsonrpc"
token = "openclaw-rules"

payload = {
    "jsonrpc": "2.0",
    "id": "nest2-to-abai-v4",
    "method": "message/send",
    "params": {
        "message": {
            "kind": "message",
            "messageId": str(uuid.uuid4()),
            "role": "user",
            "parts": [{"kind": "text", "text": "阿百1號，我是 Nest 2.0 宿主機的蝦仁班主。這是一次跨節點的 A2A 握手實測，收到請簡短回覆我 Pong！"}]
        }
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# 忽略 SSL 憑證驗證，確保在 IP 直連下不受憑證網域限制
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers=headers,
    method='POST'
)

print(f"蝦仁班主正在發起 A2A 到阿百1號 ({url})...")
try:
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("\n阿百1號的回覆 (A2A Response):")
        print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    # 嘗試 Fallback 2: 使用 MagicDNS 域名
    fallback_url = "https://abai-01.tail7752b1.ts.net/a2a/jsonrpc"
    print(f"IP 連線失敗，正在嘗試 Fallback 到 MagicDNS 域名 ({fallback_url})...")
    try:
        req_fallback = urllib.request.Request(
            fallback_url, 
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req_fallback, context=ctx, timeout=30) as response:
            res = json.loads(response.read().decode('utf-8'))
            print("\n阿百1號的回覆 (A2A Response):")
            print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e_fallback:
        print("Fallback 也失敗了 (Error):", e_fallback)
