# Deterministic Scripts

> 放置所有確定性任務腳本。遵循 Deterministic-First 原則。

## 目錄結構

```
scripts/deterministic/
├── {project-name}/
│   ├── {task-id}-{description}.js       ← 主腳本
│   ├── {task-id}-{description}.test.js  ← 腳本自身嘅 test
│   └── README.md                         ← 該 Project 嘅腳本說明
├── _templates/
│   ├── deterministic-template.js         ← 通用模板
│   └── validator-template.js             ← 格式驗證模板
└── README.md                             ← 本文件
```

## 使用規則

1. **每個腳本必須可獨立執行** — `node script.js` 即可跑
2. **Exit Code** — 0 = pass, 1 = fail
3. **輸出格式** — JSON（方便機器解析）
4. **自帶驗證** — 每個腳本都有 `verify()` 函數同 test cases
5. **命名規範** — `{task-id}-{描述}.js`（例：`T001-calculate-tax.js`）

## 適用場景

- 測試斷言 / Test Runner
- 會計帳目計算
- 數學運算
- 格式驗證（JSON / 日期 / email）
- 數據轉換（CSV → JSON）
- 字串解析（regex）
- 文件模板生成

## 唔適用場景（應由 AI 處理）

- 需求分析
- 架構設計
- 代碼審查意見
- 自然語言生成
