---
inclusion: manual
description: Main Agent Shell 使用政策（L3 - 手動載入）
---

# Shell 使用政策

> 如非必要唔好用 shell，優先用內建工具。

## 優先順序（由高到低）
1. **內建工具** — read_file、fs_write、str_replace、grep_search 等
2. **Hook** — 重複性操作寫成 Hook 自動執行
3. **Code/Script** — 寫一段 code 解決問題
4. **Shell command** — 最後手段

## 自我檢查
用 shell 前問自己：
- 「呢個操作可唔可以用內建工具做到？」→ 可以就唔用 shell
- 「呢個 shell command 係咪會重複執行？」→ 係就寫成 Hook

## 允許使用 Shell 嘅情況
| 情況 | 例子 |
|------|------|
| 裝 dependency | `npm install`、`pip install` |
| Git 操作 | `git add`、`git commit`、`git push` |
| Build / Lint | `npm run build` |
| 確認環境 | `kiro-cli --version`、`node --version` |
| 取系統時間 | `Get-Date` |
| 調用 kiro-cli | `kiro-cli chat --agent [name]` |

## 禁止用 shell 嘅情況
- ❌ 讀文件（用 read_file）
- ❌ 寫文件（用 fs_write）
- ❌ 搜尋文件（用 grep_search）
- ❌ 移動/重命名（用 smartRelocate）
- ❌ 刪除文件（需用戶確認）

## 必須加 timeout
所有 `execute_pwsh` 必須加 `timeout: 600000`，零例外。
