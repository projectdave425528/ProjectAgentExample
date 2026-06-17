---
inclusion: always
description: Evaluator 文件清單 + 幾時讀（L1 - 永遠載入）
---

# Evaluator 文件導航

> 所有 Steering 文件清單。按 L 層級決定載入方式。

## 文件清單

| 文件 | L層 | inclusion | 幾時讀 |
|------|-----|-----------|--------|
| `role.md` | L1 | always | 身份 + 核心規則（自動載入） |
| `navigation.md` | L1 | always | 本文件（自動載入） |
| `tools.md` | L2 | always | 工具權限（自動載入） |
| `project-file-paths.md` | L2 | always | Project 路徑查表（自動載入） |
| `project-protocols-comm.md` | L2 | always | 通訊協議（自動載入） |
| `project-protocols-checkpoint.md` | L3 | manual | 建立/恢復 Checkpoint 時 |
| `project-protocols-decision-log.md` | L3 | manual | 每個 Step 完成後寫 Decision Log 時 |
| `project-protocols-memory.md` | L3 | manual | 寫 outbox reply 時（更新 memory） |
| `project-protocols-record-write.md` | L3 | manual | 寫入 ProjectRecord 遇到問題時 |
| `project-protocols-format.md` | L3 | manual | 寫 outbox reply 前（確認格式） |
| `project-protocols-error-handling.md` | L3 | manual | 遇到 error 時 |
| `project-protocols-size-rules.md` | L3 | manual | 任務太大 / 怕 timeout 時 |
| `project-protocols-shell-policy.md` | L3 | manual | 想用 shell 前 |
| `role-execution.md` | L3 | manual | **評估前必讀**（測試驗證/FAIL標記） |
| `role-constraints.md` | L3 | manual | 評分時（Checklist/評分細則/循環限制） |
| `domain-knowledge-evaluation-criteria.md` | L3 | manual | 評分計算時 |
| `deterministic-first.md` | L2 | always | Deterministic-First 原則（自動載入） |
| `anti-amnesia.md` | L1 | always | 防失憶規則（自動載入） |
