---
inclusion: always
description: Main Agent 工具權限（L2 - 永遠載入）
---

# Main Agent 工具權限

| 工具 | 用途 | 備註 |
|------|------|------|
| `read_file` / `read_files` | 讀文件（ProjectRecord、steering、specs） | |
| `fs_write` / `str_replace` | 寫文件（inbox assignment、conversation-log、checkpoint） | |
| `execute_pwsh` | 跑 shell | 先睇 `project-protocols-shell-policy.md`；限 Git/確認環境/取時間/kiro-cli |
| `invoke_sub_agent` | 調用 Sub Agent（fallback） | |
| ❌ 唔可以寫 production code | 交俾 Generator | |
| ❌ 唔可以做 code review | 交俾 Evaluator | |
| ❌ 唔可以跑 test | 交俾 Evaluator | |
