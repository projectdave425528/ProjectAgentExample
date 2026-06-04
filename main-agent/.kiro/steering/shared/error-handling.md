---
inclusion: manual
description: 共用 Error 處理規則（所有 Agent 嘅單一來源 / Single Source of Truth）
---

# Error 處理規則（所有 Agent 共用）
> 🔒 **本 section 只可由用戶修改或刪除，Agent 唔可以自行更改。**
> 📌 本文件係 Error 處理嘅 **canonical 來源**。各 Agent L1 嘅 Error 處理 section 應與此一致；如有衝突，以本文件為準。

## 通用規則（全部 Agent 適用）

1. **最多重試 3 次** — 遇到 Error 先自己重試，3 次仍然失敗就停止
2. **搵簡單替代方案** — 如果原方法太複雜（會消耗大量 Token/Credit），改用更簡單嘅方法。搵唔到就向上級（Main Agent / 用戶）請求指示
3. **Assignment Fail 必須記錄** — 即使 Assignment 失敗，都要寫 outbox assignment reply（記錄做咗咩、點解失敗、試過咩方法），然後向上級請求指示
4. **唔好死撐** — 寧願早啲上報，唔好浪費 Token/Credit 喺明顯做唔到嘅嘢上面
5. **超時拆細** — 任何 step（command、API call、file operation）如果預計或實際運行超過 10 分鐘，必須將該 step 拆成更細嘅子步驟再逐個執行（例如：跑全部 test → 拆成逐個模組跑；處理 5000 個文件 → 分批 50 個）
6. **Shell Command 必須加 timeout** — 所有 `execute_pwsh` 必須加 `timeout: 600000`（10 分鐘），零例外

## Main Agent 專屬補充

- **替代方案必須問用戶確認** — Main Agent 唔可以自己決定用替代方案。格式：
  ```
  ⚠️ 原方案遇到問題
  - 問題：{描述}
  - 原方案：{原本做法}
  - 替代方案：{簡化後嘅做法}
  - 影響：{替代方案有咩 trade-off}
  請確認用替代方案 / 其他建議？
  ```
- **Sub Agent 調用失敗處理**：
  - 第 1 次失敗 → 重試（用同一方法）
  - 第 2 次失敗 → 切換方法（CLI → invoke_sub_agent，或反過來）
  - 第 3 次失敗 → 停止，向用戶上報（列出兩個方法嘅 error + 建議方向）
