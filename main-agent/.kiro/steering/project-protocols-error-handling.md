---
inclusion: manual
description: Main Agent Error + Timeout 處理規則（L3 - 手動載入）
---

# Error 處理 + Timeout 處理規則（必須遵守，零例外）
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## Error 處理
1. **最多重試 3 次** — 調用 Agent 出錯時重試，3 次仍然失敗就停止
2. **搵簡單替代方案** — 必須問用戶確認先可以執行：
   ```
   ⚠️ 原方案遇到問題
   - 問題：{描述}
   - 原方案：{原本做法}
   - 替代方案：{簡化後嘅做法}
   - 影響：{trade-off}
   請確認用替代方案 / 其他建議？
   ```
3. **Assignment Fail 必須記錄** — 即使失敗都要寫 outbox reply
4. **唔好死撐** — 寧願早啲問用戶
5. **Shell Command 必須加 timeout: 600000**
6. **Sub Agent 調用失敗處理**：
   - 第 1 次 → 重試（同一方法）
   - 第 2 次 → 切換方法（CLI ↔ invoke_sub_agent）
   - 第 3 次 → 停止，向用戶上報

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
4. 重試次數 ≥ 3？ → 停止執行，報告失敗，問用戶

## Step 完成後
- Step 完成 → 自動進入下一個 Step
- 全部 Step 完成 → Task 完成，報告成功

## 零例外規則
- 上述流程適用於所有 Step，冇例外
- Agent 唔可以跳過進度檢查
- Agent 唔可以跳過時間記錄
