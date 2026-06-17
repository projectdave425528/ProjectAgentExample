---
inclusion: manual
description: Generator 任務執行流程（L3 - 手動載入）
---

# Generator 任務執行流程

> 開始任務時讀取。包含啟動流程、自我評估、自學流程。

## 啟動流程
1. 讀 `./ProjectRecord/active-project.md` → 確認當前 Project
2. 讀 `./ProjectRecord/{active-project}/inbox/generator/assignment-{id}.md` → 取得任務計劃
3. 建立 Checkpoint（見 `project-protocols-checkpoint.md`）
4. 自我評估 → 確認有能力完成
   → 完成後：寫 Decision Log（記錄評估結果同點解決定繼續/自學/blocked）
5. 確認 Task 嘅 Test Criteria（從 Planner 計劃取得）
6. 讀 `domain-knowledge-test-rules.md` → 了解測試要求
7. 讀 `domain-knowledge-code-standards.md` → 了解代碼規範
8. 讀 `../../.kiro/skills/clean-code/SKILL.md`（Part A）→ Clean Code 原則
   → 完成後：寫 Decision Log（記錄點解揀呢個 Clean Code 策略）
9. 讀 `../../.kiro/skills/design-patterns/SKILL.md`（Part B）→ Design Patterns 實現指引
   → 完成後：寫 Decision Log（記錄點解揀呢個 Design Pattern）
10. 生成代碼 + 對應 Unit Test → 寫到 `./ProjectRecord/{active-project}/output/`
    → 每完成一個主要模組：寫 Decision Log（記錄代碼實現嘅關鍵決策）
11. 每完成一個文件 → 更新 Checkpoint 執行記錄（零例外）
12. 本地驗證 test 可以 pass（如果環境允許）
13. 按 template 寫完成報告到 outbox → 更新 Checkpoint → 更新 memory

> 🔒 **Decision Log 規則**：每個 Step 完成後必須寫一份 Decision Log，見 `project-protocols-decision-log.md`。唔寫 = Step 未完成。

## 自我評估清單

收到任務後，逐項檢查：

| # | 評估項目 | 通過條件 | 不通過動作 |
|---|----------|----------|------------|
| 1 | 語言熟悉度 | 知道語法 + 常用 pattern | 自學 |
| 2 | 框架熟悉度 | 知道 API + 最佳實踐 | 自學 |
| 3 | 業務邏輯理解 | 明白 acceptance criteria | 問 Planner |
| 4 | 外部依賴 | 所有 library 可用 | 報告 blocked |
| 5 | 安全要求 | 知道點防 injection / XSS | 自學 |

### 評估結果
- 全部通過 → 直接開始生成
- 1-2 項不通過 → 進入自學流程
- 3+ 項不通過 → 報告 blocked

## 自學流程（5 步）

```
Step 1: 識別知識缺口（明確列出「我唔知咩」）
Step 2: 搜尋文檔（官方文檔 > Stack Overflow > Blog）
Step 3: 讀範例代碼（repo 內類似實現 / 官方 example）
Step 4: 小規模驗證（最小 POC 確認理解正確）
Step 5: 放棄自學，報告 blocked
```

### 自學限制
- 每個知識缺口最多 3 次搜尋嘗試
- 3 次搵唔到答案 → 直接 blocked
- 唔好無限 loop 喺自學
