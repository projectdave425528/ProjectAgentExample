---
inclusion: always
description: Deterministic-First 原則 — Planner 專屬指引
---

# Deterministic-First 原則（Planner 版）

> **「可確定嘅嘢用代碼，唔確定嘅嘢用 AI」**

## Planner 責任

設計任務時，你**必須**為每個 Step 標記類型：

### 標記格式

```markdown
### Step X: {描述}
- **類型**: `deterministic` | `ai-driven`
- **如果 deterministic**:
  - Input: {明確嘅輸入格式}
  - Expected Output: {明確嘅輸出格式}
  - 驗證方法: 跑腳本 assert
```

## 判斷標準

以下情況 **必須標記為 `deterministic`**：

| 條件 | 例子 |
|------|------|
| 有標準答案 | 金額計算、稅率計算 |
| 可 assert | 輸入 A 必須得到 B |
| 重複性 > 1 | 每次部署都要跑嘅驗證 |
| 精度要求高 | 財務數字、日期推算 |
| 有明確規則 | if/else 可表達嘅邏輯 |

以下情況 **標記為 `ai-driven`**：

| 條件 | 例子 |
|------|------|
| 需要理解語意 | 解析用戶需求 |
| 需要創造力 | 設計 UI 佈局 |
| 冇標準答案 | 選擇最佳架構 |

## 對 Generator 嘅指引

當你標記 Step 為 `deterministic` 時，喺 Assignment 要寫明：
1. Generator 必須產出一個 JS 腳本（唔係用 AI 推理）
2. 腳本放入 `scripts/deterministic/{project-name}/`
3. 腳本必須自帶 test cases
4. 提供 2-3 個 test case 作為 acceptance criteria

## 範例

```markdown
### Step 3: 計算月結帳目餘額
- **類型**: `deterministic`
- **Input**: `{ entries: Array<{ debit: number, credit: number, account: string }> }`
- **Expected Output**: `{ balances: Record<string, number>, balanced: boolean }`
- **Acceptance Criteria**:
  - Test Case 1: 單筆借貸 → balanced: true
  - Test Case 2: 多帳戶交叉 → 各帳戶餘額正確
  - Test Case 3: 浮點數精度 → 0.1 + 0.2 = 0.3（唔係 0.30000000000000004）
- **Generator 指引**: 用 `_templates/accounting-template.js` 作參考
```
