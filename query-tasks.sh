#!/bin/bash
# query-tasks.sh — check tasks in lcm.db
sqlite3 /home/user/.openclaw/lcm.db <<EOF
.headers on
.mode column
SELECT id, status, createdAt FROM tasks ORDER BY createdAt DESC LIMIT 5;
EOF
