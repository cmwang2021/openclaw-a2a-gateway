import datetime

log_path = '/tmp/openclaw/openclaw-2026-05-26.log'
with open(log_path) as f:
    lines = f.readlines()

print("=== Logs matching time 05:01 === ")
for line in lines:
    if '05:01:' in line or '05:02:' in line or '05:03:' in line:
        if 'error' in line.lower() or 'fail' in line.lower() or 'google-gemini-cli' in line or '9router' in line or 'task' in line:
            print(line.strip())
