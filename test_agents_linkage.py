#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蝦家班 AI 代理網路連動實測套件 (test_agents_linkage.py)
專為「蝦仁班主」設計。當探長在 Telegram 呼叫測試時，蝦仁班主應直接運行此腳本，
並將真實無誤的終端輸出呈報給探長，嚴禁任何編造、幻想或胡說八道！
"""

import socket
import urllib.request
import json
import subprocess
import time

def check_tcp_port(ip, port, timeout=2):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False

def http_get_json(url, timeout=2):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Xiaren-Tester/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return None, str(e)

def run_shell(cmd):
    try:
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def main():
    print("==================================================")
    print("🦐 蝦家班 AI 代理網路連動實體測試報告 (實測為準) 🦐")
    print(f"測試時間 (UTC): {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("==================================================")

    # 1. 測試我自己 (宿主機 A2A 網關)
    print("\n[1] 測試自己 (Nest 2.0 宿主機 A2A 網關 :18800)")
    card_status, card_data = http_get_json("http://localhost:18800/.well-known/agent-card.json")
    if card_status == 200:
        print(f"  🟢 網關狀態: 在線 (OK)")
        print(f"  🟢 代理名稱: {card_data.get('name', '未知')}")
        print(f"  🟢 協議版本: {card_data.get('protocolVersion', '未知')}")
    else:
        print(f"  🔴 網關狀態: 離線或異常 (FAILED)")
        print(f"  🔴 錯誤原因: {card_data}")

    # 2. 測試阿百館長 (Docker 容器)
    print("\n[2] 測試阿百館長 (Docker 容器 openclaw-runtime :18790)")
    docker_port_alive = check_tcp_port("127.0.0.1", 18790)
    docker_ps_code, docker_ps_out, _ = run_shell("docker ps --filter name=openclaw-runtime --format '{{.Status}}'")
    
    if docker_port_alive:
        print(f"  🟢 核心端口 (18790): 可連通 (OK)")
    else:
        print(f"  🔴 核心端口 (18790): 連線失敗 (FAILED) — 請檢查容器映射")
        
    if docker_ps_code == 0 and docker_ps_out:
        print(f"  🟢 容器狀態: {docker_ps_out} (OK)")
    else:
        print(f"  🔴 容器狀態: 未在運行或無法查詢 (FAILED)")

    # 3. 測試 9Router-Shrimp 模型提供者 (:20129)
    print("\n[3] 測試模型端點 (9router-shrimp :20129)")
    router_alive = check_tcp_port("127.0.0.1", 20129)
    if router_alive:
        models_status, models_data = http_get_json("http://localhost:20129/v1/models")
        if models_status == 200:
            print(f"  🟢 端口狀態: 可連通且 API 響應正常 (OK)")
            models_list = [m.get('id') for m in models_data.get('data', [])] if isinstance(models_data, dict) else []
            print(f"  🟢 可用模型: {', '.join(models_list[:3])} 等共 {len(models_list)} 個")
        else:
            print(f"  🟡 端口狀態: 可連通，但 API 回報錯誤 (DEGRADED)")
            print(f"  🟡 錯誤訊息: {models_data}")
    else:
        print(f"  🔴 端口狀態: 連線失敗 (FAILED) — 小米金鑰或 Playground 服務可能未啟動")

    # 4. 測試蝦馬仕 (Nest 1.0 Hermes Agent)
    print("\n[4] 測試蝦馬仕 (Nest 1.0 :100.121.100.54)")
    hermes_alive = check_tcp_port("100.121.100.54", 22, timeout=2)
    if hermes_alive:
        print(f"  🟢 連線狀態: 可直連 (OK) — 奇蹟！單向 Shared Node 限制已解除？")
    else:
        print(f"  🔴 連線狀態: 無法直連 (BLOCKED) — 證實有 Tailscale 單向限制。請改用中繼跳板")

    # 5. 測試阿百1號 (Firebase Studio 蝦工坊)
    print("\n[5] 測試阿百1號工坊 (abai-01 :100.83.105.23)")
    idx_tailscale_ssh = check_tcp_port("100.83.105.23", 22, timeout=2) # Tailscale SSH port 22
    idx_ssh_2222 = check_tcp_port("100.83.105.23", 2222, timeout=2)  # NixOS SSH port 2222
    idx_a2a_18800 = check_tcp_port("100.83.105.23", 18800, timeout=2)
    
    if idx_tailscale_ssh or idx_ssh_2222:
        print(f"  🟢 SSH 連線通道: 在線 (OK) — 可用 tailscale ssh 或 ssh -p 2222 接入！")
        if idx_tailscale_ssh:
            print(f"    - Tailscale SSH (port 22): 🟢 可連通")
        if idx_ssh_2222:
            print(f"    - NixOS SSH (port 2222): 🟢 可連通")
    else:
        print(f"  🔴 SSH 連線通道: 連線失敗 (OFFLINE) — 工坊未拉起或休眠中")
        
    if idx_a2a_18800:
        print(f"  🟢 A2A 端口 (18800): 可直連 (OK)")
    else:
        print(f"  🔴 A2A 端口 (18800): 無法直連 (BLOCKED) — 外部端口遭 NixOS 阻擋，需拉起 Tailscale Funnel 連接")

    print("\n==================================================")
    print("💡 蝦仁班主認知指引：")
    print(" 1. 對於標記 [OK] 的節點，代表管道 100% 暢通，可立即發送 task。")
    print(" 2. 對於標記 [FAILED] 或 [BLOCKED] 的節點，應明確向探長回報『無法直接連動』。")
    print(" 3. 請勇敢指出物理連線阻礙，拒絕捏造任何 Pong 回應！")
    print("==================================================")

if __name__ == "__main__":
    main()
