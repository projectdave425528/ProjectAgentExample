---
inclusion: manual
description: Planner Checkpoint 規則（L3 - 手動載入）
---

# Checkpoint 規則（必須遵守，零例外）

> 每個 Assignment 必須有一份 Checkpoint 文件。

## 文件路徑同命名
- 格式：`checkpoint-A{id}-planner-{status}.md`
- 路徑：`./ProjectRecord/{active-project}/checkpoints/planner/`
- 開始：`checkpoint-A{id}-planner-in_progress.md`
- 完成：`checkpoint-A{id}-planner-completed.md`
- Blocked：`checkpoint-A{id}-planner-blocked.md`
- **重命名方法**：用 `smartRelocate` 工具（唔好用 shell）

## 寫入時機
1. **開始前**：讀 `./ProjectRecord/templates/checkpoint-template.md`，填寫「計劃」section
2. **每個實際操作後必須 append 一行**（零例外）：
   - 寫文件 → `write` + 路徑 + 用途
   - 讀文件 → `read` + 路徑 + 目的
   - 做技術決定 → `decision` + 內容 + 原因
   - 遇到錯誤 → `error` + 錯誤訊息 + 影響
   - 重試 → `retry` + 第幾次 + 結果
3. **遇到問題/做決定**：append 到「問題同決策記錄」section
4. **完成時**：填「最終狀態」section + 重命名文件
5. **唔記錄 = 任務未完成**

## Checkpoint 寫入失敗處理
- 失敗 → 唔影響主流程，繼續做
- 喺 outbox reply 備註：「Checkpoint 寫入失敗」
