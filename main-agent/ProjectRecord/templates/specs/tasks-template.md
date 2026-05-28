# Tasks: {spec-name}

## Task List

### Task 1: {title}
- **Status**: pending | in_progress | completed | blocked
- **Required**: yes | no
- **Depends on**: {task number | none}

**Description**: {具體要做咩}

**Expected Outcome**:
- [ ] {verifiable outcome 1}
- [ ] {verifiable outcome 2}

**Output Files**:
- `{file path}`

---

### Task 2: {title}
- **Status**: pending
- **Required**: yes | no
- **Depends on**: Task 1

**Description**: {具體要做咩}

**Expected Outcome**:
- [ ] {verifiable outcome 1}
- [ ] {verifiable outcome 2}

**Output Files**:
- `{file path}`

---

## 實例

### 實例 1：Todo API Tasks

```markdown
# Tasks: Todo CRUD API

## Task List

### Task 1: Create Database Migration
- **Status**: pending
- **Required**: yes
- **Depends on**: none

**Description**: 用 Prisma 建立 Todo table 嘅 migration file，包含所有 design 定義嘅 fields。

**Expected Outcome**:
- [ ] Migration file 存在
- [ ] Schema 包含所有 design 定義嘅 fields
- [ ] Foreign key 正確指向 User table
- [ ] `npx prisma migrate dev` 成功執行

**Output Files**:
- `prisma/migrations/xxx_add_todo_table/migration.sql`
- `prisma/schema.prisma`

---

### Task 2: Implement Todo Repository
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 1

**Description**: 實作 Todo 嘅 data access layer，封裝所有 Prisma 操作，包含 CRUD 同 pagination。

**Expected Outcome**:
- [ ] CRUD 四個方法都有實作
- [ ] 所有 query 都有 user_id 過濾（安全隔離）
- [ ] Cursor-based pagination 正確實作
- [ ] TypeScript 類型完整

**Output Files**:
- `src/modules/todo/todo.repository.ts`
- `src/modules/todo/todo.types.ts`

---

### Task 3: Implement Todo Service
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 2

**Description**: 實作業務邏輯層，包含 Zod validation 同 authorization checks。

**Expected Outcome**:
- [ ] Input validation 用 Zod schema
- [ ] 權限檢查（只能操作自己嘅 Todo）
- [ ] Error handling 完整
- [ ] Service 唔直接依賴 Prisma（透過 Repository）

**Output Files**:
- `src/modules/todo/todo.service.ts`
- `src/modules/todo/todo.schema.ts`

---

### Task 4: Implement Todo Route + Controller
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 3

**Description**: 實作 Express route 同 controller，連接 Service 層，處理 HTTP request/response。

**Expected Outcome**:
- [ ] 四個 endpoints 都有實作（POST/GET/PUT/DELETE）
- [ ] Auth middleware 正確套用
- [ ] Request validation 喺 controller 層處理
- [ ] Response format 符合 design spec

**Output Files**:
- `src/modules/todo/todo.route.ts`
- `src/modules/todo/todo.controller.ts`

---

### Task 5: Write Unit Tests
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 4

**Description**: 為 Service 同 Repository 層寫 unit tests，確保核心邏輯正確。

**Expected Outcome**:
- [ ] Service layer tests cover happy path + error cases
- [ ] Repository layer tests with mocked Prisma
- [ ] All tests pass
- [ ] Coverage > 80%

**Output Files**:
- `src/modules/todo/__tests__/todo.service.test.ts`
- `src/modules/todo/__tests__/todo.repository.test.ts`

---

### Task 6: Write Integration Tests
- **Status**: pending
- **Required**: no
- **Depends on**: Task 5

**Description**: 用 Supertest 寫 API integration tests，測試完整 request flow。

**Expected Outcome**:
- [ ] All CRUD endpoints tested
- [ ] Auth scenarios tested (valid/invalid/missing token)
- [ ] Error responses match expected format
- [ ] Pagination tested

**Output Files**:
- `src/modules/todo/__tests__/todo.integration.test.ts`
```
