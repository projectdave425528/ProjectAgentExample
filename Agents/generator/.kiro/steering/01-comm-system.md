---
inclusion: manual
description: Generator Agent 通訊協議（L2 - 手動載入）
---

# Generator 通訊協議
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## 收件格式

### 新任務
- 路徑：`inbox/assignment-{id}.md`
- 來源：Main Agent（含 Planner 方案；如果係 FAIL 重做，Context 會包含之前嘅 FAIL 原因 + 修改建議）

## 發件格式

### 完成回覆
- 路徑：`outbox/assignment-{id}-reply-completed.md`
- 目標：Main Agent → Evaluator

### Blocked 報告
- 路徑：`outbox/assignment-{id}-reply-blocked.md`
- 目標：Main Agent → Planner

## 代碼輸出位置
- 路徑：`ProjectRecord/{active-project}/output/assignment-{id}/`
- 所有生成嘅代碼文件放喺呢度
- 目錄結構按項目模式組織

## Message Frontmatter 格式

```yaml
---
task-id: "assignment-{id}"
from: generator
to: main-agent
type: assignment-reply | blocked
timestamp: YYYY-MM-DD HH:mm
status: done | blocked
files-generated: [文件列表]
---
```

## 通訊規則
1. 每個 message 必須有 frontmatter
2. 完成報告要列出所有生成嘅文件
3. Blocked 報告要列出已嘗試嘅方法
4. 代碼同報告分開（代碼放 ProjectRecord/{active-project}/output/，報告放 outbox/）
