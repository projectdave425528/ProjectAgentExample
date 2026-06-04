---
inclusion: always
description: Main Agent 文件導航地圖（L1 - 永遠載入）— 工具權限 + 文件清單 + 使用時機 + 點搵 Project 內容
---

# Main Agent 文件導航地圖

> 呢份係「目錄」：話你知有咩文件、幾時讀邊份、點搵 Project 資料。

## 我嘅角色同工具
- **角色**：Orchestrator（調度），唔自己寫 code / 改 code / 跑 test
- **工具**：可讀寫文件、跑 shell（Git / 確認環境 / 取系統時間）— 先睇 `shared/avoid-shell.md`
- **調用 Sub Agent**：Kiro CLI 優先，唔得就用 invoke_sub_agent（詳見 `01-comm-system.md`）

## 我嘅 Steering 文件清單（幾時讀）
| 文件 | 層級 | 幾時讀 |
|------|------|--------|
| `00-index.md` | L1 always | 身份 + 核心規則 + 啟動流程（已自動載入） |
| `01-comm-system.md` | L2 always | 調用 Sub Agent / 收發 / ID 規則（已自動載入） |
| `02-file-map.md` | L1 always | 本文件（導航） |
| `details/operations.md` | L3 | **派工 / 收 reply / 寫記錄前讀**（自動測試/格式/Checkpoint/Specs/記憶/UserConfig） |
| `details/comm-detail.md` | L3 | 要完整目錄結構圖 / Message 格式時 |
| `details/role-detail.md` | L3 | 處理 blocked / 循環限制時 |
| `details/git-rules.md` | L3 | Git commit / push 前 |
| `shared/avoid-shell.md` | L3 | 想用 shell 前 |
| `shared/error-handling.md` | L3 | 遇到 error 時 |
| `shared/context-management.md` | L3 | 調度大任務 / 怕 timeout 時 |

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **搵記錄（最重要）**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`，用關鍵字/ID/Agent/Status 篩選 → 只讀對應文件，唔好逐個揭
3. **斷線恢復**：掃 `./ProjectRecord/{active-project}/checkpoints/*/` 搵 `*-in_progress.md`
4. **收 Sub Agent reply**：`./ProjectRecord/{active-project}/outbox/{agent}/`
5. **Spec（如有）**：`./ProjectRecord/{active-project}/specs/{requirements,design,tasks}.md`
6. **各 Agent 記憶**：`./ProjectRecord/{active-project}/memory/{agent}-memory.md`
7. **共用 template**：`./ProjectRecord/templates/`（assignment / reply / checkpoint / search-index / verdict）

## 我寫去邊
- **派工** → `./ProjectRecord/{active-project}/inbox/{agent}/assignment-{id}.md`
- **對話記錄** → `./ProjectRecord/{active-project}/conversation-log.md`（append）
- **搜尋索引** → `./ProjectRecord/{active-project}/SearchIndex.md`（每次寫入後 append）
- **我嘅 Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/main-agent/`
- **交付成品** → `./ProjectRecord/{active-project}/output/`
- **Session / 用戶文件** → Project 專屬用 `{active-project}/UserConfig|UserDocument/`；跨 Project 用頂層

## Sub Agent 速查
| Agent | 派俾佢做 | 佢寫去 |
|-------|---------|--------|
| `planner` | 需求分析 / 架構 / 任務拆分 / Specs | `outbox/planner/` |
| `generator` | 按計劃寫 code + test | `output/` + `outbox/generator/` |
| `evaluator` | 跑 test + 評分（PASS/FAIL/REPLAN） | `outbox/evaluator/` |
