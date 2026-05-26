---
inclusion: manual
description: Planner Agent 通訊協議（L2 - 手動載入）
---

# Planner 通訊協議
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## 收件格式

### 新任務
- 路徑：`inbox/task-{id}.md`
- 來源：Main Agent

### 反饋（REPLAN）
- 路徑：`inbox/task-{id}-feedback.md`
- 來源：Evaluator（經 Main Agent 轉發）

## 發件格式

### 方案回覆
- 路徑：`outbox/task-{id}-reply.md`
- 目標：Main Agent → Generator

### Escalation（上報）
- 路徑：`outbox/task-{id}-escalation.md`
- 目標：Main Agent（需要用戶決定）

## Message Frontmatter 格式

```yaml
---
task-id: "task-{id}"
from: planner
to: main-agent
type: reply | escalation
timestamp: YYYY-MM-DD HH:mm
status: done | blocked | need-clarification
---
```

## 通訊規則
1. 每個 message 必須有 frontmatter
2. 一個 task-id 對應一個 reply 文件（覆蓋更新）
3. Escalation 同 reply 分開文件
4. 收到 feedback 後，更新原有 reply（唔好開新文件）
