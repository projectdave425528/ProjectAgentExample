---
inclusion: manual
description: Assignment Message 範例集（L3 - 手動載入）。唔識格式時先讀，平時只需 assignment-template.md。
---

# Assignment Message 範例集

> 格式定義見 `../assignment-template.md`。本文件只係教學範例，需要時先讀。

## 實例 1：Plan Request

```markdown
# Assignment 001

- **From**: main-agent
- **To**: planner
- **Timestamp**: 2026-05-27T10:30:00+08:00
- **Type**: plan-request
- **TaskRef**: Task 1: 設計 Todo API 架構
- **TaskID**: TodoCRUD/Task-1
- **TaskStatus**: pending → in_progress

## 需求
幫我設計一個 REST API，用嚟管理用戶嘅 Todo List。需要支援 CRUD 操作同用戶認證。

## Context
- 技術棧：Node.js + Express + PostgreSQL
- 已有 User model，需要加 Todo model
- 部署環境：Docker + AWS ECS

## 驗證標準
- [ ] 方案摘要包含技術棧選擇
- [ ] 架構圖用 Mermaid 格式
- [ ] 任務清單每項有 acceptance criteria
- [ ] 風險評估至少 2 項

## 預期輸出
方案摘要 + 架構圖 + 任務清單 + 風險評估
```

## 實例 2：Generate Request

```markdown
# Assignment 002

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-27T11:00:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: pending → in_progress

## 需求
根據 Planner 嘅計劃，實現 Todo CRUD API endpoints。

## Context
- 計劃參考：ProjectRecord/{active-project}/outbox/planner/assignment-001-reply-completed.md
- 代碼輸出位置：ProjectRecord/{active-project}/output/src/routes/todo.ts
- 需要包含：路由定義 + Controller + Service + Model

## 驗證標準
- [ ] CRUD 四個方法都有實作
- [ ] 所有 query 都有 user_id 過濾
- [ ] TypeScript 類型完整
- [ ] 函數 < 30 行

## 預期輸出
完整可運行嘅代碼文件，放喺 ProjectRecord/{active-project}/output/ 目錄
```

## 實例 3：Evaluate Request

```markdown
# Assignment 003

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-27T11:30:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Todo API 代碼。

## Context
- 代碼位置：ProjectRecord/{active-project}/output/src/routes/todo.ts
- 原始需求：ProjectRecord/{active-project}/outbox/planner/assignment-001-reply-completed.md
- Generator 回覆：ProjectRecord/{active-project}/outbox/generator/assignment-002-reply-completed.md

## 驗證標準
- [ ] 滿足 acceptance criteria
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] Parameterized Query
- [ ] Input Validation
- [ ] Error Handling

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
```

## 實例 4：FAIL 後重新派發 Generator（新 Assignment）

```markdown
# Assignment 004

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-27T12:30:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: in_progress（FAIL 重做）

## 需求
修改 Todo CRUD API 代碼，解決 Evaluator 指出嘅問題。

## Context
- 原始計劃：ProjectRecord/{active-project}/outbox/planner/assignment-001-reply-completed.md
- 上次代碼：ProjectRecord/{active-project}/output/assignment-002/
- Evaluator FAIL 原因（Assignment 003）：
  1. 缺少 input validation（todo.controller.ts:25）→ 加 Zod schema
  2. SQL injection 風險（todo.repository.ts:42）→ 改用 parameterized query
- FAIL 次數：1/3

## 驗證標準
- [ ] Input validation 用 Zod schema（修復 #1）
- [ ] Parameterized query（修復 #2）
- [ ] 原有功能唔受影響

## 預期輸出
修改後嘅代碼文件，放喺 ProjectRecord/{active-project}/output/ 目錄
```

## 實例 5：REPLAN 後重新派發 Planner（新 Assignment）

```markdown
# Assignment 006

- **From**: main-agent
- **To**: planner
- **Timestamp**: 2026-05-27T14:00:00+08:00
- **Type**: plan-request
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: in_progress（REPLAN 重設計）

## 需求
重新設計 Todo API 方案。之前嘅方案經過 3 次 Generator 修改仍然無法通過 Evaluator。

## Context
- 原始需求：用戶要求 Todo CRUD API + JWT 認證
- 之前方案（Assignment 001）嘅問題：
  - 架構過於複雜，Generator 無法正確實作分層
  - Evaluator 連續 3 次 FAIL（Assignment 003/005/007）
- 建議方向：簡化架構，減少分層
- REPLAN 次數：1/2

## 驗證標準
- [ ] 方案比之前更簡單（減少分層）
- [ ] Generator 可以喺一次迭代內完成
- [ ] 保留所有原始功能需求

## 預期輸出
簡化後嘅方案摘要 + 架構圖 + 任務清單 + 風險評估
```
