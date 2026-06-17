---
inclusion: always
description: Generator 文件清單 + 幾時讀（L1 - 永遠載入）
---

# Generator 文件導航

| 文件 | L層 | inclusion | 幾時讀 |
|------|-----|-----------|--------|
| `role.md` | L1 | always | 身份 + 核心規則（自動載入） |
| `navigation.md` | L1 | always | 本文件（自動載入） |
| `tools.md` | L2 | always | 工具權限（自動載入） |
| `project-file-paths.md` | L2 | always | Project 路徑查表（自動載入） |
| `project-protocols-comm.md` | L2 | always | 通訊協議（自動載入） |
| `project-protocols-checkpoint.md` | L3 | manual | 建立/恢復 Checkpoint 時 |
| `project-protocols-decision-log.md` | L3 | manual | 每個 Step 完成後寫 Decision Log 時 |
| `project-protocols-memory.md` | L3 | manual | 寫 outbox reply 時 |
| `project-protocols-record-write.md` | L3 | manual | 寫入 ProjectRecord 遇到問題時 |
| `project-protocols-format.md` | L3 | manual | 寫 outbox reply 前 |
| `project-protocols-error-handling.md` | L3 | manual | 遇到 error 時 |
| `project-protocols-size-rules.md` | L3 | manual | 任務太大 / 怕 timeout 時 |
| `project-protocols-shell-policy.md` | L3 | manual | 想用 shell 前 |
| `role-execution.md` | L3 | manual | 開始任務時（啟動流程/自我評估/自學） |
| `role-constraints.md` | L3 | manual | 自我評估 / blocked 報告 / 操作模式 |
| `domain-knowledge-test-rules.md` | L3 | manual | **生成代碼前必讀**（測試規則） |
| `domain-knowledge-code-standards.md` | L3 | manual | 寫 code 時（命名/安全/錯誤處理） |
| `deterministic-first.md` | L2 | always | Deterministic-First 原則（自動載入） |
| `anti-amnesia.md` | L1 | always | 防失憶規則（自動載入） |
