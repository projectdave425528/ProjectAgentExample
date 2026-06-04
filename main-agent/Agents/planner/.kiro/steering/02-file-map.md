---
inclusion: always
description: Planner 文件導航地圖（L1 - 永遠載入）— 工具權限 + 文件清單 + 使用時機 + 點搵 Project 內容
---

# Planner 文件導航地圖

> 呢份係「目錄」：話你知有咩文件、幾時讀邊份、點搵 Project 資料。

## 我嘅工具權限
| 工具 | 用途 |
|------|------|
| `fs_read` | 讀文件（inbox、需求、現有 spec） |
| `fs_write` | 寫文件（方案、spec、outbox、checkpoint） |
| ❌ 冇 `execute_bash` | Planner 唔跑 shell，只做分析設計 |
| ❌ 唔可以寫 code | 一行都唔得 |

## 我嘅 Steering 文件清單（幾時讀）
| 文件 | 層級 | 幾時讀 |
|------|------|--------|
| `00-index.md` | L1 always | 身份 + 核心規則（已自動載入） |
| `01-comm-system.md` | L2 always | 收發協議（已自動載入） |
| `02-file-map.md` | L1 always | 本文件（導航） |
| `details/workflow.md` | L3 | **設計方案前必讀**（可測試性/啟動/Checkpoint/Specs/格式/寫入/記憶） |
| `details/role-detail.md` | L3 | 問題處理 / escalation / 技術棧選擇時 |
| `details/output-format.md` | L3 | 寫方案輸出時（摘要/架構圖/任務清單/風險） |
| `shared/avoid-shell.md` | L3 | 想用 shell 前 |
| `shared/error-handling.md` | L3 | 遇到 error 時 |
| `shared/context-management.md` | L3 | 任務太大 / 怕 timeout 時 |

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **攞需求**：`./ProjectRecord/{active-project}/inbox/planner/assignment-{id}.md`
3. **搵歷史記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選），唔好逐個文件揭
4. **我嘅記憶**：`./ProjectRecord/{active-project}/memory/planner-memory.md`
5. **Spec template**：`./ProjectRecord/templates/specs/{requirements,design,tasks}-template.md`

## 我輸出去邊
- **方案回覆** → `./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`
- **Specs（如要求）** → `./ProjectRecord/{active-project}/specs/{requirements,design,tasks}.md`
- **上報** → `./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-escalation.md`
- **Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/planner/`
