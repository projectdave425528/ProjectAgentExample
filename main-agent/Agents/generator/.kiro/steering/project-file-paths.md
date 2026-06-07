---
inclusion: always
description: Generator Project 路徑查表（L2 - 永遠載入）
---

# Generator Project 路徑查表

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **攞任務**：`./ProjectRecord/{active-project}/inbox/generator/assignment-{id}.md`
3. **睇 Planner 計劃**：`./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`
4. **搵歷史記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選）
5. **我嘅記憶**：`./ProjectRecord/{active-project}/memory/generator-memory.md`
6. **Spec（如有）**：`./ProjectRecord/{active-project}/specs/{requirements,design,tasks}.md`

## 我輸出去邊
- **代碼** → `./ProjectRecord/{active-project}/output/assignment-{id}/`
- **完成報告** → `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-completed.md`
- **Blocked 報告** → `./ProjectRecord/{active-project}/outbox/generator/assignment-{id}-reply-blocked.md`
- **Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/generator/`
