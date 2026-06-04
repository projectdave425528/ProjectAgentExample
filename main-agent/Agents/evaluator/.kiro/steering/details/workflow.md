---
inclusion: manual
description: Evaluator 工作流程細則（L3 - 手動載入）— 自動測試驗證 / 啟動 / FAIL 標記 / Checkpoint / 格式 / ProjectRecord 寫入 / 記憶
---

# Evaluator 工作流程細則

> 本文件係 L3（manual）。Evaluator 執行評估時先 `read_file` 載入。
> 由 `00-index.md`（L1）瘦身搬出，內容不變。

## 自動測試驗證規則（必須遵守，零例外）

### 測試執行流程
1. **確認 test 文件存在** — 冇 test 文件 → 直接 FAIL（分數上限 50）
2. **分析 test 覆蓋度** — 對照 Planner 嘅 Test Criteria 逐項檢查
3. **確認 Integration Test 存在**（如果 Task 涉及多模組互動）：
   - 有 integration test → 正常評分
   - 冇 integration test 但應該有 → 扣分（分數上限 70），feedback 要求補充
4. **嘗試執行 test**（如果環境允許）：
   - Unit test 全部 PASS → 正常評分
   - Integration test 全部 PASS → 加分
   - 有 FAIL → 記錄失敗嘅 test，扣分
   - 無法執行（缺少依賴）→ 靜態分析 test 品質
5. **評估 test 品質** — 唔係有 test 就得，test 本身要有意義

### Integration Test 驗證標準
| # | 檢查項 | 判斷標準 |
|---|--------|----------|
| I1 | Integration test 存在 | 涉及多模組互動嘅 Task 必須有 |
| I2 | 測試真實互動 | 唔係用 mock 代替所有依賴（至少有一層真實互動） |
| I3 | 數據流完整 | 測試覆蓋 input → processing → output 全流程 |
| I4 | Setup/Teardown | 有正確嘅 test data 準備同清理 |
| I5 | 環境隔離 | 唔影響 production data，用 test 環境 |

### 可測試性評分（15%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| T1 | Test 存在 | 5% | 每個 public method 都有對應 test |
| T2 | Test 覆蓋度 | 4% | Happy + Error + Edge case 都有 |
| T3 | Test 獨立性 | 3% | 唔依賴執行順序、外部服務 |
| T4 | Test 可讀性 | 3% | 命名清晰、AAA pattern |

### Critical Test 問題（發現即 FAIL）
| 問題 | 原因 |
|------|------|
| 完全冇 test | 違反基本要求 |
| Test 依賴真實 DB / API | 唔可重複、唔可獨立 |
| Test 永遠 pass（冇 assert） | 假 test，冇意義 |
| Test 測試 implementation 而唔係 behavior | 脆弱 test，改 code 就爛 |

## 啟動流程
1. 先讀取 `./ProjectRecord/active-project.md` → 確認當前 Project 名稱（例如 `ProjectExample`）
2. 讀 `./ProjectRecord/{active-project}/inbox/evaluator/` → 取得代碼 + 原始計劃
3. **建立 Checkpoint 文件**（見下方 Checkpoint 規則）
4. 逐項評估 → 計算分數
5. **每完成一個評估類別 → 更新 Checkpoint 執行記錄**
6. **嚴格按照 `./ProjectRecord/templates/assignment-reply-template.md` 格式**寫 verdict 到 `./ProjectRecord/{active-project}/outbox/evaluator/`
7. **如果 Verdict = FAIL → 執行 Output Folder 標記**（見下方 FAIL Output 標記規則）
8. **更新 Checkpoint Status → completed，重命名文件**

## FAIL Output 標記規則（必須遵守，零例外）
> 當 Verdict 為 FAIL 時，必須將對應嘅 output folder 重命名加入 `-FAILED` 標記，方便識別。

### 重命名規則
- 原路徑：`./ProjectRecord/{active-project}/output/assignment-{id}/`
- FAIL 後重命名為：`./ProjectRecord/{active-project}/output/assignment-{id}-FAILED/`
- 如果同一個 Assignment 第 2 次 FAIL：`assignment-{id}-FAILED-2/`
- 如果同一個 Assignment 第 3 次 FAIL：`assignment-{id}-FAILED-3/`

### 執行時機
- 寫完 verdict（verdict-fail）到 outbox 之後
- 重命名 output folder 之後

### 重命名失敗處理
- 重命名失敗 → 唔影響主流程，喺 verdict 備註標記「Output folder 重命名失敗」
- 如果 folder 唔存在（Generator 冇寫 output）→ 跳過，唔報錯

## Checkpoint 規則（必須遵守，零例外）
> 每個 Assignment 必須有一份 Checkpoint 文件，記錄計劃、中間步驟、思考過程。

### 文件路徑同命名
- 格式：`checkpoint-A{id}-{agent}-{status}.md`
- 路徑：`./ProjectRecord/{active-project}/checkpoints/evaluator/`
- 開始時建立：`./ProjectRecord/{active-project}/checkpoints/evaluator/checkpoint-A{id}-evaluator-in_progress.md`
- 完成時重命名：`./ProjectRecord/{active-project}/checkpoints/evaluator/checkpoint-A{id}-evaluator-completed.md`
- Blocked 時重命名：`./ProjectRecord/{active-project}/checkpoints/evaluator/checkpoint-A{id}-evaluator-blocked.md`
- **重命名方法**：用 `smartRelocate` 工具（唔好用 shell command `Remove-Item` + 重新建立）

### 寫入時機
1. **開始前**：讀取 `./ProjectRecord/templates/checkpoint-template.md`，填寫「計劃」section
2. **每個實際操作後必須 append 一行到「執行記錄」**（零例外）：
   - 讀文件 → 記錄 `read` + 路徑 + 目的
   - 做評估判斷 → 記錄 `validate` + 驗證咩 + 結果
   - 做技術決定 → 記錄 `decision` + 內容 + 原因
   - 遇到錯誤 → 記錄 `error` + 錯誤訊息 + 影響
   - 跑 shell command → 記錄 `shell` + 完整 command + exit code / output 摘要
   - 跑測試 → 記錄 `test` + command + pass/fail 數量
   - 寫 verdict → 記錄 `write` + 路徑
   - 重命名 output folder → 記錄 `rename` + 原路徑 → 新路徑
3. **遇到問題/做決定時**：append 到「問題同決策記錄」section
4. **完成時**：填寫「最終狀態」section（含統計）+ 重命名文件
5. **唔記錄 = 任務未完成** — Main Agent 會檢查 checkpoint 嘅執行記錄是否完整

### Checkpoint 寫入失敗處理
- Checkpoint 寫入失敗 → **唔影響主流程**（繼續做嘢）
- 但要喺 outbox reply 嘅「備註」標記：「Checkpoint 寫入失敗」

## 格式一致性規則（必須遵守，零例外）
> 所有寫入 ProjectRecord 嘅文件必須嚴格遵守 `./ProjectRecord/templates/` 入面嘅對應 template。

1. **寫 verdict 前**：先讀取 `./ProjectRecord/templates/assignment-reply-template.md`，按格式填寫（AssignmentStatus 用 verdict-pass / verdict-fail / verdict-replan）
2. **所有欄位必須齊全** — template 入面有嘅欄位唔可以省略（分數必須填數字，唔可以填 N/A）
3. **唔好自創格式** — 唔好加 template 冇定義嘅 section
4. **格式唔一致 = 任務未完成** — Main Agent 會驗證格式，唔合格會退回重寫
5. **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫 SearchIndex.md。Main Agent 會喺收到 reply 後自行更新。

## 通訊協議
- 先讀取 `./ProjectRecord/active-project.md` 確認當前 Project
- 收件：`./ProjectRecord/{active-project}/inbox/evaluator/assignment-{id}.md`（含代碼路徑 + 計劃）
- 發件：`./ProjectRecord/{active-project}/outbox/evaluator/assignment-{id}-reply-verdict.md`
- Blocked：`./ProjectRecord/{active-project}/outbox/evaluator/assignment-{id}-reply-blocked.md`

## ProjectRecord 寫入規則（必須遵守，零例外）
> 🔒 **寫入 ProjectRecord 係任務完成嘅必要條件。寫入失敗 = 任務未完成。**

1. **任務完成 = outbox 寫入成功** — 無論結果係 PASS/FAIL/REPLAN，都必須成功寫入 `./ProjectRecord/{active-project}/outbox/evaluator/assignment-{id}-reply-verdict.md`
2. **寫入失敗處理**：
   - 第一次失敗 → 重試一次
   - 第二次失敗 → 嘗試用更簡單嘅內容寫入（至少包含 verdict + 總分）
   - 第三次失敗 → 向 Main Agent 回報：「ProjectRecord 寫入失敗，需要人工介入」
3. **回報格式**（寫入失敗時）：
   - 喺 console/output 明確輸出：`[ERROR] ProjectRecord 寫入失敗：{原因}`
   - 如果可以寫入其他位置，寫一份 fallback 到 `./ProjectRecord/{active-project}/outbox/evaluator/assignment-{id}-write-failed.md`
4. **唔好靜默失敗** — 寫入失敗絕對唔可以當冇事發生，必須通知 Main Agent 或用戶

## 記憶更新（必須執行，零例外）
完成任務寫 outbox assignment reply 時，**必須同時**更新 Project Memory：
1. 讀取 `./ProjectRecord/{active-project}/memory/evaluator-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + Verdict + 主要問題）
3. 超過 5 條就刪最舊嘅
4. 如果有新發現，加到「評估經驗」或「項目標準」
5. Reply 必須包含欄位：`Memory 已更新：✅/❌`
6. **唔寫 memory = 任務未完成**
