---
inclusion: always
description: Main Agent 文件清單 + 幾時讀（L1 - 永遠載入）
---

# Main Agent 文件導航

| 文件 | L層 | inclusion | 幾時讀 |
|------|-----|-----------|--------|
| `role.md` | L1 | always | 身份 + 核心規則（自動載入） |
| `navigation.md` | L1 | always | 本文件（自動載入） |
| `tools.md` | L2 | always | 工具權限（自動載入） |
| `project-file-paths.md` | L2 | always | Project 路徑查表 + 目錄結構圖（自動載入） |
| `project-protocols-comm.md` | L2 | always | Sub Agent 調用規則 + inbox/outbox 格式（自動載入） |
| `project-protocols-checkpoint.md` | L3 | manual | 建立/恢復 Checkpoint 時 |
| `project-protocols-memory.md` | L3 | manual | 完成調度後更新 memory 時 |
| `project-protocols-record-write.md` | L3 | manual | 寫入 ProjectRecord 遇到問題時 |
| `project-protocols-format.md` | L3 | manual | 派工 / 收 reply / 寫記錄前 |
| `project-protocols-git.md` | L3 | manual | Git commit / push 前 |
| `project-protocols-error-handling.md` | L3 | manual | 遇到 error 時 |
| `project-protocols-size-rules.md` | L3 | manual | 調度大任務 / 怕 timeout 時 |
| `project-protocols-shell-policy.md` | L3 | manual | 想用 shell 前 |
| `role-execution.md` | L3 | manual | 派工 / 收 reply / 做決定時 |
| `role-constraints.md` | L3 | manual | 處理 blocked / 循環限制時 |
