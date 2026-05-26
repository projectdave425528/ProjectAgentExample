---
inclusion: manual
description: Generator Agent 通訊協議（L2 - 手動載入）
---

# Generator 通訊協議
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## 收件格式

### 新任務
- 路徑：`inbox/task-{id}.md`
- 來源：Main Agent（含 Planner 方案）

### 修改反饋（FAIL）
- 路徑：`inbox/task-{id}-feedback.md`
- 來源：Evaluator（經 Main Agent 轉發）

## 發件格式

### 完成回覆
- 路徑：`outbox/task-{id}-reply.md`
- 目標：Main Agent → Evaluator

### Blocked 報告
- 路徑：`outbox/task-{id}-blocked.md`
- 目標：Main Agent → Planner

## 代碼輸出位置
- 路徑：`../../output/task-{id}/`
- 所有生成嘅代碼文件放喺呢度
- 目錄結構按項目模式組織

## Message Frontmatter 格式

```yaml
---
task-id: "task-{id}"
from: generator
to: main-agent
type: reply | blocked
timestamp: YYYY-MM-DD HH:mm
status: done | blocked
files-generated: [文件列表]
---
```

## 通訊規則
1. 每個 message 必須有 frontmatter
2. 完成報告要列出所有生成嘅文件
3. Blocked 報告要列出已嘗試嘅方法
4. 代碼同報告分開（代碼放 output/，報告放 outbox/）
