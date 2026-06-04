---
inclusion: manual
description: Generator 工作流程細則（L3 - 手動載入）— 啟動 / Checkpoint / 格式 / ProjectRecord 寫入 / 記憶
---

# Generator 工作流程細則

> 本文件係 L3（manual）。Generator 執行任務時先 `read_file` 載入。
> 由 `00-index.md`（L1）瘦身搬出，內容不變。

## 啟動流程
1. 先讀取 `./ProjectRecord/active-project.md` → 確認當前 Project 名稱（例如 `ProjectExample`）
2. 讀 `./ProjectRecord/{active-project}/inbox/generator/` → 取得任務計劃
3. **建立 Checkpoint 文件**（見下方 Checkpoint 規則）
4. 自我評估 → 確認有能力完成
5. 確認 Task 嘅 Test Criteria（從 Planner 嘅計劃取得）
6. 生成代碼 + 對應 Unit Test → 寫到 `./ProjectRecord/{active-project}/output/`
7. **每完成一個文件 → 更新 Checkpoint 執行記錄**
8. **本地驗證 test 可以 pass**（如果環境允許）
9. **嚴格按照 `./ProjectRecord/templates/assignment-reply-template.md` 格式**寫完成報告到 `./ProjectRecord/{active-project}/outbox/generator/`
10. **更新 Checkpoint Status → completed，重命名文件**

## Checkpoint 規則（必須遵守，零例外）
> 每個 Assignment 必須有一份 Checkpoint 文件，記錄計劃、中間步驟、思考過程。

### 文件路徑同命名
- 格式：`checkpoint-A{id}-{agent}-{status}.md`
- 路徑：`./ProjectRecord/{active-project}/checkpoints/generator/`
- 開始時建立：`./ProjectRecord/{active-project}/checkpoints/generator/checkpoint-A{id}-generator-in_progress.md`
- 完成時重命名：`./ProjectRecord/{active-project}/checkpoints/generator/checkpoint-A{id}-generator-completed.md`
- Blocked 時重命名：`./ProjectRecord/{active-project}/checkpoints/generator/checkpoint-A{id}-generator-blocked.md`
- **重命名方法**：用 `smartRelocate` 工具（唔好用 shell command `Remove-Item` + 重新建立）
- Cancelled（斷線）：文件保持 `in_progress`（Main Agent 恢復時可以讀取）

### 寫入時機
1. **開始前**：讀取 `./ProjectRecord/templates/checkpoint-template.md`，填寫「計劃」section
2. **每個實際操作後必須 append 一行到「執行記錄」**（零例外）：
   - 寫文件 → 記錄 `write` + 路徑 + 用途
   - 讀文件 → 記錄 `read` + 路徑 + 目的
   - 跑 shell command → 記錄 `shell` + 完整 command + exit code / output 摘要
   - 做技術決定 → 記錄 `decision` + 內容 + 原因
   - 遇到錯誤 → 記錄 `error` + 錯誤訊息 + 影響
   - 重試 → 記錄 `retry` + 第幾次 + 結果
   - 跑測試 → 記錄 `test` + command + pass/fail 數量
3. **遇到問題/做決定時**：append 到「問題同決策記錄」section
4. **完成時**：填寫「最終狀態」section（含統計）+ 重命名文件
5. **唔記錄 = 任務未完成** — Main Agent 會檢查 checkpoint 嘅執行記錄是否完整

### Checkpoint 寫入失敗處理
- Checkpoint 寫入失敗 → **唔影響主流程**（繼續做嘢）
- 但要喺 outbox reply 嘅「備註」標記：「Checkpoint 寫入失敗」

## 格式一致性規則（必須遵守，零例外）
> 所有寫入 ProjectRecord 嘅文件必須嚴格遵守 `./ProjectRecord/templates/` 入面嘅對應 template。

1. **寫 outbox assignment reply 前**：先讀取 `./ProjectRecord/templates/assignment-reply-template.md`，按格式填寫
2. **寫 blocked 報告前**：同樣用 assignment-reply-template，Status 填 `blocked`
3. **所有欄位必須齊全** — template 入面有嘅欄位唔可以省略（可以填 N/A 但唔可以刪）
4. **唔好自創格式** — 唔好加 template 冇定義嘅 section（除非 template 有「備註」欄位）
5. **格式唔一致 = 任務未完成** — Main Agent 會驗證格式，唔合格會退回重寫
6. **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫 SearchIndex.md。Main Agent 會喺收到 reply 後自行更新。

## 通訊協議
- 先讀取 `./ProjectRecord/active-project.md` 確認當前 Project
- 收件：`./ProjectRecord/{active-project}/inbox/generator/assignment-{id}.md`
- 發件：`./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-completed.md`
- Blocked：`./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-blocked.md`

## ProjectRecord 寫入規則（必須遵守，零例外）
> 🔒 **寫入 ProjectRecord 係任務完成嘅必要條件。寫入失敗 = 任務未完成。**

1. **任務完成 = outbox 寫入成功** — 無論結果係 completed/blocked/failed，都必須成功寫入 `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-{status}.md`（status: completed 或 blocked）
2. **寫入失敗處理**：
   - 第一次失敗 → 重試一次
   - 第二次失敗 → 嘗試用更簡單嘅內容寫入（至少包含 status + 一句話摘要）
   - 第三次失敗 → 向 Main Agent 回報：「ProjectRecord 寫入失敗，需要人工介入」
3. **回報格式**（寫入失敗時）：
   - 喺 console/output 明確輸出：`[ERROR] ProjectRecord 寫入失敗：{原因}`
   - 如果可以寫入其他位置，寫一份 fallback 到 `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-write-failed.md`
4. **唔好靜默失敗** — 寫入失敗絕對唔可以當冇事發生，必須通知 Main Agent 或用戶

## 記憶更新（必須執行，零例外）
完成任務寫 outbox assignment reply 時，**必須同時**更新 Project Memory：
1. 讀取 `./ProjectRecord/{active-project}/memory/generator-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + 結果 + 學到咩）
3. 超過 5 條就刪最舊嘅
4. 如果有新教訓，加到「常見錯誤」或「項目知識」
5. Reply 必須包含欄位：`Memory 已更新：✅/❌`
6. **唔寫 memory = 任務未完成**
