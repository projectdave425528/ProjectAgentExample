---
inclusion: manual
description: Root Agent 操作流程（L3 - 手動載入）
---

# Root Agent 操作流程

## Integration Testing
- 涉及多模組/服務互動嘅任務，必須考慮 Integration Test
- 觸發條件：2+ 模組互動、DB CRUD、API endpoint、message queue、file I/O 配合
- Planner 識別 Integration Points → Generator 寫 Integration Test → Evaluator 驗證
