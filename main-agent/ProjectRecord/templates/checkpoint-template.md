# Checkpoint: Assignment {id}

- **Agent**: {agent-name}
- **TaskRef**: Task {task-number}: {task-title}
- **TaskID**: {active-project}/Task-{task-number}
- **Started**: {ISO timestamp}
- **Last Updated**: {ISO timestamp}
- **Status**: in_progress | completed | cancelled | blocked

## 文件命名規則
> `checkpoint-A{id}-{agent}-{status}.md`
> 例如：`checkpoint-A008-generator-in_progress.md`
> 完成後重命名：`checkpoint-A008-generator-completed.md`

---

## 計劃（開始前填寫）
### 打算做咩
{列出呢個 assignment 要完成嘅所有步驟}

### 預計產出文件
- `{file path 1}`
- `{file path 2}`

### 依賴
- {需要讀取嘅文件/模組}

---

## 執行記錄（每完成一步 append）

| # | 時間 | 步驟 | 狀態 | 備註 |
|---|------|------|------|------|
| 1 | {HH:MM} | {做咗咩} | ✅/❌/⏳ | {額外資訊} |

---

## 思考過程（遇到問題時記錄）

### {問題描述}
- **遇到咩**：{描述}
- **考慮過嘅方案**：{方案 A / B / C}
- **最終決定**：{選擇 + 原因}

---

## 最終狀態

- **產出文件**：{實際寫咗嘅文件列表}
- **測試結果**：{pass/fail 數量}
- **未完成項目**：{如果 cancelled/blocked，列出未做嘅嘢}
- **下一步建議**：{俾 Main Agent 嘅恢復指引}
