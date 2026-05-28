# Checkpoint: Assignment {id}

- **Agent**: {agent-name}
- **TaskRef**: Task {task-number}: {task-title}
- **TaskID**: {active-project}/Task-{task-number}
- **Started**: {ISO timestamp}
- **Last Updated**: {ISO timestamp}
- **Status**: in_progress | completed | cancelled | blocked

## 文件命名規則
> `checkpoint-A{id}-{agent}-{status}.md`
> 路徑：`./ProjectRecord/{active-project}/checkpoints/{agent}/`
> 例如：`checkpoints/generator/checkpoint-A008-generator-in_progress.md`
> 完成後重命名：`checkpoints/generator/checkpoint-A008-generator-completed.md`

---

## 計劃（開始前填寫）

### 打算做咩
{列出呢個 assignment 要完成嘅所有步驟，編號}

### 預計產出文件
- `{file path 1}`
- `{file path 2}`

### 依賴
- {需要讀取嘅文件/模組}

---

## 執行記錄（每完成一步必須 append，零例外）

> ⚠️ **每個實際操作都必須記錄，包括：寫文件、讀文件、跑 shell command、遇到問題、重試等。**
> **唔記錄 = 任務未完成。**

| # | 時間 | 操作類型 | 詳情 | 狀態 | 備註 |
|---|------|----------|------|------|------|
| 1 | {HH:MM} | {類型} | {具體內容} | ✅/❌/⏳/🔄 | {額外資訊} |

### 操作類型說明
| 類型 | 說明 | 詳情欄要記錄咩 |
|------|------|----------------|
| `write` | 寫入/建立文件 | 文件路徑 + 文件用途（一句話） |
| `read` | 讀取文件 | 文件路徑 + 讀取目的 |
| `shell` | 執行 shell command | 完整 command + 執行結果（exit code / output 摘要） |
| `decision` | 做技術決定 | 決定內容 + 原因（一句話） |
| `error` | 遇到錯誤 | 錯誤訊息 + 影響範圍 |
| `retry` | 重試操作 | 重試邊個操作 + 第幾次重試 + 結果 |
| `import` | Import/依賴確認 | 確認咗咩 module 可用 |
| `test` | 執行測試 | 測試命令 + pass/fail 數量 + 失敗嘅 test 名 |
| `rename` | 重命名文件/目錄 | 原路徑 → 新路徑 |
| `validate` | 驗證/檢查 | 驗證咩 + 結果 |

### 狀態符號
| 符號 | 意義 |
|------|------|
| ✅ | 成功完成 |
| ❌ | 失敗 |
| ⏳ | 進行中 |
| 🔄 | 重試中 |

---

## 問題同決策記錄（遇到問題時 append）

### 問題 {n}: {問題標題}
- **時間**：{HH:MM}
- **遇到咩**：{具體描述}
- **影響**：{會影響咩}
- **考慮過嘅方案**：
  - 方案 A：{描述}
  - 方案 B：{描述}
- **最終決定**：{選擇 + 原因}
- **重試次數**：{0/1/2/3}

---

## 最終狀態（完成時填寫）

### 產出文件清單
| # | 文件路徑 | 用途 |
|---|----------|------|
| 1 | `{path}` | {描述} |

### 測試結果
- **執行命令**：`{pytest command}`
- **結果**：{pass}/{total} tests passed
- **失敗嘅 tests**：{列出失敗嘅 test 名，如果全 pass 寫「無」}
- **執行時間**：{seconds}

### 統計
- **總操作數**：{執行記錄嘅行數}
- **成功操作**：{✅ 數量}
- **失敗操作**：{❌ 數量}
- **重試次數**：{🔄 總次數}
- **Shell commands 執行數**：{shell 類型嘅行數}

### 未完成項目（如果 cancelled/blocked）
- {列出未做嘅嘢}

### 下一步建議（俾 Main Agent 嘅恢復指引）
- {如果斷線，Main Agent 應該做咩}
