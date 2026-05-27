# Assignment Reply: {id}

- **From**: {agent-name}
- **To**: main-agent
- **Timestamp**: {ISO timestamp}
- **AssignmentStatus**: completed | blocked | verdict-pass | verdict-fail | verdict-replan | escalation
- **TaskRef**: Task {task-number}: {task-title}
- **TaskID**: {spec-name}/Task-{task-number}
- **TaskStatus**: in_progress → completed | blocked

## 驗證標準
- [x] {已完成嘅 outcome}
- [ ] {未完成嘅 outcome}

## 結果
{Agent 嘅回覆內容}

## 備註
{任何額外資訊}

## Memory 已更新
✅ / ❌

---

## AssignmentStatus 說明

| Status | 用途 | 使用者 | 文件名後綴 |
|--------|------|--------|-----------|
| completed | 任務完成 | Planner / Generator | `-reply-completed.md` |
| blocked | 無法完成，需要幫助 | Generator | `-reply-blocked.md` |
| verdict-pass | 代碼通過（≥80分） | Evaluator | `-reply-verdict.md` |
| verdict-fail | 代碼需修改（60-79分） | Evaluator | `-reply-verdict.md` |
| verdict-replan | 方案需重設計（<60分） | Evaluator | `-reply-verdict.md` |
| escalation | 需要用戶決定 | Planner | `-reply-escalation.md` |

---

## 實例

### 實例 1：Planner 完成（AssignmentStatus: completed）

```markdown
# Assignment Reply: 001

- **From**: planner
- **To**: main-agent
- **Timestamp**: 2026-05-27T10:45:00+08:00
- **AssignmentStatus**: completed
- **TaskRef**: Task 1: 設計 Todo API 架構
- **TaskID**: TodoCRUD/Task-1
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] 方案摘要包含技術棧選擇
- [x] 架構圖用 Mermaid 格式
- [x] 任務清單每項有 acceptance criteria
- [x] 風險評估至少 2 項

## 結果

### 方案摘要
建立 RESTful Todo API，支援 CRUD + JWT 認證。採用分層架構（Route → Controller → Service → Model）。

### 架構圖
```
Client → Auth Middleware → Router → Controller → Service → Model → PostgreSQL
```

### 任務清單
1. 建立 Todo Model（schema + migration）
2. 實現 CRUD Service 層
3. 實現 Controller + 路由
4. 加入 Auth Middleware 驗證
5. 寫 Integration Tests

### 風險評估
| 風險 | 影響 | 緩解 |
|------|------|------|
| DB Migration 失敗 | 高 | 先寫 rollback script |
| JWT Token 過期處理 | 中 | 加 refresh token 機制 |

## 備註
建議先做 Assignment 1-3，再加認證。

## Memory 已更新
✅
```

### 實例 2：Generator Blocked（AssignmentStatus: blocked）

```markdown
# Assignment Reply: 002

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-27T11:15:00+08:00
- **AssignmentStatus**: blocked
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: in_progress → blocked

## 驗證標準
- [ ] CRUD 四個方法都有實作
- [ ] 所有 query 都有 user_id 過濾
- [ ] TypeScript 類型完整

## 結果
無法完成代碼生成。

### 已嘗試
1. 搜尋 .env 文件 → 唔存在
2. 搜尋 src/models/ → 目錄為空
3. 搜尋 config/ → 冇 DB 相關設定

### 需要幫助
- PostgreSQL connection string（.env 入面冇定義）
- 現有 User model 嘅 schema（搵唔到 src/models/user.ts）

## 備註
請提供以上資訊或確認文件位置。

## Memory 已更新
✅
```

### 實例 3：Evaluator Verdict PASS（AssignmentStatus: verdict-pass）

```markdown
# Assignment Reply: 003

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: 2026-05-27T12:00:00+08:00
- **AssignmentStatus**: verdict-pass
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] 滿足 acceptance criteria
- [x] 函數 < 30 行、參數 ≤ 3
- [x] Parameterized Query
- [x] Input Validation
- [x] Error Handling

## 結果

### 評分：86/100

| 類別 | 得分 | 權重 | 加權分 |
|------|------|------|--------|
| 功能性 | 90 | 40% | 36 |
| 代碼品質 | 85 | 30% | 25.5 |
| 安全性 | 80 | 20% | 16 |
| 可維護性 | 85 | 10% | 8.5 |

### 優點
- 分層清晰，職責單一
- Parameterized query 正確使用

### 建議（非必須修改）
- 可以加 rate limiting middleware

## 備註
代碼合格，可以交付。

## Memory 已更新
✅
```

### 實例 4：Evaluator Verdict FAIL（AssignmentStatus: verdict-fail）

```markdown
# Assignment Reply: 003

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: 2026-05-27T12:00:00+08:00
- **AssignmentStatus**: verdict-fail
- **TaskRef**: Task 2: 實作 Todo Repository
- **TaskID**: TodoCRUD/Task-2
- **TaskStatus**: in_progress（FAIL，需要重做）

## 驗證標準
- [x] 滿足 acceptance criteria
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] Parameterized Query ← FAIL
- [ ] Input Validation ← FAIL
- [x] Error Handling

## 結果

### 評分：68/100

### 必須修改
| # | 問題 | 位置 | 修改建議 |
|---|------|------|----------|
| 1 | 缺少 input validation | todo.controller.ts:25 | 加 Zod schema |
| 2 | SQL injection 風險 | todo.repository.ts:42 | 改用 parameterized query |

### 修改優先順序
1. SQL injection（Critical）
2. Input validation

## 備註
修改後重新提交。

## Memory 已更新
✅
```

### 實例 5：Planner Escalation（AssignmentStatus: escalation）

```markdown
# Assignment Reply: 001

- **From**: planner
- **To**: main-agent
- **Timestamp**: 2026-05-27T10:30:00+08:00
- **AssignmentStatus**: escalation
- **TaskRef**: Task 1: 設計 Todo API 架構
- **TaskID**: TodoCRUD/Task-1
- **TaskStatus**: in_progress → blocked（等待用戶決定）

## 驗證標準
- [ ] 方案摘要包含技術棧選擇
- [ ] 架構圖用 Mermaid 格式

## 結果
需要用戶澄清以下問題：

1. 認證 scope：只需 JWT 定係要支援 OAuth2？
2. 多租戶：每個用戶獨立 DB 定係共用 DB + tenant_id？
3. 部署：需要支援 horizontal scaling 嗎？

## 備註
以上問題會影響架構設計，需要用戶決定先可以繼續。

## Memory 已更新
✅
```
