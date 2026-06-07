---
inclusion: manual
description: Main Agent ProjectRecord 寫入規則（L3 - 手動載入）
---

# ProjectRecord 寫入規則（必須遵守，零例外）

> 🔒 **寫入 ProjectRecord 係任務完成嘅必要條件。**

1. **任務完成 = outbox 寫入成功** — 無論結果係咩，都必須寫入
2. **寫入失敗處理**：
   - 第一次失敗 → 重試
   - 第二次失敗 → 簡化內容寫入
   - 第三次失敗 → 向用戶回報
3. **唔好靜默失敗** — 必須通知用戶
