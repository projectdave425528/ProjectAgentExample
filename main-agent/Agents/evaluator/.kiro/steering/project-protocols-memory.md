---
inclusion: manual
description: Memory 更新規則（L3 - 寫 outbox reply 時）
---

# Memory 更新規則（必須執行，零例外）

完成任務寫 outbox assignment reply 時，**必須同時**更新 Project Memory：

1. 讀取 `./ProjectRecord/{active-project}/memory/evaluator-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + Verdict + 主要問題）
3. 超過 5 條就刪最舊嘅
4. 如果有新發現，加到「評估經驗」或「項目標準」
5. Reply 必須包含欄位：`Memory 已更新：✅/❌`
6. **唔寫 memory = 任務未完成**
