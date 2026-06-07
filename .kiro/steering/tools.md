---
inclusion: always
description: Root Agent 工具權限（L2 - 永遠載入）
---

# Root Agent 工具權限

| 工具 | 用途 | 備註 |
|------|------|------|
| `read_file` / `read_files` | 讀取任何文件 | |
| `fs_write` / `str_replace` | 建立/修改文件 | |
| `execute_pwsh` | 跑 shell command | 必須加 timeout: 600000 |
| `grep_search` / `file_search` | 搜尋文件內容/路徑 | |
| `invoke_sub_agent` | 調用 sub-agent | |
| `remote_web_search` / `web_fetch` | 上網搜尋 | |

## 行為限制
- 操作前先確認目標文件／目錄是否存在
- 唔好自動刪除文件，需用戶確認
- 唔好假設工具已安裝，先確認
- 唔好修改 workspace 外的文件（需明確授權）
