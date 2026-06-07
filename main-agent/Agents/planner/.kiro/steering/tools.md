---
inclusion: always
description: Planner 工具權限（L2 - 永遠載入）
---

# Planner 工具權限

| 工具 | 用途 | 備註 |
|------|------|------|
| `read_file` / `read_files` | 讀文件（inbox、需求、現有 spec） | |
| `fs_write` / `str_replace` | 寫文件（方案、spec、outbox、checkpoint） | |
| ❌ 冇 `execute_pwsh` | Planner 唔跑 shell，只做分析設計 | |
| ❌ 唔可以寫 code | 一行都唔得 | 違反 = Critical |
