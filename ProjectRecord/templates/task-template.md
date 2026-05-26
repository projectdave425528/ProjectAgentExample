# Task {id}

- **From**: main-agent
- **To**: {agent-name}
- **Timestamp**: {ISO timestamp}
- **Type**: plan-request | generate-request | evaluate-request

## 需求
{具體內容}

## Context
{相關背景資訊}

## 預期輸出
{期望 Agent 回覆咩}

---

## 實例

### 實例 1：Plan Request

```markdown
# Task 001

- **From**: main-agent
- **To**: planner
- **Timestamp**: 2026-05-27T10:30:00+08:00
- **Type**: plan-request

## 需求
幫我設計一個 REST API，用嚟管理用戶嘅 Todo List。需要支援 CRUD 操作同用戶認證。

## Context
- 技術棧：Node.js + Express + PostgreSQL
- 已有 User model，需要加 Todo model
- 部署環境：Docker + AWS ECS

## 預期輸出
方案摘要 + 架構圖 + 任務清單 + 風險評估
```

### 實例 2：Generate Request

```markdown
# Task 002

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-27T11:00:00+08:00
- **Type**: generate-request

## 需求
根據 Planner 嘅計劃，實現 Todo CRUD API endpoints。

## Context
- 計劃參考：ProjectRecord/{active-project}/planner/outbox/task-001-reply.md
- 代碼輸出位置：ProjectRecord/{active-project}/output/src/routes/todo.ts
- 需要包含：路由定義 + Controller + Service + Model

## 預期輸出
完整可運行嘅代碼文件，放喺 ProjectRecord/{active-project}/output/ 目錄
```

### 實例 3：Evaluate Request

```markdown
# Task 003

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-27T11:30:00+08:00
- **Type**: evaluate-request

## 需求
審查 Generator 產出嘅 Todo API 代碼。

## Context
- 代碼位置：ProjectRecord/{active-project}/output/src/routes/todo.ts
- 原始需求：ProjectRecord/{active-project}/planner/outbox/task-001-reply.md
- Generator 回覆：ProjectRecord/{active-project}/generator/outbox/task-002-reply.md

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
```
