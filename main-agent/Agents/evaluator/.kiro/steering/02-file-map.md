---
inclusion: always
description: Evaluator 文件導航地圖（L1 - 永遠載入）— 工具權限 + 文件清單 + 使用時機 + 點搵 Project 內容
---

# Evaluator 文件導航地圖

> 呢份係「目錄」：話你知有咩文件、幾時讀邊份、點搵 Project 資料。

## 我嘅工具權限
| 工具 | 用途 |
|------|------|
| `fs_read` | 讀文件（inbox、代碼、計劃、test） |
| `fs_write` | 寫文件（verdict、checkpoint、重命名 FAIL output） |
| `execute_bash` | 跑 shell（執行 test 驗證）— 先睇 `shared/avoid-shell.md` |
| ❌ 唔可以改代碼 | 只可評分 + 反饋 |

## 我嘅 Steering 文件清單（幾時讀）
| 文件 | 層級 | 幾時讀 |
|------|------|--------|
| `00-index.md` | L1 always | 身份 + 核心規則 + Verdict 標準（已自動載入） |
| `01-comm-system.md` | L2 always | 收發協議（已自動載入） |
| `02-file-map.md` | L1 always | 本文件（導航） |
| `details/workflow.md` | L3 | **評估前必讀**（測試驗證/啟動/FAIL標記/Checkpoint/格式/寫入/記憶） |
| `details/role-detail.md` | L3 | 評分時（完整 Checklist/評分細則/Critical 問題/循環限制） |
| `details/output-format.md` | L3 | 寫 PASS/FAIL/REPLAN 反饋時 |
| `shared/avoid-shell.md` | L3 | 想用 shell 前 |
| `shared/error-handling.md` | L3 | 遇到 error 時 |
| `shared/context-management.md` | L3 | 任務太大 / 怕 timeout 時 |

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **攞評估任務**：`./ProjectRecord/{active-project}/inbox/evaluator/assignment-{id}.md`（含代碼路徑 + 計劃）
3. **睇要評嘅代碼**：`./ProjectRecord/{active-project}/output/assignment-{id}/`
4. **睇原始計劃**：`./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`（對照 Test Criteria）
5. **搵歷史記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選）
6. **我嘅記憶**：`./ProjectRecord/{active-project}/memory/evaluator-memory.md`

## 我輸出去邊
- **Verdict** → `./ProjectRecord/{active-project}/outbox/evaluator/assignment-{id}-reply-verdict.md`
- **FAIL 時** → 重命名 `output/assignment-{id}/` 為 `output/assignment-{id}-FAILED/`
- **Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/evaluator/`
