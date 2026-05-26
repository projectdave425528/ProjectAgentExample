---
## [{timestamp}] {from} → {to}

**Type**: {message-type}
**Status**: {status}
**Summary**: {一句話摘要}

---

## 實例

### 實例 1：調用 Planner

```markdown
---
## [2026-05-27T10:30:00+08:00] main-agent → planner

**Type**: plan-request
**Status**: dispatched
**Summary**: 派發 Todo API 設計任務俾 Planner
```

### 實例 2：Planner 回覆

```markdown
---
## [2026-05-27T10:45:00+08:00] planner → main-agent

**Type**: plan-reply
**Status**: completed
**Summary**: Planner 完成 Todo API 架構設計，建議分 5 個子任務
```

### 實例 3：Evaluator 判定 FAIL

```markdown
---
## [2026-05-27T12:00:00+08:00] evaluator → main-agent

**Type**: verdict
**Status**: FAIL (63/100)
**Summary**: 代碼有 SQL injection 風險 + 缺少 ownership check，需要 Generator 修正
```

### 實例 4：用戶介入

```markdown
---
## [2026-05-27T12:30:00+08:00] user → main-agent

**Type**: user-command
**Status**: received
**Summary**: 用戶要求跳過認證功能，先交付基本 CRUD
```
