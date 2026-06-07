---
inclusion: manual
description: 格式一致性規則（L3 - 寫 outbox reply 前確認格式）
---

# 格式一致性規則（必須遵守，零例外）

> 所有寫入 ProjectRecord 嘅文件必須嚴格遵守 `./ProjectRecord/templates/` 入面嘅對應 template。

1. **寫 verdict 前**：先讀取 `./ProjectRecord/templates/assignment-reply-template.md`，按格式填寫
   - AssignmentStatus 用 `verdict-pass` / `verdict-fail` / `verdict-replan`
2. **所有欄位必須齊全** — template 入面有嘅欄位唔可以省略（分數必須填數字，唔可以填 N/A）
3. **唔好自創格式** — 唔好加 template 冇定義嘅 section
4. **格式唔一致 = 任務未完成** — Main Agent 會驗證格式，唔合格會退回重寫
5. **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫 SearchIndex.md
