---
inclusion: manual
description: Planner 格式一致性規則（L3 - 手動載入）
---

# 格式一致性規則（必須遵守，零例外）

> 所有寫入 ProjectRecord 嘅文件必須遵守 `./ProjectRecord/templates/` 嘅對應 template。

## 規則

1. **先讀取 `./ProjectRecord/active-project.md`** → 確認當前 Project 名稱
2. **寫 outbox assignment reply 前**：先讀 `./ProjectRecord/templates/assignment-reply-template.md`，按格式填寫
3. **所有欄位必須齊全** — template 入面有嘅欄位唔可以省略（可以填 N/A 但唔可以刪）
4. **唔好自創格式** — 唔好加 template 冇定義嘅 section（除非 template 有「備註」欄位）
5. **格式唔一致 = 任務未完成** — Main Agent 會驗證格式，唔合格退回重寫
6. **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫 SearchIndex.md
