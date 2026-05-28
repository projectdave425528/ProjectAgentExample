---
inclusion: manual
description: Planner Agent 輸出格式模板（L3 - 手動載入）
---

# Planner 輸出格式

## 1. 方案摘要模板

```markdown
## 方案摘要

- **目標**: [一句話描述]
- **技術棧**: [語言 + 框架 + DB]
- **預估任務數**: [N 個]
- **預估複雜度**: [低/中/高]
```

---

## 2. 架構圖格式（Mermaid）

```markdown
## 架構圖

​```mermaid
graph TD
    A[用戶] --> B[前端]
    B --> C[API]
    C --> D[數據庫]
​```
```

### 架構圖規則
- 必須用 Mermaid 格式
- 節點命名要清晰（唔好用 A、B、C）
- 標示數據流方向
- 複雜系統可用 subgraph 分組

---

## 3. 任務清單格式

```markdown
## 任務清單

| # | 任務 | 依賴 | Acceptance Criteria | Test Criteria |
|---|------|------|---------------------|---------------|
| 1 | ... | 無 | ... | Happy: ... / Error: ... / Edge: ... |
| 2 | ... | #1 | ... | Happy: ... / Error: ... / Edge: ... |
| 3 | ... | #1, #2 | ... | Happy: ... / Error: ... / Edge: ... |
```

### 任務清單規則
- 每個任務必須有 Acceptance Criteria
- **每個任務必須有 Test Criteria**（Happy Path + Error Path + Edge Case）
- 依賴關係要明確標示
- 任務粒度：Generator 可以喺一次迭代內完成
- 排序：按依賴順序（無依賴嘅排前面）
- **可測試性**：每個任務嘅 scope 要細到可以寫獨立 unit test

### Test Criteria 格式
每個 Task 嘅 Test Criteria 必須包含：
```markdown
**Happy Path:**
- [正常輸入] → [預期輸出]

**Error Path:**
- [錯誤輸入] → [預期錯誤處理]

**Edge Case:**
- [邊界值] → [預期行為]
- [null/empty] → [預期行為]
```

---

## 4. 風險評估格式

```markdown
## 風險評估

| 風險 | 可能性 | 影響 | 緩解方案 |
|------|--------|------|----------|
| ... | 高/中/低 | 高/中/低 | ... |
```

### 風險分類
| 類型 | 例子 |
|------|------|
| 技術風險 | 框架唔支援某功能 |
| 依賴風險 | 第三方 API 唔穩定 |
| 安全風險 | 涉及敏感數據處理 |
| 時間風險 | 工作量超出預期 |

---

## 5. 完整回覆模板

一個完整嘅 Planner 回覆應包含以下所有部分：

```markdown
---
task-id: "assignment-{id}"
from: planner
to: main-agent
type: assignment-reply
timestamp: YYYY-MM-DD HH:mm
status: done
---

## 方案摘要
[...]

## 架構圖
[Mermaid 圖]

## 任務清單
[表格]

## 風險評估
[表格]

## 備註
[任何額外說明]
```
