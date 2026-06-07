---
inclusion: manual
description: Planner 任務執行流程（L3 - 手動載入）
---

# Planner 任務執行流程

> 設計方案前必讀。包含可測試性設計規則、Specs 產出規則。

## 啟動流程
1. 讀 `./ProjectRecord/active-project.md` → 確認當前 Project
2. 讀 `./ProjectRecord/{active-project}/inbox/planner/assignment-{id}.md` → 取得需求
3. 建立 Checkpoint（見 `project-protocols-checkpoint.md`）
4. 讀 `../../.kiro/skills/clean-code/SKILL.md` → Clean Code 設計原則（重點：SRP、可測試性、抽象層級）
5. 讀 `../../.kiro/skills/design-patterns/SKILL.md`（Part A）→ 方案設計嘅 Pattern 選擇
6. 分析需求 → 設計方案（遵守可測試性設計規則）
6. 每完成一個主要步驟 → 更新 Checkpoint 執行記錄
7. 按 `./ProjectRecord/templates/assignment-reply-template.md` 格式寫 outbox reply
8. 更新 Checkpoint → completed，重命名文件

## 可測試性設計規則（必須遵守）

### 任務拆分原則
1. **單一職責** — 每個 Task 只做一件事，方便寫獨立 test
2. **明確 Input/Output** — 每個 Task 嘅 acceptance criteria 必須定義：
   - Input：咩數據 / 參數進去
   - Output：期望咩結果出嚟
   - Edge Cases：至少列 2 個邊界情況
3. **無隱藏依賴** — Task 之間嘅依賴要用 interface / abstraction 隔開
4. **可 Mock 嘅外部依賴** — 涉及 DB / API / File 嘅 Task，設計時要預留 interface 方便 mock

### Test Criteria 寫法
每個 Task 嘅 Test Criteria 必須包含：
- **Happy Path**: 正常情況下嘅預期行為（至少 1 個）
- **Error Path**: 錯誤情況下嘅預期行為（至少 1 個）
- **Edge Case**: 邊界情況（至少 1 個）
- **Integration Point**: 同其他模組/服務嘅互動驗證（如適用）

### 任務清單格式
```markdown
| # | 任務 | 依賴 | Acceptance Criteria | Test Criteria | Integration Points |
|---|------|------|---------------------|---------------|--------------------|
| 1 | ... | 無 | ... | Happy/Error/Edge | 同邊啲模組互動 |
```

### Integration Testing 設計規則
1. **識別 Integration Point** — 每個 Task 列出同邊啲模組/服務有互動
2. **定義 Integration Test Scenario** — 端到端嘅數據流同預期行為
3. **環境要求** — 列出 integration test 需要嘅環境
4. **隔離策略** — test container / in-memory DB / mock API

### 架構設計要求
- 業務邏輯同 infrastructure 必須分層
- 每層之間用 interface 連接
- 推薦模式：Controller → Service → Repository（interface）→ DB

## Specs 產出規則

### 當 Assignment 要求產出 Specs 時
1. 讀取 `./ProjectRecord/templates/specs/` 入面嘅 template
2. 按 template 格式產出三份文件
3. 寫入 `./ProjectRecord/{active-project}/specs/`：
   - `requirements.md`
   - `design.md`
   - `tasks.md`
4. 同時寫 outbox assignment reply
5. Reply 嘅「結果」section 列出已產出嘅 Specs 文件路徑
