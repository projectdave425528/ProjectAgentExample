# Multi-Agent 漸進式披露設計

> 將 Agent Steering 重構為三層架構，減少 Token 消耗
> 參考：Progressive_Disclosure_Framework.md
> 設計日期：2026-05-25

---

## 設計目標

| 目標 | 做法 |
|------|------|
| 減少 Token | 只載入 Index（< 50 行），需要時先讀 Detail |
| 減少 Credit | 每次對話唔需要載入完整 Steering |
| 清晰分類 | 角色規則 vs 通訊系統 vs 項目知識 分開 |
| 快速定位 | 用錨點 + 關鍵字搵到需要嘅內容 |

---

## 現有問題

```
而家：所有規則塞入一個 00-core-memory.md（~90 行）
     → 每次對話都載入全部
     → 大部分內容當次對話用唔到
     → 浪費 Token + Credit
```

---

## 新架構：三層漸進式披露

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Index（永遠載入）                                    │
│ 文件：00-index.md                                            │
│ 大小：< 50 行                                                │
│ 內容：角色一句話 + 文件目錄 + 關鍵字索引                       │
│ inclusion: always                                            │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Summary（需要時載入）                                │
│ 文件：01-role-summary.md / 02-comm-summary.md                │
│ 大小：< 100 行 each                                         │
│ 內容：規則摘要 + 錨點指向 Detail                              │
│ inclusion: manual（用 #引用 或 Agent 自己讀）                 │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Detail（執行時載入）                                 │
│ 文件：各種 detail-*.md                                       │
│ 大小：無限制                                                  │
│ 內容：完整規則 + 範例 + 模板                                  │
│ 載入方式：Agent 用 read_file 按需讀取                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Steering 文件重構計劃

### 現有 → 新結構

```
現有：
.kiro/steering/
├── 00-core-memory.md      ← 所有規則（~90 行，always）
└── 01-session-context.md  ← 進度記錄（~80 行，always）

新：
.kiro/steering/
├── 00-index.md            ← L1 Index（< 50 行，always）
├── 01-role-summary.md     ← L2 角色摘要（manual）
├── 02-comm-system.md      ← L2 通訊系統（manual）
├── 03-session-context.md  ← L2 進度記錄（manual，經常更新）
└── details/
    ├── role-detail.md     ← L3 完整角色規則
    ├── comm-detail.md     ← L3 通訊協議詳情
    ├── git-rules.md       ← L3 Git 操作規則
    └── spec-rules.md      ← L3 Spec 文件規則
```

---

## 00-index.md 設計（Layer 1 — 永遠載入）

```markdown
---
inclusion: always
---

# Main Agent (Orchestrator) — 索引

<!-- @index-main -->
[index] [orchestrator] [main-agent]

## 我係邊個
Multi-Agent 系統嘅 Orchestrator。接收需求 → 調用 Agent → 判斷結果 → 交付。

## 文件目錄
| # | 文件 | 內容 | 載入方式 |
|---|------|------|---------|
| 1 | 01-role-summary.md | 角色職責 + 調用規則 | #Role |
| 2 | 02-comm-system.md | Agent 通訊系統 + 路徑 | #Comm |
| 3 | 03-session-context.md | 項目進度 + 環境 | #Session |
| 4 | details/role-detail.md | 完整角色規則 | read_file |
| 5 | details/comm-detail.md | 通訊協議詳情 | read_file |
| 6 | details/git-rules.md | Git 操作規則 | read_file |
| 7 | details/spec-rules.md | Spec 文件規則 | read_file |

## 快速定位
| 需要做咩 | 讀邊個 |
|---------|--------|
| 調用 Agent | #Comm 或 @comm-cli-path |
| 判斷 verdict | #Role 或 @role-verdict-rules |
| Git commit | details/git-rules.md |
| 讀 Spec | details/spec-rules.md |
| 睇進度 | #Session |

## 行為規則（最小集）
- 每次 Action 前先解釋
- 唔明就問
- 簡潔優先
<!-- /@index-main -->
```

---

## 01-role-summary.md 設計（Layer 2 — 角色摘要）

```markdown
---
inclusion: manual
---

# 角色摘要

<!-- @role-summary -->
[role] [orchestrator] [rules]

## 職責
- 接收需求 → 調用 Agent → 判斷結果 → 交付
- 唔寫代碼、唔評估、唔設計架構

## 調用流程
Planner → Generator → Evaluator → PASS/FAIL/REPLAN

## 循環限制
- FAIL 3 次 → 強制 REPLAN
- REPLAN 2 次 → 問用戶

## 詳情
→ details/role-detail.md
<!-- /@role-summary -->
```

---

## 02-comm-system.md 設計（Layer 2 — 通訊系統）

```markdown
---
inclusion: manual
---

# Agent 通訊系統

<!-- @comm-system -->
[communication] [cli] [path]

## CLI 調用
& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent [name] "[prompt]"

## Agent 路徑
| Agent | inbox | outbox |
|-------|-------|--------|
| Planner | ../planner/inbox/ | ../planner/outbox/ |
| Generator | ../generator/inbox/ | ../generator/outbox/ |
| Evaluator | ../evaluator/inbox/ | ../evaluator/outbox/ |

## 文件記錄
- 調用前：inbox/task-{NNN}.md
- 調用後：outbox/task-{NNN}-reply.md
- 每步：shared/conversation-log.md

## 詳情
→ details/comm-detail.md
<!-- /@comm-system -->
```

---

## Token 節省估算

| | 現有 | 新（漸進式） | 節省 |
|---|---|---|---|
| 每次對話載入 | ~170 行（core-memory + session-context） | ~50 行（index only） | **70%** |
| 需要調用 Agent 時 | 已載入 | +50 行（comm-summary） | 按需 |
| 需要 Git 操作時 | 已載入 | +30 行（git-rules） | 按需 |
| 完整規則 | 已載入 | +90 行（detail） | 按需 |

---

## 實施步驟

```
Step 1: 建立 00-index.md（L1）
        → 從 00-core-memory.md 抽取最小集

Step 2: 拆分 00-core-memory.md 成 L2 文件
        → 01-role-summary.md（角色 + 調用規則）
        → 02-comm-system.md（通訊路徑 + 文件記錄）

Step 3: 建立 details/ 目錄（L3）
        → role-detail.md（完整角色規則）
        → comm-detail.md（通訊協議詳情 + 模板）
        → git-rules.md（Git 操作規則）
        → spec-rules.md（Spec 文件規則）

Step 4: 修改 01-session-context.md
        → 改為 03-session-context.md（manual inclusion）
        → 只喺需要睇進度時載入

Step 5: 刪除舊嘅 00-core-memory.md

Step 6: 測試
        → 開 Main Agent window
        → 確認只載入 index
        → 試調用 Agent（確認會讀 comm-system）
```

---

## 各 Agent 嘅漸進式披露

### Sub Agent（Planner / Generator / Evaluator）

```
.kiro/steering/
├── 00-index.md            ← L1（角色一句話 + 文件目錄）
├── 01-rules-summary.md    ← L2（規則摘要）
└── details/
    └── full-rules.md      ← L3（完整規則 + 範例）
```

Sub Agent 比 Main Agent 簡單，因為佢哋嘅規則較少。
可以考慮只用 L1 + L2（唔需要 L3），視乎文件大小。

---

## 決策：邊啲 Agent 需要漸進式？

| Agent | 現有 Steering 大小 | 需要漸進式？ |
|-------|-------------------|------------|
| Main Agent | ~170 行 | ✅ 需要（最大） |
| Generator | ~100 行 | ⚠️ 可選（中等） |
| Evaluator | ~80 行 | ❌ 唔需要（夠細） |
| Planner | ~70 行 | ❌ 唔需要（夠細） |

**建議：先改 Main Agent，其他 Agent 視乎效果再決定。**

---

## 快速參考

```
┌─────────────────────────────────────────────────┐
│ 漸進式披露規則                                    │
├─────────────────────────────────────────────────┤
│ 1. 00-index.md 永遠載入（< 50 行）              │
│ 2. 需要時先讀 L2（#引用 或 read_file）           │
│ 3. 執行時先讀 L3（read_file details/）           │
│ 4. 唔需要嘅內容永遠唔載入                        │
│ 5. 每次對話只消耗需要嘅 Token                    │
└─────────────────────────────────────────────────┘
```
