---
inclusion: manual
description: Evaluator Agent 通訊協議（L2 - 手動載入）
---

# Evaluator 通訊協議
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## 收件格式

### 評估任務
- 路徑：`inbox/task-{id}.md`
- 來源：Main Agent
- 內容：代碼路徑 + 原始計劃（Planner 方案）

## 發件格式

### Verdict 回覆
- 路徑：`outbox/task-{id}-verdict.md`
- 目標：Main Agent

### Verdict 類型
| Verdict | 意義 | 下一步 |
|---------|------|--------|
| PASS | 代碼合格 | Main Agent 交付到 output/ |
| FAIL | 代碼需修改 | Main Agent 轉發反饋俾 Generator |
| REPLAN | 方案有根本問題 | Main Agent 轉發反饋俾 Planner |

## Message Frontmatter 格式

```yaml
---
task-id: "task-{id}"
from: evaluator
to: main-agent
type: verdict
timestamp: YYYY-MM-DD HH:mm
verdict: PASS | FAIL | REPLAN
score: [0-100]
fail-count: [第幾次 FAIL]
---
```

## 通訊規則
1. 每個 message 必須有 frontmatter
2. Verdict 文件名固定用 `-verdict.md` 後綴
3. 每次重新評估覆蓋同一個 verdict 文件
4. FAIL count 記錄喺 frontmatter（用於循環限制判斷）
