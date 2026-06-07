---
inclusion: manual
description: Main Agent 格式一致性規則（L3 - 手動載入）
---

# 格式一致性規則（必須遵守，零例外）

## 自己寫 assignment 時
1. **先讀取 `./ProjectRecord/active-project.md`** → 確認當前 Project 名稱
2. **寫 inbox assignment 前**：先讀 `./ProjectRecord/templates/assignment-template.md`
3. **寫 conversation-log 前**：先讀 `./ProjectRecord/templates/conversation-log-entry-template.md`
4. **寫入後更新 SearchIndex**：append 一行，格式參照 `./ProjectRecord/templates/search-index-entry-template.md`

## 驗證 Agent 回覆時
1. 對照 `./ProjectRecord/templates/assignment-reply-template.md` 驗證
2. 缺少必要欄位 → 退回重寫（計入重試次數）
3. 格式正確 → 繼續流程

## SearchIndex 維護
- **SearchIndex 由 Main Agent 統一維護** — Sub Agent 唔好直接寫
- Main Agent 收到任何 inbox/outbox 寫入後，自行 append
- SearchIndex 唔存在或損壞 → 重建（掃描所有 frontmatter）
