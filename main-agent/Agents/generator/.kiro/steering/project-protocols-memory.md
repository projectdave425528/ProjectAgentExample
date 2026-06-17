---
inclusion: manual
description: Generator Memory 更新規則（L3 - 手動載入）
---

# Memory 更新規則（必須執行，零例外）

> 完成任務寫 outbox reply 時，**必須同時**更新 Memory。

## 更新步驟
1. 讀取 `./ProjectRecord/{active-project}/memory/generator-memory.md`
2. 喺「最近任務」表格加一行（日期 + 摘要 + 結果 + 學到咩）
3. 超過 5 條就刪最舊嘅
4. 如果有新教訓，加到「常見錯誤」或「項目知識」
5. 如果有**重要教訓**（會影響未來代碼質量嘅），加到「重要教訓（永久）」section（最多 10 條，滿咗就替換最唔重要嘅）
6. Reply 必須包含欄位：`Memory 已更新：✅/❌`

## 重要規則
- **唔寫 memory = 任務未完成**
- 即使 Assignment 失敗（blocked/partial），都要更新 memory
