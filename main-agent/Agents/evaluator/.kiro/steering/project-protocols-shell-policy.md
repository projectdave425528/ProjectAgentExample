---
inclusion: manual
description: Shell 使用政策（L3 - 想用 shell 前讀）
---

# Shell 使用政策

> 如非必要唔好用 shell，優先用內建工具（read_file / fs_write / str_replace / grep_search）。

## 允許使用 Shell 嘅情況
| 情況 | 例子 |
|------|------|
| 執行 test | `pytest`、`npm test`、`dotnet test` |
| 確認環境 | `node --version`、`python --version` |
| 裝 dependency | `npm install`、`pip install` |
| Build / Lint | `npm run build`、`eslint` |
| 取系統時間 | `Get-Date` |

## 必須遵守
1. 所有 `execute_pwsh` 必須加 `timeout: 600000`
2. 唔好用 shell 做可以用內建工具做嘅嘢（讀/寫文件、搜尋）
3. 唔好用 shell 做破壞性操作（rm -rf、drop table）
4. 長 command 考慮寫成 script 文件再執行
