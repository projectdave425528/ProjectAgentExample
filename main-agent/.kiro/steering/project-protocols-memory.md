---
inclusion: manual
description: Main Agent Memory 更新規則（L3 - 手動載入）
---

# Memory 更新規則（必須執行，零例外）

## 自己嘅記憶
每次完成一輪調度（用戶需求 → 交付）後：
1. 讀取 `./ProjectRecord/{active-project}/memory/main-agent-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + 結果 + 備註）
3. 超過 5 條就刪最舊嘅
4. 如果有新發現，加到「調度經驗」或「項目知識」
5. **唔寫 memory = 任務未完成**

## 驗證 Sub Agent 記憶
收到任何 Agent 嘅 reply 後，檢查 `Memory 已更新` 欄位：
- ✅ → 正常繼續
- ❌ 或缺少 → 從 reply 內容提煉教訓，寫入 `./ProjectRecord/{active-project}/memory/{agent}-memory.md`
