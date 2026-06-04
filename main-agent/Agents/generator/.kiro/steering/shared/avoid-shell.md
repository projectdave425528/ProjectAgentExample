---
inclusion: manual
description: 避免 Shell Command 規則（Generator 本地副本）
---

# 避免 Shell Command 規則
> 📌 本文件係 Generator workspace 嘅本地副本，內容應與 Main Agent 嘅 `.kiro/steering/shared/avoid-shell.md` 一致。

## 核心原則
- **如非必要，唔好用 shell command** — 優先用內建工具（file read/write、search、etc.）
- Shell command 需要用戶 approve，浪費時間同打斷 flow

## 優先順序（由高到低）
1. **內建工具** — fs_write、str_replace、read_file、grep_search 等
2. **Hook** — 重複性操作寫成 Hook 自動執行
3. **Code/Script** — 寫一段 code 解決問題
4. **Shell command** — 最後手段，只用於以上方法都做唔到嘅情況

## 必須用 Shell 嘅例外情況
- 安裝 dependencies（npm install、pip install）
- Git 操作（commit、push、branch）
- 執行 build / test / lint
- 需要確認環境狀態（版本、路徑）
- 取得系統時間（Get-Date）

## 自我檢查
> 「呢個操作可唔可以用內建工具做到？」如果可以，就唔好用 shell。
> 「呢個 shell command 係咪會重複執行？」如果係，寫成 Hook。
