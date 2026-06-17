---
inclusion: always
description: Evaluator Project 路徑查表（L2 - 永遠載入）
---

# Evaluator Project 路徑查表

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **攞評估任務**：`./ProjectRecord/{active-project}/inbox/evaluator/assignment-{id}.md`（含代碼路徑 + 計劃）
3. **睇要評嘅代碼**：`./ProjectRecord/{active-project}/output/assignment-{id}/`
4. **睇原始計劃**：`./ProjectRecord/{active-project}/outbox/planner/assignment-{id}-reply-completed.md`（對照 Test Criteria）
5. **搵歷史記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選）
6. **我嘅記憶**：`./ProjectRecord/{active-project}/memory/evaluator-memory.md`

## 我輸出去邊
- **Verdict** → `./ProjectRecord/{active-project}/outbox/evaluator/assignment-{id}-reply-verdict.md`
- **FAIL 時** → 重命名 `output/assignment-{id}/` 為 `output/assignment-{id}-FAILED/`
- **Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/evaluator/`
- **Decision Log** → `./ProjectRecord/{active-project}/decision-logs/evaluator/`
