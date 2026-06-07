---
inclusion: always
description: Main Agent Project 路徑查表 + 完整目錄結構圖（L2 - 永遠載入）
---

# Main Agent Project 路徑查表

## 點搵 Project 內容
1. **確認當前 Project**：先讀 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. **搵記錄**：先讀 `./ProjectRecord/{active-project}/SearchIndex.md`（用關鍵字/ID 篩選）
3. **斷線恢復**：掃 `./ProjectRecord/{active-project}/checkpoints/*/` 搵 `*-in_progress.md`
4. **收 Sub Agent reply**：`./ProjectRecord/{active-project}/outbox/{agent}/`
5. **Spec（如有）**：`./ProjectRecord/{active-project}/specs/{requirements,design,tasks}.md`
6. **各 Agent 記憶**：`./ProjectRecord/{active-project}/memory/{agent}-memory.md`
7. **共用 template**：`./ProjectRecord/templates/`

## 我寫去邊
- **派工** → `./ProjectRecord/{active-project}/inbox/{agent}/assignment-{id}.md`
- **對話記錄** → `./ProjectRecord/{active-project}/conversation-log.md`（append）
- **搜尋索引** → `./ProjectRecord/{active-project}/SearchIndex.md`（每次寫入後 append）
- **我嘅 Checkpoint** → `./ProjectRecord/{active-project}/checkpoints/main-agent/`
- **交付成品** → `./ProjectRecord/{active-project}/output/`

## 完整目錄結構
```
./ProjectRecord/
├── active-project.md
├── templates/
└── {active-project}/
    ├── specs/
    ├── memory/ (main-agent / planner / generator / evaluator)
    ├── SearchIndex.md
    ├── conversation-log.md
    ├── checkpoints/ (main-agent / planner / generator / evaluator)
    ├── control/
    ├── output/
    ├── inbox/ (planner / generator / evaluator / main-agent)
    └── outbox/ (planner / generator / evaluator / main-agent)
```

## Sub Agent 速查
| Agent | 派俾佢做 | 佢寫去 |
|-------|---------|--------|
| `planner` | 需求分析 / 架構 / 任務拆分 / Specs | `outbox/planner/` |
| `generator` | 按計劃寫 code + test | `output/` + `outbox/generator/` |
| `evaluator` | 跑 test + 評分（PASS/FAIL/REPLAN） | `outbox/evaluator/` |

## UserConfig / UserDocument 放置
### 路徑決定流程
1. 讀取 `./ProjectRecord/active-project.md` 嘅 `current` 值
2. 如果操作屬於特定 Project → 寫入 `./ProjectRecord/{current}/UserConfig/` 或 `UserDocument/`
3. 如果操作係通用/跨 Project → 寫入頂層 `./UserConfig/` 或 `./UserDocument/`
