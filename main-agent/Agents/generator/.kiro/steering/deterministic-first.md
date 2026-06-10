---
inclusion: always
description: Deterministic-First 原則 — Generator 專屬指引
---

# Deterministic-First 原則（Generator 版）

> **「可確定嘅嘢用代碼，唔確定嘅嘢用 AI」**

## Generator 責任

當 Assignment 嘅 Step 標記為 `deterministic` 時，你**必須**：

1. **寫一個 JS 腳本**（唔係用 LLM 推理去得出答案）
2. **放入** `scripts/deterministic/{project-name}/`
3. **腳本自帶驗證** — `verify()` 函數 + test cases
4. **可獨立執行** — `node script.js` 直接跑

## 腳本要求

| 要求 | 規範 |
|------|------|
| 執行方式 | `node script.js`（零依賴或只用 Node 內建模組） |
| Exit Code | 0 = pass, 1 = fail |
| 輸出格式 | JSON（`{ status, passed, failed, total }`） |
| 命名 | `{task-id}-{description}.js` |
| 精度 | 金額用整數（cent）計算，最後除 100 |
| 可重用 | `module.exports = { main }` 方便其他腳本調用 |

## 模板位置

```
scripts/deterministic/_templates/
├── deterministic-template.js   ← 通用模板
└── validator-template.js       ← 格式驗證
```

## 工作流程

```
收到 deterministic Step
    │
    ▼
查看 _templates/ 有冇合適模板
    │
    ├── Yes → 複製模板，改 main() 邏輯
    │
    └── No → 用 deterministic-template.js 起步
    │
    ▼
實現 main() 函數
    │
    ▼
加入 test cases（至少 3 個，覆蓋 edge cases）
    │
    ▼
本地跑 `node script.js` 確認 PASS
    │
    ▼
放入 output folder
```

## 禁止事項

- ❌ 唔好用 LLM 推理去做 deterministic 計算（例：唔好用 AI 計 1+1）
- ❌ 唔好寫依賴外部服務嘅腳本（必須 self-contained）
- ❌ 唔好用 `eval()` 或 `Function()` 做動態執行
- ❌ 唔好省略 test cases（最少 3 個）
- ❌ 唔好用浮點數直接做金額計算（必須轉整數）

## 同 Unit Test 嘅關係

Deterministic 腳本嘅 `verify()` **唔係取代** Unit Test：
- `verify()` = 腳本自身嘅快速驗證
- Unit Test = 驗證整個模組嘅行為（可能調用呢個腳本）

兩者都要有。
