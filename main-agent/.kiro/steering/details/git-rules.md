---
inclusion: manual
---

# Git 操作規則

## 核心原則

**唔好自動 commit。所有 Git 操作必須問用戶。**

## 完成任務後嘅流程

當任務 PASS 並交付後，問用戶：

```
任務已完成。你想點處理 Git？
1. Commit + Push（我幫你 commit 到當前 branch）
2. 新 Branch（我開新 branch 再 commit）
3. 唔做（保持 uncommitted 狀態）
```

### 選項 1：Commit + Push
1. `git add` 相關文件（唔好用 `git add .`）
2. 用標準格式寫 commit message
3. `git commit`
4. `git push`

### 選項 2：新 Branch
1. 問用戶 branch 名（或建議一個）
2. `git checkout -b {branch-name}`
3. `git add` 相關文件
4. `git commit`
5. `git push -u origin {branch-name}`

### 選項 3：唔做
- 乜都唔做，保持現狀

## Commit Message 格式

```
{type}: {簡短描述}

{詳細描述（可選）}
```

### Type 列表
| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修 bug |
| `refactor` | 重構（唔改功能） |
| `docs` | 文件更新 |
| `chore` | 雜項（配置、依賴等） |
| `test` | 測試相關 |

### 範例
```
feat: add user CRUD API endpoints

- POST /api/users (create)
- GET /api/users/:id (read)
- PUT /api/users/:id (update)
- DELETE /api/users/:id (delete)
```

## 禁止行為

- ❌ 自動 commit（冇問用戶就 commit）
- ❌ `git add .`（要指定文件）
- ❌ Force push（`git push -f`）
- ❌ 直接 push 到 main/master（除非用戶明確要求）
- ❌ `git reset --hard`
- ❌ 修改 `.gitignore` 而唔通知用戶
