---
inclusion: manual
description: Decision Log 寫入規則（L3 - 手動載入）
---

# Decision Log 規則（必須遵守，零例外）

> 🔒 **每個 Step 完成後必須寫一份 Decision Log。唔寫 = Step 未完成。**

## 目的

記錄每個 Step 嘅決策過程：考慮過咩方案、點解權衡後揀咗現時嘅選擇。
用途：審計、學習、日後追溯「點解當時咁做」。

## 文件路徑同命名

- **路徑**：`./ProjectRecord/{active-project}/decision-logs/{agent-name}/`
- **命名格式**：`decision-log-{assignment-id}-step{N}-{step-name}.md`
- **例如**：`decision-log-A001-step2-design-schema.md`

## 寫入時機（零例外）

**每個 Step 完成後，必須：**
1. 判斷：呢個 Step 有冇需要做決定？
   - **有決定**（例如揀方案、設計選擇、判斷分數）→ 完整寫 Decision Log（步驟 2-4）
   - **冇決定**（純讀取 / 純格式化 / 機械操作）→ 喺 Checkpoint 寫一行 `decision: mechanical — 無決策`，免去獨立文件
2. 讀取 `./ProjectRecord/templates/decision-log-template.md`
3. 填寫所有欄位
4. 寫入 `./ProjectRecord/{active-project}/decision-logs/{agent-name}/`
5. 喺 Checkpoint 加一行引用：`decision | 見 decision-log-{id}-step{N}-{name}.md`

## 必填欄位

| 欄位 | 要求 |
|------|------|
| Assignment ID | 必填，同 Checkpoint 一致 |
| Assignment Name | 必填，從 assignment 文件取得 |
| 問題陳述 | 一句話描述需要決定咩 |
| 考慮過嘅方案 | 至少 2 個方案（即使一個明顯較優） |
| 最終選擇 | 明確標示邊個方案 + 一句話原因 |
| 權衡因素 | 至少 1 個 |
| 潛在風險 | 至少 1 個 |

## 同 Checkpoint 嘅關係

- **Checkpoint** = 操作流水帳（做咗咩）→ 用途：恢復
- **Decision Log** = 決策推理（點解咁做）→ 用途：審計 + 學習
- 兩者獨立存在，Checkpoint 只引用 Decision Log 路徑

## 目錄結構

```
ProjectRecord/{active-project}/
├── checkpoints/
│   ├── main-agent/
│   ├── planner/
│   ├── generator/
│   └── evaluator/
│
└── decision-logs/              ← 新增
    ├── main-agent/
    ├── planner/
    ├── generator/
    └── evaluator/
```

## 寫入失敗處理

- 第一次失敗 → 重試
- 第二次失敗 → 簡化內容（至少包含 Assignment ID + 最終選擇 + 原因）
- 第三次失敗 → 喺 Checkpoint 標記 `decision-log-write-failed`，繼續主流程
- Decision Log 寫入失敗**唔阻塞**主任務，但必須標記
