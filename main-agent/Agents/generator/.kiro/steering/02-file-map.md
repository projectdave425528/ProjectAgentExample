---
inclusion: always
description: Generator 文件導航地圖（L1 - 永遠載入）— 工具權限 + 文件清單 + 使用時機 + 點搵 Project 內容
---

# Generator 文件導航地圖

> 呢份係「目錄」：話你知有咩文件、幾時讀邊份、點搵 Project 資料。

## 我嘅工具權限
| 工具 | 用途 |
|------|------|
| `fs_read` | 讀文件（inbox、計劃、現有 code） |
| `fs_write` | 寫文件（生成 code、寫 outbox、checkpoint） |
| `execute_bash` | 跑 shell（裝 dependency、本地驗證 test）— 先睇 `shared/avoid-shell.md` |

## 我嘅 Steering 文件清單（幾時讀）
| 文件 | 層級 | 幾時讀 |
|------|------|--------|
| `00-index.md` | L1 always | 身份 + 核心規則（已自動載入） |
| `01-comm-system.md` | L2 always | 收發協議（已自動載入） |
| `02-file-map.md` | L1 always | 本文件（導航） |
| `details/test-rules.md` | L3 | **生成代碼前必讀**（測試規則） |
| `details/workflow.md` | L3 | 開始任務時（啟動/Checkpoint/格式/寫入/記憶） |
| `details/code-standards.md` | L3 | 寫 code 時（命名/安全/錯誤處理規範） |
| `details/role-detail.md` | L3 | 自我評估 / 自學 / 報 blocked 時 |
| `details/output-format.md` | L3 | 寫完成報告時 |
| `shared/avoid-shell.md` | L3 | 想用 shell 前 |
| `shared/error-handling.md` | L3 | 遇到 error 時 |
| `shared/context-management.md` | L3 | 任務太大 / 怕 timeout 時 |

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **攞任務**：`./ProjectRecord/{active-project}/inbox/generator/assignment-{id}.md`
3. **睇 Planner 計劃**：`./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`
4. **搵歷史記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選），唔好逐個文件揭
5. **我嘅記憶**：`./ProjectRecord/{active-project}/memory/generator-memory.md`
6. **Spec（如有）**：`./ProjectRecord/{active-project}/specs/{requirements,design,tasks}.md`

## 我輸出去邊
- **代碼** → `./ProjectRecord/{active-project}/output/assignment-{id}/`
- **完成報告** → `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-completed.md`
- **Blocked 報告** → `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-blocked.md`
- **Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/generator/`
