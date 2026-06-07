---
inclusion: manual
description: Generator 角色限制 + Blocked 報告 + 操作模式（L3 - 手動載入）
---

# Generator 角色限制

## Scope 限制（必須遵守，零例外）
- ❌ 唔好修改 Assignment scope 以外嘅文件或功能
- ❌ 唔好順手 refactor 唔相關嘅 code
- ❌ 唔好改動已存在嘅 function signature（除非 Assignment 要求）
- ❌ 唔好刪除本身存在嘅 dead code
- ✅ 你造成嘅 orphan → 要刪
- ✅ 發現其他問題 → 喺 outbox reply 備註

## Blocked 報告格式

```markdown
## Blocked Report

**Task ID**: assignment-{id}
**Blocked 原因**: [具體原因]

### 已嘗試
1. [嘗試 1] → 結果：[失敗原因]
2. [嘗試 2] → 結果：[失敗原因]
3. [嘗試 3] → 結果：[失敗原因]

### 需要幫助
- [具體需要咩]

### 建議
- [替代方案]
```

## CLI 模式 vs Multi-Window 模式

| 任務複雜度 | 推薦模式 | 適合 |
|-----------|----------|------|
| 單文件修改 | CLI | 簡單任務、快速迭代 |
| 多文件 CRUD | CLI / Multi-Window | 中等複雜度 |
| 全新模組開發 | Multi-Window | 需要大量 context |
| 需要大量自學 | Multi-Window | 複雜任務 |
