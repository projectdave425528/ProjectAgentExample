# Reply: Task {id}

- **From**: {agent-name}
- **To**: main-agent
- **Timestamp**: {ISO timestamp}
- **Status**: completed | blocked | failed

## 結果
{Agent 嘅回覆內容}

## 備註
{任何額外資訊}

## Memory 已更新
✅ / ❌

---

## 實例

### 實例 1：Planner 完成回覆

```markdown
# Reply: Task 001

- **From**: planner
- **To**: main-agent
- **Timestamp**: 2026-05-27T10:45:00+08:00
- **Status**: completed

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
建議先做 Task 1-3，再加認證。

## Memory 已更新
✅
```

### 實例 2：Generator Blocked 回覆

```markdown
# Reply: Task 002

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-27T11:15:00+08:00
- **Status**: blocked

## 結果
無法完成代碼生成。

## 備註
需要以下資源先可以繼續：
1. PostgreSQL connection string（.env 入面冇定義）
2. 現有 User model 嘅 schema（搵唔到 src/models/user.ts）

請提供以上資訊或確認文件位置。

## Memory 已更新
✅
```
