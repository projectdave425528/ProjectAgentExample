---
inclusion: manual
description: Generator ProjectRecord 寫入規則（L3 - 手動載入）
---

# ProjectRecord 寫入規則（必須遵守，零例外）

> 🔒 **寫入 ProjectRecord 係任務完成嘅必要條件。寫入失敗 = 任務未完成。**

## 規則

1. **任務完成 = outbox 寫入成功** — 無論結果係 completed/blocked/failed，都必須成功寫入 outbox reply
2. **寫入失敗處理**：
   - 第一次失敗 → 重試一次
   - 第二次失敗 → 嘗試用更簡單嘅內容寫入（至少包含 status + 一句話摘要）
   - 第三次失敗 → 向 Main Agent 回報：「ProjectRecord 寫入失敗，需要人工介入」
3. **回報格式**（寫入失敗時）：
   - 喺 console/output 明確輸出：`[ERROR] ProjectRecord 寫入失敗：{原因}`
   - 如果可以寫入其他位置，寫一份 fallback 到 `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-write-failed.md`
4. **唔好靜默失敗** — 寫入失敗絕對唔可以當冇事發生，必須通知 Main Agent 或用戶
