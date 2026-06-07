---
inclusion: always
description: Generator 工具權限（L2 - 永遠載入）
---

# Generator 工具權限

| 工具 | 用途 | 備註 |
|------|------|------|
| `read_file` / `read_files` | 讀文件（inbox、計劃、現有 code） | |
| `fs_write` / `str_replace` | 寫文件（生成 code、寫 outbox、checkpoint） | |
| `execute_pwsh` | 跑 shell（裝 dependency、本地驗證 test） | 先睇 `project-protocols-shell-policy.md` |
