---
inclusion: manual
description: Main Agent 調度流程（L3 - 手動載入）
---

# Main Agent 調度流程

> 派工 / 收 reply / 做決定時讀取。

## 自動測試流程（Main Agent 職責）

### 派 Assignment 俾 Generator 時
1. 確認 Planner 計劃包含 Test Criteria
2. Assignment 明確要求：「必須同時提供 unit test + integration test」
3. 指定 test framework（根據技術棧）
4. 多模組互動 → 明確要求 integration test
   → 完成後：寫 Decision Log（記錄派工決策同理由）

### 收到 Generator 回覆時
1. 確認 output 包含 test 文件
2. 冇 unit test → 直接退回
3. 冇 integration test 但應該有 → 退回要求補充
4. 有 test → 正常派俾 Evaluator
   → 完成後：寫 Decision Log（記錄點解接受或退回）

### 派 Assignment 俾 Evaluator 時
1. 指示執行 unit test + integration test
2. 提供 test 文件路徑
3. 提供 Planner 嘅 Test Criteria
4. 確認測試環境配置
   → 完成後：寫 Decision Log

> 🔒 **Decision Log 規則**：每個調度 Step 完成後必須寫一份 Decision Log，見 `project-protocols-decision-log.md`。唔寫 = Step 未完成。

## Specs 管理規則

### 啟動時讀取
1. 確認 Project 後檢查 specs/ 是否存在
2. 有文件 → 讀取（requirements/design/tasks）
3. 用 Specs 作為 Assignment context

### 用戶要求建立 Specs 時
1. 派 Assignment 俾 Planner（type: plan-request）
2. Planner 完成後寫入 `./ProjectRecord/{active-project}/specs/`
3. Specs 文件格式必須參照 `./ProjectRecord/templates/specs/` 入面嘅 template

### TaskID 格式
- `{active-project}/Task-{number}`
