---
inclusion: manual
description: Main Agent 操作細則（L3 - 手動載入）— 自動測試 / 格式 / Checkpoint / Specs / 記憶
---

# Main Agent 操作細則

> 本文件係 L3（manual）。Main Agent 喺執行對應操作時先 `read_file` 載入。
> 由 `00-index.md`（L1）瘦身搬出，內容不變。

---

## 自動測試流程（Main Agent 職責）

### 派 Assignment 俾 Generator 時
1. 確認 Planner 嘅計劃包含 Test Criteria
2. Assignment 明確要求：「必須同時提供 unit test + integration test」
3. 指定 test framework（根據技術棧）
4. 如果任務涉及多個模組/服務互動 → 明確要求 integration test 覆蓋互動點

### 收到 Generator 回覆時
1. 確認 output 包含 test 文件（unit + integration）
2. 如果冇 unit test → 直接退回，唔使經 Evaluator
3. 如果冇 integration test 但任務涉及多模組互動 → 退回要求補充
4. 有 test → 正常派俾 Evaluator

### 派 Assignment 俾 Evaluator 時
1. 明確指示：「請執行 unit test + integration test 並驗證結果」
2. 提供 test 文件路徑
3. 提供 Planner 嘅 Test Criteria 作為對照
4. 如果有 integration test → 確認測試環境配置正確

---

## 格式一致性規則（必須遵守，零例外）
> 所有寫入 ProjectRecord 嘅文件必須嚴格遵守 `./ProjectRecord/templates/` 入面嘅對應 template。

### 自己寫 assignment 時
1. **先讀取 `./ProjectRecord/active-project.md`** → 確認當前 Project 名稱
2. **寫 inbox assignment 前**：先讀取 `./ProjectRecord/templates/assignment-template.md`，按格式填寫
3. **寫 conversation-log 前**：先讀取 `./ProjectRecord/templates/conversation-log-entry-template.md`，按格式填寫
4. **寫入後更新 SearchIndex**：append 一行到 `./ProjectRecord/{active-project}/SearchIndex.md`，格式參照 `./ProjectRecord/templates/search-index-entry-template.md`

### 驗證 Agent 回覆時
1. **所有 Agent assignment reply**：對照 `./ProjectRecord/templates/assignment-reply-template.md` 驗證
3. **缺少必要欄位** → 退回 Agent 重寫（計入重試次數）
4. **格式正確** → 繼續流程
5. **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫 SearchIndex.md。Main Agent 收到任何 inbox/outbox 寫入後，自行 append 對應記錄到 SearchIndex。

### 搵記錄時
1. **先讀 `./ProjectRecord/{active-project}/SearchIndex.md`** — 用關鍵字/Task ID/Agent/Status 篩選
2. **只讀取對應嘅文件** — 唔好逐個 inbox/outbox 文件讀取
3. **SearchIndex 唔存在或損壞** → 重建（掃描所有 inbox/outbox frontmatter）

---

## Checkpoint 恢復規則（斷線/重啟後）

### 恢復流程
1. 掃描 `./ProjectRecord/{active-project}/checkpoints/main-agent/` 目錄
2. 搵所有 `*-in_progress.md` → 呢啲係未完成嘅調度
3. 掃描對應嘅 `./ProjectRecord/{active-project}/checkpoints/{sub-agent}/` → 了解執行進度
4. 對比實際文件系統（output/ + outbox/）確認真實狀態
5. 決定：繼續（重新派 Sub Agent）/ 補寫 reply / 派 Evaluator

### 判斷邏輯
| Checkpoint 狀態 | output/ 有文件？ | outbox/ 有 reply？ | 動作 |
|----------------|-----------------|-------------------|------|
| in_progress | ❌ | ❌ | 重新派 Sub Agent |
| in_progress | ✅（部分） | ❌ | 讀 checkpoint 了解缺咩 → 重新派 |
| in_progress | ✅（完整） | ❌ | 補寫 outbox reply → 派 Evaluator |
| in_progress | ✅ | ✅ | 更新 checkpoint → completed |

### Main Agent 自己嘅 Checkpoint 規則
> Main Agent 每次調度（派 assignment / 收 reply / 做決定）都要記錄 checkpoint。
> **每個實際操作後必須 append 一行到「執行記錄」**（零例外）。唔記錄 = 任務未完成。

1. **派 Assignment 前**：建立 `./ProjectRecord/{active-project}/checkpoints/main-agent/checkpoint-A{id}-main-agent-in_progress.md`
   - 讀取 `./ProjectRecord/templates/checkpoint-template.md`，按格式填寫「計劃」section
2. **每個實際操作後必須 append 一行到「執行記錄」**：
   - 寫 inbox assignment → 記錄 `write` + 路徑 + 派俾邊個 Agent
   - 調用 Sub Agent → 記錄 `shell` 或 `decision` + 調用方法（CLI / invoke_sub_agent）
   - 收到 Sub Agent reply → 記錄 `read` + outbox 路徑 + verdict/status
   - 做調度決定（PASS/FAIL/REPLAN）→ 記錄 `decision` + 決定內容 + 原因
   - 更新 tasks.md → 記錄 `write` + 更新咗邊個 Task status
   - 更新 SearchIndex → 記錄 `write` + 加咗幾行
   - 遇到錯誤 → 記錄 `error` + 錯誤訊息
   - 重試 → 記錄 `retry` + 第幾次 + 結果
3. **遇到問題/做決定時**：append 到「問題同決策記錄」section
4. **Task 完成（PASS）後**：填寫「最終狀態」section（含統計）+ 重命名為 `checkpoint-A{id}-main-agent-completed.md`
5. **Checkpoint 路徑統一用 active-project**：`./ProjectRecord/{active-project}/checkpoints/main-agent/`

### Checkpoints 目錄結構（所有 Project 通用）
```
./ProjectRecord/{active-project}/checkpoints/
├── main-agent/
│   ├── checkpoint-A001-main-agent-completed.md
│   ├── checkpoint-A002-main-agent-completed.md
│   └── checkpoint-A008-main-agent-in_progress.md   ← 斷線後恢復入口
├── planner/
│   └── checkpoint-A001-planner-completed.md
├── generator/
│   ├── checkpoint-A002-generator-completed.md
│   └── checkpoint-A008-generator-in_progress.md    ← 了解執行進度
└── evaluator/
    └── checkpoint-A003-evaluator-completed.md
```

---

## UserConfig / UserDocument 放置規則

### Project 專屬（根據 active-project 決定路徑）
- Session 記錄 → `./ProjectRecord/{active-project}/UserConfig/sessions/`
- 用戶文件 → `./ProjectRecord/{active-project}/UserDocument/`

### 跨 Project 通用
- 通用 Session → `./UserConfig/sessions/`（唔屬於特定 Project 嘅對話）
- 通用用戶文件 → `./UserDocument/`（跨 Project 嘅文件）

### 路徑決定流程
1. 讀取 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. 如果操作屬於特定 Project → 寫入 `./ProjectRecord/{current}/UserConfig/` 或 `UserDocument/`
3. 如果操作係通用/跨 Project → 寫入頂層 `./UserConfig/` 或 `./UserDocument/`

---

## Specs 管理規則

### 啟動時讀取
1. 確認當前 Project 後，檢查 `./ProjectRecord/{active-project}/specs/` 是否存在
2. 如果存在且有文件 → 讀取所有 `.md` 文件（requirements.md、design.md、tasks.md）
3. 用 Specs 內容作為 Assignment 嘅 context（TaskRef、TaskID 從 tasks.md 取得）

### 用戶要求建立 Specs 時
1. 開新 Assignment 派俾 Planner，Type: `plan-request`
2. Assignment 需求：「根據用戶需求，產出 requirements.md、design.md、tasks.md」
3. Planner 完成後，Main Agent 將產出寫入 `./ProjectRecord/{active-project}/specs/`
4. Specs 文件格式必須參照 `./ProjectRecord/templates/specs/` 入面嘅 template

### Specs 路徑
```
./ProjectRecord/{active-project}/specs/
├── requirements.md
├── design.md
└── tasks.md
```

### TaskID 格式
- `{active-project}/Task-{number}`
- 例如：`ProjectCRUDGenerator/Task-2`
- 對應 `./ProjectRecord/{active-project}/specs/tasks.md` 入面嘅 Task 2

---

## 記憶更新 + 驗證（必須執行，零例外）

### 自己嘅記憶
每次完成一輪調度（用戶需求 → 交付）後，**必須**更新 Project Memory：
1. 讀取 `./ProjectRecord/{active-project}/memory/main-agent-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + 結果 + 備註）
3. 超過 5 條就刪最舊嘅
4. 如果有新發現，加到「調度經驗」或「項目知識」
5. **唔寫 memory = 任務未完成**

### 驗證 Sub Agent 記憶
收到任何 Agent 嘅 reply 後，檢查 `Memory 已更新` 欄位：
- ✅ → 正常繼續
- ❌ 或缺少 → 從 reply 內容提煉教訓，寫入 `./ProjectRecord/{active-project}/memory/{agent}-memory.md`
