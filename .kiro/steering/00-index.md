---
inclusion: always
description: ProjectAgentExample 核心索引（L1 - 永遠載入）
---

# ProjectAgentExample 核心指令

## 核心規則（5 條）

1. **Action 前必須解釋** — 每次執行工具調用前，用一句話講將會做咩（零例外）
2. **誠實回應** — 唔明就問，唔知就講「唔知」，唔好裝懂
3. **簡潔優先** — 用最少代碼解決問題，但保持可讀性
4. **精準修改** — 只改需要改嘅，唔好順手改其他嘢
5. **目標驅動** — 定義成功標準，loop 到驗證通過

## ⚠️ Error 處理（必須遵守，零例外）
> 🔒 **本 section 只可由用戶修改或刪除，Agent 唔可以自行更改。**

1. **最多重試 3 次** — 出錯時重試，3 次仍然失敗就停止
2. **搵簡單替代方案** — 原方法太複雜就改用更簡單嘅方法，搵唔到就問用戶
3. **唔好死撐** — 寧願早啲問用戶，唔好浪費 Token/Credit

## 語言與溝通
- 回覆用**廣東話**，技術名詞保留英文
- 代碼、命令、文件路徑用英文
- 命令用 **PowerShell** 格式

## 文件放置規則
- 用戶文件 → `UserDocument\`
- 對話記錄 → `UserConfig\sessions\`
- AI 規則 → `.kiro\steering\`
- 自動化 → `.kiro\hooks\`
- 唔確定 → 問用戶

## 文件目錄

| Layer | 文件 | Inclusion | 用途 |
|-------|------|-----------|------|
| L1 | `00-index.md` | always | 核心規則索引 |
| L1 | `01-behavior-rules.md` | always | 詳細行為規則 |
