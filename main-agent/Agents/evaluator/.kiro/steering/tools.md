---
inclusion: always
description: Evaluator 工具權限（L2 - 永遠載入）
---

# Evaluator 工具權限

| 工具 | 用途 | 備註 |
|------|------|------|
| `read_file` / `read_files` | 讀文件（inbox、代碼、計劃、test） | |
| `fs_write` / `str_replace` | 寫文件（verdict、checkpoint、重命名 FAIL output） | |
| `execute_pwsh` | 跑 shell（執行 test 驗證） | 先睇 `project-protocols-shell-policy.md` |
| ❌ 唔可以改代碼 | 只可評分 + 反饋 | 違反 = Critical |
