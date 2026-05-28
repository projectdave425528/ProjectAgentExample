# Verdict: Task {id}

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: {ISO timestamp}
- **Verdict**: PASS | FAIL | REPLAN

## 評分
| 維度 | 權重 | 分數 |
|------|------|------|
| 功能 | 40% | {score} |
| 品質 | 30% | {score} |
| 安全 | 20% | {score} |
| 維護 | 10% | {score} |
| **總分** | | **{total}** |

## 問題清單
- {issue 1}
- {issue 2}

## 修改建議
- {suggestion 1}
- {suggestion 2}

## Memory 已更新
✅ / ❌

---

## 實例

### 實例 1：PASS

```markdown
# Verdict: Task 003

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: 2026-05-27T11:45:00+08:00
- **Verdict**: PASS

## 評分
| 維度 | 權重 | 分數 |
|------|------|------|
| 功能 | 40% | 90 |
| 品質 | 30% | 85 |
| 安全 | 20% | 80 |
| 維護 | 10% | 85 |
| **總分** | | **86** |

## 問題清單
- 缺少 input validation 嘅 edge case（空字串）
- 建議加 rate limiting

## 修改建議
- 加 express-validator 做 input sanitization
- 考慮加 helmet middleware

## Memory 已更新
✅
```

### 實例 2：FAIL

```markdown
# Verdict: Task 003

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: 2026-05-27T12:00:00+08:00
- **Verdict**: FAIL

## 評分
| 維度 | 權重 | 分數 |
|------|------|------|
| 功能 | 40% | 70 |
| 品質 | 30% | 60 |
| 安全 | 20% | 50 |
| 維護 | 10% | 65 |
| **總分** | | **63** |

## 問題清單
- DELETE endpoint 冇做 ownership check（任何人可以刪其他人嘅 Todo）
- SQL query 用 string concatenation（SQL injection 風險）
- 冇 error handling middleware
- 函數超過 50 行（違反代碼規範）

## 修改建議
- 加 ownership validation：`WHERE user_id = req.user.id`
- 改用 parameterized queries
- 加 global error handler
- 拆分大函數成 helper functions

## Memory 已更新
✅
```

### 實例 3：REPLAN

```markdown
# Verdict: Task 003

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: 2026-05-27T12:15:00+08:00
- **Verdict**: REPLAN

## 評分
| 維度 | 權重 | 分數 |
|------|------|------|
| 功能 | 40% | 40 |
| 品質 | 30% | 50 |
| 安全 | 20% | 30 |
| 維護 | 10% | 45 |
| **總分** | | **41** |

## 問題清單
- 架構設計有根本問題：直接喺 route handler 寫 DB query，冇分層
- 完全冇認證機制
- 冇 error handling
- 代碼結構唔符合計劃嘅分層架構

## 修改建議
- 需要重新規劃：原計劃嘅分層架構未被遵守
- 建議 Planner 重新出一份更詳細嘅實現指引
- 明確列出每個文件嘅職責同 interface

## Memory 已更新
✅
```
