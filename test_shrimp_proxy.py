import urllib.request
import json

url = "http://127.0.0.1:20131/v1/chat/completions"
payload = {
    "model": "opencode:gemini-3-flash",
    "messages": [{"role": "user", "content": "Hello! Respond with a simple Pong!"}],
    "stream": False
}

headers = {
    "Content-Type": "application/json"
}

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers=headers,
    method='POST'
)

print(f"正在向 shrimp-proxy ({url}) 發送測試請求...")
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("\nshrimp-proxy 響應:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print("請求失敗 (Error):", e)
