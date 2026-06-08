---
inclusion: manual
description: Generator Error + Timeout 處理規則（L3 - 手動載入）
---

# Error 處理 + Timeout 處理規則（必須遵守，零例外）
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## Error 處理
1. **最多重試 3 次** — 遇到 Error 先自己重試，3 次仍然失敗就停止
2. **搵簡單替代方案** — 如果原方法太複雜（會消耗大量 Token/Credit），改用更簡單嘅方法。搵唔到就向 Main Agent 或用戶請求指示
3. **Assignment Fail 必須記錄** — 即使 Assignment 失敗，都要寫 outbox assignment reply（記錄做咗咩、點解失敗、試過咩方法），然後向 Main Agent 或用戶請求指示
4. **唔好死撐** — 寧願早啲上報，唔好浪費 Token/Credit 喺明顯做唔到嘅嘢上面
5. **Shell Command 必須加 timeout** — 所有 `execute_pwsh` 必須加 `timeout: 600000`（10 分鐘），零例外

## Timeout 處理流程
1. **每個 Step 開始前**執行 `Get-Date` 記錄開始時間
2. **每次 tool call 完成後**對比時間：
   - T < 10 min → 繼續執行
   - T ≥ 10 min → 自我評估：呢個 Step 係咪正常推進中？
3. **正常推進** → 繼續，但最大時限 30 分鐘
4. **卡住/無進展/T ≥ 30 min** → 進入 Fallback

## Fallback 流程
1. 有替代方法可唔超時？ → Yes → 換方法重做
2. 冇替代方法？ → 超時拆細，拆成更細步驟重試
3. 重試次數 < 3？ → Yes → 返回 Step 頂部重新執行
4. 重試次數 ≥ 3？ → 停止執行，報告失敗，向 Main Agent 或用戶請求指示

## Step 完成後
- Step 完成 → 自動進入下一個 Step
- 全部 Step 完成 → Task 完成，報告成功

## 零例外規則
- 上述流程適用於所有 Step，冇例外
- Agent 唔可以跳過進度檢查
- Agent 唔可以跳過時間記錄
