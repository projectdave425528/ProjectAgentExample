---
inclusion: always
description: Planner Project 路徑查表（L2 - 永遠載入）
---

# Planner Project 路徑查表

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **攞需求**：`./ProjectRecord/{active-project}/inbox/planner/assignment-{id}.md`
3. **搵歷史記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選）
4. **我嘅記憶**：`./ProjectRecord/{active-project}/memory/planner-memory.md`
5. **Spec template**：`./ProjectRecord/templates/specs/{requirements,design,tasks}-template.md`

## 我輸出去邊
- **方案回覆** → `./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`
- **Specs（如要求）** → `./ProjectRecord/{active-project}/specs/{requirements,design,tasks}.md`
- **上報** → `./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-escalation.md`
- **Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/planner/`
