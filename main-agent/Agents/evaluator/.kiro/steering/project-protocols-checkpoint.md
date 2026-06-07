---
inclusion: manual
description: Checkpoint 規則（L3 - 建立/命名/寫入時機/恢復）
---

# Checkpoint 規則（必須遵守，零例外）

> 每個 Assignment 必須有一份 Checkpoint 文件，記錄計劃、中間步驟、思考過程。

## 文件路徑同命名
- 格式：`checkpoint-A{id}-evaluator-{status}.md`
- 路徑：`./ProjectRecord/{active-project}/checkpoints/evaluator/`
- 開始時：`checkpoint-A{id}-evaluator-in_progress.md`
- 完成時重命名：`checkpoint-A{id}-evaluator-completed.md`
- Blocked 時重命名：`checkpoint-A{id}-evaluator-blocked.md`
- **重命名方法**：用 `smartRelocate` 工具

## 寫入時機
1. **開始前**：讀取 `./ProjectRecord/templates/checkpoint-template.md`，填寫「計劃」section
2. **每個實際操作後必須 append 一行到「執行記錄」**（零例外）：
   - 讀文件 → `read` + 路徑 + 目的
   - 做評估判斷 → `validate` + 驗證咩 + 結果
   - 做技術決定 → `decision` + 內容 + 原因
   - 遇到錯誤 → `error` + 錯誤訊息 + 影響
   - 跑 shell → `shell` + 完整 command + exit code / output 摘要
   - 跑測試 → `test` + command + pass/fail 數量
   - 寫 verdict → `write` + 路徑
   - 重命名 output folder → `rename` + 原路徑 → 新路徑
3. **遇到問題/做決定時**：append 到「問題同決策記錄」section
4. **完成時**：填寫「最終狀態」section（含統計）+ 重命名文件
5. **唔記錄 = 任務未完成**

## Checkpoint 寫入失敗處理
- 寫入失敗 → **唔影響主流程**（繼續做嘢）
- 但要喺 outbox reply 嘅「備註」標記：「Checkpoint 寫入失敗」
