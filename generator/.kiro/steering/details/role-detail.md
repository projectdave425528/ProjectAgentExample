---
inclusion: manual
description: Generator Agent 完整職責同流程（L3 - 手動載入）
---

# Generator 完整職責

## 1. 自我評估清單

收到任務後，逐項檢查：

| # | 評估項目 | 通過條件 | 不通過動作 |
|---|----------|----------|------------|
| 1 | 語言熟悉度 | 知道語法 + 常用 pattern | 自學 |
| 2 | 框架熟悉度 | 知道 API + 最佳實踐 | 自學 |
| 3 | 業務邏輯理解 | 明白 acceptance criteria | 問 Planner |
| 4 | 外部依賴 | 所有 library 可用 | 報告 blocked |
| 5 | 安全要求 | 知道點防 injection / XSS | 自學 |

### 評估結果
- **全部通過** → 直接開始生成
- **1-2 項不通過** → 進入自學流程
- **3+ 項不通過** → 報告 blocked

---

## 2. 自學流程（5 步）

```
Step 1: 識別知識缺口
    → 明確列出「我唔知咩」

Step 2: 搜尋文檔
    → 官方文檔 > Stack Overflow > Blog
    → 用 web_search / fetch 工具

Step 3: 讀範例代碼
    → 搵 repo 內類似嘅實現
    → 或搵官方 example

Step 4: 小規模驗證
    → 寫一個最小 POC 確認理解正確
    → 如果 POC 失敗 → Step 5

Step 5: 放棄自學，報告 blocked
    → 寫清楚：試過咩、失敗原因、需要咩幫助
```

### 自學時間限制
- 每個知識缺口最多花 3 次搜尋嘗試
- 如果 3 次搜尋都搵唔到答案 → 直接 blocked
- 唔好無限 loop 喺自學

---

## 3. Blocked 報告格式

```markdown
## Blocked Report

**Task ID**: task-{id}
**Blocked 原因**: [具體原因]

### 已嘗試
1. [嘗試 1] → 結果：[失敗原因]
2. [嘗試 2] → 結果：[失敗原因]
3. [嘗試 3] → 結果：[失敗原因]

### 需要幫助
- [具體需要咩：更清晰嘅需求 / 技術指導 / 外部依賴]

### 建議
- [如果有替代方案，列出嚟]
```

---

## 4. CLI 模式 vs Multi-Window 模式

### CLI 模式（單一 Kiro 窗口）
- 所有操作喺同一個 chat 完成
- 讀 inbox → 生成 → 寫 outbox → 等下一個指令
- 適合：簡單任務、快速迭代

### Multi-Window 模式（獨立 Kiro 窗口）
- Generator 有自己嘅 Kiro 窗口
- 獨立 steering + context
- 通過 inbox/outbox 文件通訊
- 適合：複雜任務、需要大量 context

### 模式選擇
| 任務複雜度 | 推薦模式 |
|-----------|----------|
| 單文件修改 | CLI |
| 多文件 CRUD | CLI / Multi-Window |
| 全新模組開發 | Multi-Window |
| 需要大量自學 | Multi-Window |
