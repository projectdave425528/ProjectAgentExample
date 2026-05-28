# Requirements: {spec-name}

## 概述
{一句話描述呢個 feature / 系統要做咩}

## User Stories

### US-{id}: {title}
- **As a** {角色}
- **I want** {功能}
- **So that** {價值}

#### Acceptance Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}
- [ ] {criterion 3}

## System Behaviors (EARS Notation)

### {Feature Area}

WHEN {condition}
THE SYSTEM SHALL {expected behavior}

WHEN {condition}
THE SYSTEM SHALL {expected behavior}

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | {描述} | Must | |
| FR-002 | {描述} | Should | |
| FR-003 | {描述} | Could | |

## Non-Functional Requirements

| ID | Type | Requirement | Criteria |
|----|------|-------------|----------|
| NFR-001 | Performance | {描述} | {量化標準} |
| NFR-002 | Security | {描述} | {量化標準} |

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|-------------------|
| {edge case} | {system response} |

## Constraints
- {技術約束}
- {業務約束}

## Out of Scope
- {明確唔做嘅嘢}

---

## 實例

### 實例 1：Todo API Requirements

```markdown
# Requirements: Todo CRUD API

## 概述
為現有用戶系統加入 Todo List 管理功能，支援完整 CRUD 操作。

## User Stories

### US-001: 建立 Todo
- **As a** 已登入用戶
- **I want** 建立新嘅 Todo item
- **So that** 我可以記錄待辦事項

#### Acceptance Criteria
- [ ] 可以設定 title（必填，最長 200 字）
- [ ] 可以設定 description（選填）
- [ ] 可以設定 due date（選填）
- [ ] 建立後自動設為 pending 狀態

### US-002: 列出 Todo
- **As a** 已登入用戶
- **I want** 睇到自己所有 Todo items
- **So that** 我可以追蹤進度

#### Acceptance Criteria
- [ ] 只顯示自己嘅 Todo（唔會睇到其他人嘅）
- [ ] 支援按 status 篩選
- [ ] 支援分頁（每頁 20 條）

## System Behaviors (EARS Notation)

### Todo Creation

WHEN a user submits valid todo data with a title
THE SYSTEM SHALL create a new todo item with status "pending"

WHEN a user submits a title exceeding 200 characters
THE SYSTEM SHALL reject the request with a validation error

WHEN a user submits without a title
THE SYSTEM SHALL return a 400 error indicating title is required

### Todo Listing

WHEN a user requests their todo list
THE SYSTEM SHALL return only todos belonging to that user

WHEN a user filters by status
THE SYSTEM SHALL return only todos matching the specified status

### Authorization

WHEN a user attempts to access another user's todo
THE SYSTEM SHALL return a 403 forbidden error

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | Create Todo | Must | POST /api/todos |
| FR-002 | List Todos | Must | GET /api/todos |
| FR-003 | Update Todo | Must | PUT /api/todos/:id |
| FR-004 | Delete Todo | Must | DELETE /api/todos/:id |
| FR-005 | Filter by status | Should | query param: ?status=pending |

## Non-Functional Requirements

| ID | Type | Requirement | Criteria |
|----|------|-------------|----------|
| NFR-001 | Performance | API response time | < 200ms (p95) |
| NFR-002 | Security | User isolation | Users can only access own todos |

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|-------------------|
| Empty title | Return 400 with "title is required" |
| Title > 200 chars | Return 400 with "title too long" |
| Invalid due_date format | Return 400 with "invalid date format" |
| Todo not found | Return 404 |
| Unauthorized access | Return 403 |

## Constraints
- Tech stack: Node.js + Express + PostgreSQL
- Must use existing User model as foreign key
- Deployment: Docker + AWS ECS

## Out of Scope
- Shared todos (collaboration)
- File attachments
- Reminder notifications
```
