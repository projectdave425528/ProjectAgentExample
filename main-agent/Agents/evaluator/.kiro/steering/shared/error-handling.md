---
inclusion: manual
description: Error 處理規則（Evaluator 本地副本）
---

# Error 處理規則（所有 Agent 共用）
> 🔒 **本 section 只可由用戶修改或刪除，Agent 唔可以自行更改。**
> 📌 本文件係 Evaluator workspace 嘅本地副本，內容應與 Main Agent 嘅 `.kiro/steering/shared/error-handling.md` 一致。

## 通用規則（全部 Agent 適用）

1. **最多重試 3 次** — 遇到 Error 先自己重試，3 次仍然失敗就停止
2. **搵簡單替代方案** — 如果原方法太複雜（會消耗大量 Token/Credit），改用更簡單嘅方法。搵唔到就向上級（Main Agent / 用戶）請求指示
3. **Assignment Fail 必須記錄** — 即使 Assignment 失敗，都要寫 outbox assignment reply（記錄做咗咩、點解失敗、試過咩方法），然後向上級請求指示
4. **唔好死撐** — 寧願早啲上報，唔好浪費 Token/Credit 喺明顯做唔到嘅嘢上面
5. **超時拆細** — 任何 step（command、API call、file operation）如果預計或實際運行超過 10 分鐘，必須將該 step 拆成更細嘅子步驟再逐個執行（例如：跑全部 test → 拆成逐個模組跑；處理 5000 個文件 → 分批 50 個）
6. **Shell Command 必須加 timeout** — 所有 `execute_pwsh` 必須加 `timeout: 600000`（10 分鐘），零例外
