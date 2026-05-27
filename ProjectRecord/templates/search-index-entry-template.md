# SearchIndex Entry Template

> 每次寫入 ProjectRecord（inbox/outbox）後，必須 append 一行到 `ProjectRecord/{active-project}/SearchIndex.md`。

## 格式

```
| {assignment-id} | {agent} | {type} | {status} | {關鍵字} | {YYYY-MM-DD} | {文件相對路徑} |
```

## 欄位說明

| 欄位 | 說明 | 例子 |
|------|------|------|
| Assignment ID | 任務編號 | 001 |
| Agent | 寫入嘅 Agent | planner / generator / evaluator / main-agent |
| Type | 文件類型 | assignment / assignment-reply / verdict / blocked / escalation |
| Status | 狀態 | dispatched / completed / blocked / failed / PASS / FAIL / REPLAN |
| 關鍵字 | 一句話描述（≤10 字） | Todo API 架構設計 |
| 日期 | 寫入日期 | 2026-05-27 |
| 文件路徑 | 相對於 ProjectRecord/ 嘅路徑 | planner/outbox/assignment-001-reply-completed.md |

---

## 實例

### 實例 1：Main Agent 派發任務

```
| 001 | main-agent | assignment | dispatched | Todo API 需求分析 | 2026-05-27 | planner/inbox/assignment-001.md |
```

### 實例 2：Planner 完成回覆

```
| 001 | planner | assignment-reply | completed | Todo API 架構設計 | 2026-05-27 | planner/outbox/assignment-001-reply-completed.md |
```

### 實例 3：Generator 完成

```
| 002 | generator | assignment-reply | completed | Todo CRUD endpoints | 2026-05-27 | generator/outbox/assignment-002-reply-completed.md |
```

### 實例 4：Generator Blocked

```
| 002 | generator | blocked | blocked | 缺少 DB connection | 2026-05-27 | generator/outbox/assignment-002-reply-blocked.md |
```

### 實例 5：Evaluator PASS

```
| 003 | evaluator | verdict | PASS (86) | Todo API 通過 | 2026-05-27 | evaluator/outbox/assignment-003-reply-verdict.md |
```

### 實例 6：Evaluator FAIL

```
| 003 | evaluator | verdict | FAIL (63) | SQL injection 風險 | 2026-05-27 | evaluator/outbox/assignment-003-reply-verdict.md |
```

### 實例 7：Escalation

```
| 001 | planner | escalation | need-clarification | 需要確認認證 scope | 2026-05-27 | planner/outbox/assignment-001-reply-escalation.md |
```

---

## 搜尋用法

Agent 搵記錄時：
1. 讀取 `ProjectRecord/{active-project}/SearchIndex.md`
2. 用關鍵字 / Assignment ID / Agent / Status 篩選
3. 只讀取對應嘅文件路徑

**唔好逐個 inbox/outbox 文件讀取 — 先查 SearchIndex！**
