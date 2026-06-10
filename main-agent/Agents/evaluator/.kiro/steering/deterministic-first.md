---
inclusion: always
description: Deterministic-First 原則 — Evaluator 專屬指引
---

# Deterministic-First 原則（Evaluator 版）

> **「可確定嘅嘢用代碼，唔確定嘅嘢用 AI」**

## Evaluator 責任

驗證 `deterministic` 類型嘅 Step 時，你**必須**：

1. **直接跑腳本** — `node script.js`，睇 exit code
2. **唔好用 LLM 判斷結果** — 腳本自己會 assert
3. **Exit code = 0 → PASS；≠ 0 → FAIL** — 零歧義

## 評估流程

```
收到 deterministic Step 嘅代碼
    │
    ▼
確認腳本存在 scripts/deterministic/{project}/
    │
    ├── 唔存在 → 直接 FAIL（Generator 冇遵守規則）
    │
    └── 存在 → 繼續
    │
    ▼
跑 `node script.js`
    │
    ├── Exit 0 + JSON output → 讀取 passed/failed 數字
    │
    └── Exit 1 或 Error → FAIL
    │
    ▼
檢查腳本質量（Code Review）
    │
    ▼
出 Verdict
```

## 腳本質量 Checklist

評估腳本時額外檢查：

| 項目 | 要求 | 唔合格 |
|------|------|--------|
| Test Cases 數量 | ≥ 3 | < 3 → 扣分 |
| Edge Cases | 至少 1 個 | 全部 happy path → 扣分 |
| 精度處理 | 金額用整數計算 | 浮點數直接計算 → FAIL |
| 可讀性 | 有 JSDoc + 清楚命名 | 冇注釋 → 扣分 |
| Self-contained | 零外部依賴 | 有 npm 依賴 → 扣分 |
| Error Handling | 異常 input 有 throw | 冇處理 → 扣分 |

## 分數調整

| 情況 | 調整 |
|------|------|
| Deterministic Step 冇寫腳本 | 直接 FAIL（唔計分） |
| 腳本跑得 pass 但質量差 | 上限 70 分 |
| 腳本跑得 pass + 質量好 | 正常計分 |
| 用 LLM 推理代替腳本 | 直接 FAIL |

## 識別 Deterministic Step

Assignment 入面會有標記：
- `類型: deterministic`
- 有明確 Input / Expected Output
- 有 test cases 作為 acceptance criteria

如果冇標記但你判斷應該係 deterministic（有標準答案、可驗證），喺反饋中指出：
> 「呢個 Step 應該標記為 deterministic，建議 Planner 更新。」
