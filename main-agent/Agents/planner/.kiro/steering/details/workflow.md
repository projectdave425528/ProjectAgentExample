---
inclusion: manual
description: Planner 工作流程細則（L3 - 手動載入）— 可測試性設計 / 啟動 / Checkpoint / Specs / 格式 / ProjectRecord 寫入 / 記憶
---

# Planner 工作流程細則

> 本文件係 L3（manual）。Planner 執行任務時先 `read_file` 載入。
> 由 `00-index.md`（L1）瘦身搬出，內容不變。

## 可測試性設計規則（必須遵守）

### 任務拆分原則
1. **單一職責** — 每個 Task 只做一件事，方便寫獨立 test
2. **明確 Input/Output** — 每個 Task 嘅 acceptance criteria 必須定義：
   - Input：咩數據 / 參數進去
   - Output：期望咩結果出嚟
   - Edge Cases：至少列 2 個邊界情況
3. **無隱藏依賴** — Task 之間嘅依賴要用 interface / abstraction 隔開
4. **可 Mock 嘅外部依賴** — 涉及 DB / API / File 嘅 Task，設計時要預留 interface 方便 mock

### 任務清單格式（新增 Test Criteria 欄）
```markdown
| # | 任務 | 依賴 | Acceptance Criteria | Test Criteria |
|---|------|------|---------------------|---------------|
| 1 | ... | 無 | ... | 列出可驗證嘅 test case |
| 2 | ... | #1 | ... | 列出可驗證嘅 test case |
```

### Test Criteria 寫法
每個 Task 嘅 Test Criteria 必須包含：
- **Happy Path**: 正常情況下嘅預期行為（至少 1 個）
- **Error Path**: 錯誤情況下嘅預期行為（至少 1 個）
- **Edge Case**: 邊界情況（至少 1 個）
- **Integration Point**: 同其他模組/服務嘅互動驗證（如適用，至少 1 個）

### Integration Testing 設計規則
> 當任務涉及多個模組、服務、或外部系統互動時，必須設計 Integration Test。

1. **識別 Integration Point** — 每個 Task 列出同邊啲模組/服務有互動
2. **定義 Integration Test Scenario** — 描述端到端嘅數據流同預期行為
3. **環境要求** — 列出 integration test 需要嘅環境（test DB、mock server、etc.）
4. **隔離策略** — 定義點樣隔離外部依賴（test container、in-memory DB、mock API）
5. **任務清單格式加入 Integration 欄**：

```markdown
| # | 任務 | 依賴 | Acceptance Criteria | Test Criteria | Integration Points |
|---|------|------|---------------------|---------------|-------------------|
| 1 | ... | 無 | ... | ... | 列出同邊啲模組互動 |
```

### 架構設計要求
- 業務邏輯同 infrastructure（DB / API / File）必須分層
- 每層之間用 interface 連接（方便 mock）
- 推薦模式：Controller → Service（可 test）→ Repository（interface）→ DB

## 啟動流程
1. 先讀取 `./ProjectRecord/active-project.md` → 確認當前 Project 名稱（例如 `ProjectExample`）
2. 讀 `./ProjectRecord/{active-project}/inbox/planner/` → 取得需求或反饋
3. **建立 Checkpoint 文件**（見下方 Checkpoint 規則）
4. 分析需求 → 設計方案
5. **每完成一個主要步驟 → 更新 Checkpoint 執行記錄**
6. **嚴格按照 `./ProjectRecord/templates/assignment-reply-template.md` 格式**寫結果到 `./ProjectRecord/{active-project}/outbox/planner/`
7. **更新 Checkpoint Status → completed，重命名文件**

## Checkpoint 規則（必須遵守，零例外）
> 每個 Assignment 必須有一份 Checkpoint 文件，記錄計劃、中間步驟、思考過程。

### 文件路徑同命名
- 格式：`checkpoint-A{id}-{agent}-{status}.md`
- 路徑：`./ProjectRecord/{active-project}/checkpoints/planner/`
- 開始時建立：`./ProjectRecord/{active-project}/checkpoints/planner/checkpoint-A{id}-planner-in_progress.md`
- 完成時重命名：`./ProjectRecord/{active-project}/checkpoints/planner/checkpoint-A{id}-planner-completed.md`
- Blocked/Escalation 時重命名：`./ProjectRecord/{active-project}/checkpoints/planner/checkpoint-A{id}-planner-blocked.md`
- **重命名方法**：用 `smartRelocate` 工具（唔好用 shell command `Remove-Item` + 重新建立）

### 寫入時機
1. **開始前**：讀取 `./ProjectRecord/templates/checkpoint-template.md`，填寫「計劃」section
2. **每個實際操作後必須 append 一行到「執行記錄」**（零例外）：
   - 寫文件 → 記錄 `write` + 路徑 + 用途
   - 讀文件 → 記錄 `read` + 路徑 + 目的
   - 跑 shell command → 記錄 `shell` + 完整 command + exit code / output 摘要
   - 做技術決定 → 記錄 `decision` + 內容 + 原因
   - 遇到錯誤 → 記錄 `error` + 錯誤訊息 + 影響
   - 重試 → 記錄 `retry` + 第幾次 + 結果
3. **遇到問題/做決定時**：append 到「問題同決策記錄」section
4. **完成時**：填寫「最終狀態」section（含統計）+ 重命名文件
5. **唔記錄 = 任務未完成** — Main Agent 會檢查 checkpoint 嘅執行記錄是否完整

### Checkpoint 寫入失敗處理
- Checkpoint 寫入失敗 → **唔影響主流程**（繼續做嘢）
- 但要喺 outbox reply 嘅「備註」標記：「Checkpoint 寫入失敗」

## Specs 產出規則

### 當 Assignment Type 包含 Specs 產出要求時
1. 讀取 `./ProjectRecord/templates/specs/` 入面嘅 template（requirements-template.md、design-template.md、tasks-template.md）
2. 按 template 格式產出三份文件
3. 將產出寫入 `./ProjectRecord/{active-project}/specs/`：
   - `./ProjectRecord/{active-project}/specs/requirements.md`
   - `./ProjectRecord/{active-project}/specs/design.md`
   - `./ProjectRecord/{active-project}/specs/tasks.md`
4. 同時寫 outbox assignment reply（AssignmentStatus: completed）
5. Reply 嘅「結果」section 列出已產出嘅 Specs 文件路徑

## 格式一致性規則（必須遵守，零例外）
> 所有寫入 ProjectRecord 嘅文件必須嚴格遵守 `./ProjectRecord/templates/` 入面嘅對應 template。

1. **寫 outbox assignment reply 前**：先讀取 `./ProjectRecord/templates/assignment-reply-template.md`，按格式填寫
2. **所有欄位必須齊全** — template 入面有嘅欄位唔可以省略（可以填 N/A 但唔可以刪）
3. **唔好自創格式** — 唔好加 template 冇定義嘅 section（除非 template 有「備註」欄位）
4. **格式唔一致 = 任務未完成** — Main Agent 會驗證格式，唔合格會退回重寫
5. **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫 SearchIndex.md。Main Agent 會喺收到 reply 後自行更新。

## 通訊協議
- 先讀取 `./ProjectRecord/active-project.md` 確認當前 Project
- 收件：`./ProjectRecord/{active-project}/inbox/planner/assignment-{id}.md`
- 發件（完成）：`./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`
- 發件（上報）：`./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-escalation.md`

## ProjectRecord 寫入規則（必須遵守，零例外）
> 🔒 **寫入 ProjectRecord 係任務完成嘅必要條件。寫入失敗 = 任務未完成。**

1. **任務完成 = outbox 寫入成功** — 無論結果係 completed/blocked/failed，都必須成功寫入 `./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-{status}.md`
2. **寫入失敗處理**：
   - 第一次失敗 → 重試一次
   - 第二次失敗 → 嘗試用更簡單嘅內容寫入（至少包含 status + 一句話摘要）
   - 第三次失敗 → 向 Main Agent 回報：「ProjectRecord 寫入失敗，需要人工介入」
3. **回報格式**（寫入失敗時）：
   - 喺 console/output 明確輸出：`[ERROR] ProjectRecord 寫入失敗：{原因}`
   - 如果可以寫入其他位置，寫一份 fallback 到 `./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-write-failed.md`
4. **唔好靜默失敗** — 寫入失敗絕對唔可以當冇事發生，必須通知 Main Agent 或用戶

## 記憶更新（必須執行，零例外）
完成任務寫 outbox assignment reply 時，**必須同時**更新 Project Memory：
1. 讀取 `./ProjectRecord/{active-project}/memory/planner-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + 結果 + 學到咩）
3. 超過 5 條就刪最舊嘅
4. 如果有新發現，加到「常見問題」或「項目知識」
5. Reply 必須包含欄位：`Memory 已更新：✅/❌`
6. **唔寫 memory = 任務未完成**
