---
inclusion: always
description: Planner Agent 通訊協議（L2 - 永遠載入）
---

# Planner 通訊協議
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## 收件格式

### 新任務
- 路徑：`inbox/assignment-{id}.md`
- 來源：Main Agent
- 備註：如果係 REPLAN，Context 會包含之前嘅 FAIL 原因

## 發件格式

### 方案回覆
- 路徑：`outbox/assignment-{id}-reply-completed.md`
- 目標：Main Agent → Generator

### Escalation（上報）
- 路徑：`outbox/assignment-{id}-reply-escalation.md`
- 目標：Main Agent（需要用戶決定）

## Message Frontmatter 格式

```yaml
---
task-id: "assignment-{id}"
from: planner
to: main-agent
type: assignment-reply | escalation
timestamp: YYYY-MM-DD HH:mm
status: completed | blocked | need-clarification
---
```

## 通訊規則
1. 每個 message 必須有 frontmatter
2. 一個 assignment-id 對應一個 assignment reply 文件
3. Escalation 同 assignment reply 分開文件
