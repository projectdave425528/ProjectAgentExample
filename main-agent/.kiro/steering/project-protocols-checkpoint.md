---
inclusion: manual
description: Main Agent Checkpoint 規則（L3 - 手動載入）
---

# Checkpoint 規則（必須遵守，零例外）

## 文件路徑同命名
- 格式：`checkpoint-A{id}-main-agent-{status}.md`
- 路徑：`./ProjectRecord/{active-project}/checkpoints/main-agent/`
- 開始：`checkpoint-A{id}-main-agent-in_progress.md`
- 完成：`checkpoint-A{id}-main-agent-completed.md`

## 寫入時機
1. **派 Assignment 前**：建立 checkpoint，填寫「計劃」section
2. **每個實際操作後必須 append 一行**（零例外）。**唔記錄 = 任務未完成**：
   - 寫 inbox assignment → `write` + 路徑 + 派俾邊個 Agent
   - 調用 Sub Agent → `shell` 或 `decision` + 調用方法
   - 收到 reply → `read` + outbox 路徑 + verdict/status
   - 做調度決定 → `decision` + 內容 + 原因
   - 更新 tasks.md → `write` + 邊個 Task
   - 更新 SearchIndex → `write` + 加咗幾行
   - 遇到錯誤 → `error` + 訊息
   - 重試 → `retry` + 第幾次 + 結果
3. **遇到問題/做決定**：append 到「問題同決策記錄」
4. **Task 完成（PASS）**：填「最終狀態」+ 重命名

## Checkpoints 目錄結構
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
│   └── checkpoint-A008-generator-in_progress.md
└── evaluator/
    └── checkpoint-A003-evaluator-completed.md
```

## 恢復流程（斷線後）
1. 掃描 `checkpoints/main-agent/` 搵 `*-in_progress.md`
2. 掃描 `checkpoints/{sub-agent}/` 了解執行進度
3. 對比 output/ + outbox/ 確認真實狀態
4. 判斷邏輯：

| Checkpoint | output/ | outbox/ | 動作 |
|-----------|---------|---------|------|
| in_progress | ❌ | ❌ | 重新派 Sub Agent |
| in_progress | ✅（部分） | ❌ | 讀 checkpoint → 重新派 |
| in_progress | ✅（完整） | ❌ | 補寫 reply → 派 Evaluator |
| in_progress | ✅ | ✅ | 更新 checkpoint → completed |
