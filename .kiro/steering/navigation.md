---
inclusion: always
description: Root Agent 文件清單 + 幾時讀（L1 - 永遠載入）
---

# Root Agent 文件導航

| 文件 | L層 | inclusion | 幾時讀 |
|------|-----|-----------|--------|
| `role.md` | L1 | always | 身份 + 核心規則（自動載入） |
| `navigation.md` | L1 | always | 本文件（自動載入） |
| `tools.md` | L2 | always | 工具權限（自動載入） |
| `deterministic-first.md` | L2 | always | 確定性任務用腳本原則（自動載入） |
| `anti-amnesia.md` | L1 | always | 防失憶規則（自動載入） |
| `role-execution.md` | L3 | manual | 操作流程 / Integration Testing |
| `role-constraints.md` | L3 | manual | 文件放置規則 / 行為邊界 |
