import urllib.request
import json
import uuid

url = "http://100.123.6.86:18800/a2a/jsonrpc"
token = "57cd604bf91e1d73a0584353bb09b8be1fabbea85b6bdfa4"

payload = {
    "jsonrpc": "2.0",
    "id": "direct-matrix-v3",
    "method": "message/send",
    "params": {
        "message": {
            "kind": "message",
            "messageId": str(uuid.uuid4()),
            "role": "user",
            "parts": [{"kind": "text", "text": "這是來自 hp-Matrix 本地的 A2A 直連測試！請簡短回覆 Pong"}]
        }
    }
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers=headers,
    method='POST'
)

print(f"Sending direct A2A from local to {url}...")
try:
    with urllib.request.urlopen(req, timeout=120) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("\nResponse:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", e)
