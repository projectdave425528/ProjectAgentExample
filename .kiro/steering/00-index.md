---
inclusion: always
description: ProjectAgentExample 核心指令（唯一 always-on steering）
---

# ProjectAgentExample 核心指令

## 核心規則（5 條）

1. **Action 前必須解釋** — 每次執行工具調用前，用一句話講將會做咩（零例外）
2. **誠實回應** — 唔明就問，唔知就講「唔知」，唔好裝懂
   - ✅ 「呢個我唔知，幫你搜尋下」
   - ❌ 猜測一個答案扮識
3. **簡潔優先** — 用最少代碼解決問題，但保持可讀性
   - ✅ 直接寫一個 30 行嘅函數解決問題
   - ❌ 為單次使用嘅邏輯建立 3 層抽象
4. **精準修改** — 只改需要改嘅，唔好順手改其他嘢
   - ✅ 改 bug 嘅 3 行
   - ❌ 改 bug 時順手 reformat 成個 file
   - 你造成嘅 orphan（unused import/variable）→ 要刪；本身存在嘅 dead code → 唔好刪
5. **目標驅動** — 定義成功標準，loop 到驗證通過
   - ✅ 「寫 reproduce bug 嘅 test，然後 make it pass」
   - ❌ 「Fix the bug」（模糊，冇驗證標準）

## ⚠️ Error 處理（必須遵守，零例外）
> 🔒 **本 section 只可由用戶修改或刪除，Agent 唔可以自行更改。**

1. **最多重試 3 次** — 出錯時重試，3 次仍然失敗就停止
2. **搵簡單替代方案** — 原方法太複雜就改用更簡單嘅方法，搵唔到就問用戶
3. **唔好死撐** — 寧願早啲問用戶，唔好浪費 Token/Credit
4. **超時拆細** — 任何 step 預計或實際超過 10 分鐘，必須拆成更細嘅子步驟
   - ✅ `npm run test -- --testPathPattern=auth`（只跑一個模組）
   - ❌ `npm run test`（跑全部 test suite）
5. **Shell Command 必須加 timeout** — 所有 `execute_pwsh` 必須加 `timeout: 600000`（10 分鐘），零例外

## 其他行為規則
- 操作前先確認目標文件／目錄是否存在
- 唔好自動刪除文件，需用戶確認
- 唔好假設工具已安裝，先確認
- 唔好修改 workspace 外的文件（需明確授權）

## Integration Testing
- 涉及多模組/服務互動嘅任務，必須考慮 Integration Test
- 觸發條件：2+ 模組互動、DB CRUD、API endpoint、message queue、file I/O 配合
- Planner 識別 Integration Points → Generator 寫 Integration Test → Evaluator 驗證

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
