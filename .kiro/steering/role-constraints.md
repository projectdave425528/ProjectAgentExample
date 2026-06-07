---
inclusion: manual
description: Root Agent 文件放置規則 + 行為邊界（L3 - 手動載入）
---

# Root Agent 行為邊界

## 文件放置規則
- 用戶文件 → `UserDocument\`
- 對話記錄 → `UserConfig\sessions\`
- AI 規則 → `.kiro\steering\`
- 自動化 → `.kiro\hooks\`
- 唔確定 → 問用戶

## 其他行為規則
- 操作前先確認目標文件／目錄是否存在
- 唔好自動刪除文件，需用戶確認
- 唔好假設工具已安裝，先確認
- 唔好修改 workspace 外的文件（需明確授權）
