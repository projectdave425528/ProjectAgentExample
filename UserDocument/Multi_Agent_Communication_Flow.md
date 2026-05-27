# Kiro Multi-Agent 文件通訊架構 v2.0

> Main Agent 作為 Orchestrator，透過文件交換控制 Planner / Generator / Evaluator
> 參考：Claude Code Evaluator-Optimizer Loop + Agent Teams 模式
> 支援：暫停 / 繼續 / 重啟 任何 Agent
> 設計日期：2026-05-24

---

## 架構總覽

```
┌─────────────────────────────────────────────────────────────────────┐
│                          用戶（你）                                   │
│                   只同 Main Agent 對話                                │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Window 1: Main Agent (Orchestrator)                                │
│  Workspace: C:\Users\proje\ProjectKiro                              │
│                                                                     │
│  職責：接收需求 → 派發 → 監控 → 交付                                 │
│  控制：可暫停 / 繼續 / 重啟任何子 Agent                               │
│  注意：唔負責評估，評估由 Evaluator 獨立完成                           │
└──────┬──────────────────────┬──────────────────────┬────────────────┘
       │                      │                      │
       ▼                      ▼                      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Window 2     │    │ Window 3     │    │ Window 4     │
│ Planner      │    │ Generator    │    │ Evaluator    │
│              │    │              │    │              │
│ 分析需求     │    │ 生成代碼     │    │ 審查品質     │
│ 設計架構     │    │ 寫測試       │    │ 驗證正確性   │
│ 拆分任務     │    │ 實現功能     │    │ 評分 + 直接  │
│              │    │              │    │ 反饋Generator│
└──────────────┘    └──────────────┘    └──────────────┘
                           ▲                    │
                           │   FAIL feedback    │
                           └────────────────────┘
```


---

## 目錄結構

```
C:\Users\proje\AgentWorkspace\
│
├── planner\
│   ├── .kiro\
│   │   ├── steering\
│   │   │   └── 00-role.md
│   │   └── hooks\
│   │       ├── watch-inbox.kiro.hook
│   │       └── check-inbox.kiro.hook
│   ├── inbox\                  ← Main Agent 寫入指令
│   ├── outbox\                 ← Planner 寫入回覆
│   └── status.md              ← 當前狀態（running/paused/idle）
│
├── generator\
│   ├── .kiro\
│   │   ├── steering\
│   │   │   └── 00-role.md
│   │   └── hooks\
│   │       ├── watch-inbox.kiro.hook
│   │       └── check-inbox.kiro.hook
│   ├── inbox\
│   ├── outbox\
│   └── status.md
│
├── evaluator\
│   ├── .kiro\
│   │   ├── steering\
│   │   │   └── 00-role.md
│   │   └── hooks\
│   │       ├── watch-inbox.kiro.hook
│   │       └── check-inbox.kiro.hook
│   ├── inbox\
│   ├── outbox\
│   └── status.md
│
└── shared\
    ├── conversation-log.md     ← 完整對話歷史
    ├── project-context.md      ← 項目背景
    └── control\
        └── commands.md         ← Main Agent 嘅控制指令記錄
```


---

## 通訊協議

### Message 格式（inbox / outbox）

```markdown
---
id: task-001
from: main-agent | planner | generator | evaluator
to: main-agent | planner | generator | evaluator
timestamp: 2026-05-24 12:30:00
type: request | response | feedback | control
status: pending | in-progress | completed | failed
priority: high | normal | low
---

# [標題]

## 內容
[具體指令或回覆]

## 期望輸出
[輸出要求]

## 參考
[相關文件路徑]
```

### 控制指令格式（特殊 type: control）

```markdown
---
id: ctrl-001
from: main-agent
to: planner
timestamp: 2026-05-24 12:45:00
type: control
action: pause | resume | restart | cancel
---

# 控制指令

## 動作
pause / resume / restart / cancel

## 原因
[為咩要暫停/重啟]

## 附加指示
[重啟時嘅新指令，如適用]
```


---

## 狀態管理系統

### 每個 Agent 嘅 status.md

```markdown
---
agent: planner
state: running | paused | idle | error
current_task: task-001
last_updated: 2026-05-24 12:30:00
---

# 當前狀態

## 進行中任務
- task-001: 分析自動交易系統需求（60% 完成）

## 已完成任務
- （無）

## 等待中
- （無）
```

### 狀態轉換圖

```
                 ┌─────────┐
                 │  idle   │ ← 初始狀態 / restart 後
                 └────┬────┘
                      │ 收到 inbox 任務
                      ▼
                 ┌─────────┐
          ┌─────│ running  │─────┬──────────┐
          │     └────┬────┘     │          │
          │          │          │          │
    pause │          │ 完成     │ error    │ 做唔到
          │          │          │          │
          ▼          ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ paused  │ │  idle   │ │  error  │ │ blocked │
    └────┬────┘ └─────────┘ └────┬────┘ └────┬────┘
         │                       │            │
   resume│                restart│      收到新指令
         │                       │      (revised)
         ▼                       ▼            │
    ┌─────────┐            ┌─────────┐        │
    │ running │            │  idle   │        │
    └─────────┘            └─────────┘        ▼
                                         ┌─────────┐
                                         │ running │
                                         └─────────┘
```


---

## 完整工作流程（Evaluator 直接反饋 Generator + Generator 自我評估）

```
┌──────────────────────────────────────────────────────────────────┐
│ Phase 0: 用戶輸入                                                 │
│ 用戶 → Main Agent：「幫我建立自動交易系統」                         │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 1: Main Agent 派發規劃任務                                  │
│                                                                  │
│ 1. 分析需求，決定先派俾 Planner                                   │
│ 2. 寫入 planner\inbox\task-001.md                                │
│ 3. 更新 shared\conversation-log.md                               │
│ 4. 回覆用戶：「已派發俾 Planner」                                  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 2: Planner 執行                                             │
│                                                                  │
│ 1. Hook 觸發 / 手動觸發                                           │
│ 2. 讀取 inbox\task-001.md                                        │
│ 3. 分析需求 + 設計架構 + 拆分任務                                  │
│ 4. 寫入 outbox\task-001-reply.md                                 │
│ 5. 更新 status.md → idle                                         │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 3: Main Agent 審視計劃 → 派發生成 + 評估任務                │
│                                                                  │
│ 1. 讀取 planner\outbox\task-001-reply.md                         │
│ 2. 判斷計劃質量（可問用戶確認）                                    │
│ 3. 整理成 Generator 指令                                          │
│ 4. 寫入 generator\inbox\task-002.md                              │
│ 5. 同時寫入 evaluator\inbox\task-003.md（預載計劃，等代碼完成）    │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 4: Generator 自我評估                                       │
│                                                                  │
│ 1. 讀取 inbox\task-002.md                                        │
│ 2. 自我評估：我做唔做到？                                         │
│                                                                  │
│    ┌─────────────────────────────────────────────────────┐       │
│    │ ✅ 做到                                             │       │
│    │ → 正常生成代碼 → Phase 4b                           │       │
│    └─────────────────────────────────────────────────────┘       │
│                                                                  │
│    ┌─────────────────────────────────────────────────────┐       │
│    │ ❌ 做唔到                                           │       │
│    │ → 寫 blocked 報告到 planner\inbox\                  │       │
│    │ → 更新 status.md → blocked                         │       │
│    │ → 進入 Phase 4c（問題上報）                          │       │
│    └─────────────────────────────────────────────────────┘       │
└──────────────────────────────┬───────────────────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │ 做到                             │ 做唔到
              ▼                                 ▼
┌──────────────────────────┐    ┌──────────────────────────────────┐
│ Phase 4b: Generator 生成 │    │ Phase 4c: 問題上報流程            │
│                          │    │                                  │
│ 1. 按計劃生成代碼        │    │ 1. Generator 寫 blocked 到       │
│ 2. 寫 outbox\reply       │    │    planner\inbox\                │
│ 3. 寫 evaluator\inbox\   │    │                                  │
│    ready.md              │    │ 2. Planner 收到 blocked：         │
│ 4. status → idle         │    │    • 可以自己解決（設計問題）     │
│                          │    │      → 修改計劃 → 重新派發       │
│                          │    │      → 回到 Phase 4              │
│                          │    │    • 需要用戶介入（權限/能力）    │
│                          │    │      → 寫 escalation 到 outbox   │
│                          │    │      → Main Agent 收到           │
│                          │    │      → 問用戶取得資源             │
│                          │    │      → 用戶提供後重新派發         │
└──────────────┬───────────┘    └──────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 5: Evaluator 執行（獨立判斷，唔經 Main Agent）              │
│                                                                  │
│ 1. 讀取 inbox\task-003.md（計劃）+ task-003-ready.md（代碼位置） │
│ 2. 讀取 Generator 嘅代碼                                          │
│ 3. 對照 Planner 嘅計劃逐項檢查                                    │
│ 4. 判斷 verdict                                                  │
│ 5. 根據 verdict 直接行動：                                        │
│                                                                  │
│    ┌─────────────────────────────────────────────────────┐       │
│    │ PASS                                                │       │
│    │ → 寫入 outbox\task-003-reply.md（通知 Main Agent）  │       │
│    │ → Main Agent 收到後交付俾用戶                        │       │
│    └─────────────────────────────────────────────────────┘       │
│                                                                  │
│    ┌─────────────────────────────────────────────────────┐       │
│    │ FAIL                                                │       │
│    │ → 直接寫入 generator\inbox\task-004-feedback.md     │       │
│    │ → Generator 收到後先自我評估做唔做到修正             │       │
│    │   • 做到 → 修正 → 再通知 Evaluator                  │       │
│    │   • 做唔到 → 寫 blocked 到 Planner                  │       │
│    │ → 同時寫 outbox\reply 通知 Main Agent               │       │
│    └─────────────────────────────────────────────────────┘       │
│                                                                  │
│    ┌─────────────────────────────────────────────────────┐       │
│    │ REPLAN                                              │       │
│    │ → 直接寫入 planner\inbox\task-005-feedback.md       │       │
│    │ → Planner 收到後重新規劃                             │       │
│    │ → 同時寫 outbox\reply 通知 Main Agent               │       │
│    └─────────────────────────────────────────────────────┘       │
│                                                                  │
│ 6. 更新 status.md → idle                                         │
└──────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 6: Main Agent 收到通知（監控角色）                           │
│                                                                  │
│ 讀取 evaluator\outbox\ 或 planner\outbox\                       │
│                                                                  │
│ • PASS → 交付俾用戶                                              │
│ • FAIL → 通知用戶「Evaluator 已直接反饋 Generator 修正中」        │
│ • REPLAN → 通知用戶「Evaluator 已要求 Planner 重新規劃」          │
│ • escalation → 問用戶取得所需資源/權限/能力                       │
│                                                                  │
│ Main Agent 角色 = 派發 + 監控 + 通知用戶 + 取得用戶資源            │
└──────────────────────────────────────────────────────────────────┘
```


---

## 循環反饋流程圖（含 Generator 自我評估 + 問題上報）

```
                    ┌─────────────┐
                    │   用戶需求   │
                    └──────┬──────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Main Agent    │◀──── escalation（需要用戶提供資源）
                  │  (Orchestrator) │
                  └──┬──────────┬──┘
                     │          │
          派發規劃   │          │ 派發生成
                     ▼          ▼
              ┌────────┐  ┌──────────┐
              │Planner │◀─│Generator │ ← blocked（做唔到）
              └───┬────┘  └────┬─────┘
                  │            │ ▲
                  │            │ │ FAIL feedback
                  │  ┌─────────┘ │
                  │  │           │
                  │  ▼           │
                  │  ┌──────────┐│
                  │  │Evaluator ├┘
                  │  └────┬─────┘
                  │       │
                  │  ┌────┼────┐
                  │  │    │    │
                  │ PASS FAIL REPLAN
                  │  │    │    │
                  │  │    │    └──→ Planner（直接）
                  │  │    └──────→ Generator（直接）
                  │  │
                  │  ▼
                  │  Main Agent → 交付用戶
                  │
                  │ Planner 判斷 blocked：
                  │ • 可自己解決 → 修改計劃 → 重新派發 Generator
                  │ • 需要用戶 → escalation → Main Agent → 問用戶
                  │
                  └──→ 修改計劃後重新派發 Generator
```

### 問題上報路徑（Escalation Path）

```
Generator 做唔到
    │
    │ blocked 報告
    ▼
Planner 評估
    │
    ├── 可以自己解決（設計問題/拆分任務）
    │   → 修改計劃
    │   → 重新派發 Generator
    │   → 唔需要打擾用戶
    │
    └── 需要用戶介入（權限/能力/資源）
        → 寫 escalation 到 outbox
        → Main Agent 收到
        → 問用戶：「需要 XXX，你可以提供嗎？」
        → 用戶提供
        → Main Agent 寫入 Planner inbox
        → Planner 更新計劃
        → 重新派發 Generator
```


---

## 用戶控制機制（暫停 / 繼續 / 重啟）

### 控制指令表

| 用戶講 | Main Agent 做 | 效果 |
|--------|--------------|------|
| 「暫停 Planner」 | 寫 control msg 到 planner\inbox\ | Planner 停止當前工作 |
| 「繼續 Planner」 | 寫 resume msg 到 planner\inbox\ | Planner 繼續未完成工作 |
| 「重啟 Generator」 | 清空 generator\inbox\ + 寫新任務 | Generator 從頭開始 |
| 「取消全部」 | 寫 cancel 到所有 Agent inbox | 全部停止 |
| 「keep going」 | 唔寫控制指令，繼續正常流程 | 流程繼續 |
| 「跳過 Evaluator」 | 直接交付，唔派發評估 | 省略評估步驟 |

### 控制流程圖

```
用戶：「暫停 Generator」
        │
        ▼
┌─────────────────────────────────────────────────────┐
│ Main Agent 執行：                                    │
│                                                     │
│ 1. 寫入 generator\inbox\ctrl-001.md                 │
│    ---                                              │
│    type: control                                    │
│    action: pause                                    │
│    ---                                              │
│                                                     │
│ 2. 更新 shared\control\commands.md（記錄）           │
│                                                     │
│ 3. 回覆用戶：「Generator 已暫停」                     │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│ Generator（Window 3）收到控制指令：                    │
│                                                     │
│ 1. 讀取 ctrl-001.md → action = pause                │
│ 2. 停止當前工作                                      │
│ 3. 更新 status.md → state: paused                   │
│ 4. 寫入 outbox\ctrl-001-ack.md（確認已暫停）          │
└─────────────────────────────────────────────────────┘
```

### 重啟流程

```
用戶：「重啟 Planner，用新嘅需求」
        │
        ▼
┌─────────────────────────────────────────────────────┐
│ Main Agent 執行：                                    │
│                                                     │
│ 1. 寫入 planner\inbox\ctrl-002.md                   │
│    ---                                              │
│    type: control                                    │
│    action: restart                                  │
│    ---                                              │
│    ## 新指令                                         │
│    [新嘅需求內容]                                     │
│                                                     │
│ 2. （可選）清空 planner\outbox\ 舊回覆               │
│                                                     │
│ 3. 回覆用戶：「Planner 已重啟，新任務已派發」          │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│ Planner（Window 2）收到控制指令：                      │
│                                                     │
│ 1. 讀取 ctrl-002.md → action = restart              │
│ 2. 放棄當前進度                                      │
│ 3. 更新 status.md → state: running                  │
│ 4. 按新指令重新開始                                   │
│ 5. 完成後寫入 outbox\（新回覆）                       │
└─────────────────────────────────────────────────────┘
```


---

## Evaluator 設計（參考 Claude Code Evaluator-Optimizer Loop）

### Evaluator 角色定義

```
職責：
1. 對照 Planner 嘅計劃，檢查 Generator 嘅輸出
2. 逐項評分（Checklist）
3. 輸出 verdict（PASS / FAIL / REPLAN）
4. 提供具體、可操作嘅 feedback

工具權限：
- ✅ 讀取所有文件（inbox、outbox、shared、generator 代碼）
- ✅ 執行測試命令（如 npm test）
- ❌ 唔可以修改代碼（只評估，唔修正）
- ❌ 唔可以直接同用戶對話
```

### Evaluator Checklist

```markdown
## 評估清單

### 功能性（40%）
- [ ] 代碼是否實現咗 Planner 計劃嘅所有功能
- [ ] 是否可以成功編譯/運行
- [ ] 邊界情況有冇處理

### 代碼品質（30%）
- [ ] 命名是否清晰
- [ ] 有冇重複代碼
- [ ] 錯誤處理是否完善
- [ ] 代碼風格是否一致

### 安全性（20%）
- [ ] 有冇明顯安全漏洞
- [ ] 輸入有冇驗證
- [ ] 敏感資料有冇暴露

### 可維護性（10%）
- [ ] 有冇適當 comment
- [ ] 結構是否易於擴展
- [ ] 依賴是否合理
```

### Evaluator 輸出格式

```markdown
---
id: task-003-reply
from: evaluator
to: main-agent
timestamp: 2026-05-24 13:00:00
type: response
status: completed
---

# 評估結果

## Verdict: PASS | FAIL | REPLAN

## 總分: 85/100

## 各項評分
| 類別 | 分數 | 備註 |
|------|------|------|
| 功能性 | 35/40 | 缺少一個邊界處理 |
| 代碼品質 | 25/30 | 有少量重複 |
| 安全性 | 18/20 | 良好 |
| 可維護性 | 7/10 | comment 不足 |

## 問題清單
| # | 嚴重度 | 文件 | 描述 | 建議修正 |
|---|--------|------|------|---------|
| 1 | Critical | auth.ts | 冇驗證 token 過期 | 加 expiry check |
| 2 | Warning | utils.ts | 重複嘅 helper function | 抽取成共用 |
| 3 | Info | main.ts | 缺少 JSDoc | 加 comment |

## 反饋摘要
[俾 Generator 或 Planner 嘅具體修正指示]
```


---

## 各 Agent 責任定義（參考 AutoTrade 項目）

### Main Agent (Orchestrator) 責任

| 類別 | 具體責任 |
|------|---------|
| **需求管理** | 接收用戶需求、確認需求細節、管理需求變更 |
| **任務調度** | 決定派發邊個 Agent、管理任務優先級、處理 escalation |
| **進度監控** | 追蹤各 Agent 狀態、通知用戶進度、偵測超時/卡住 |
| **資源提供** | 回應 escalation（問用戶取得 API key/權限/環境） |
| **用戶溝通** | 匯報結果、問確認、交付最終產物 |
| **流程控制** | 執行暫停/繼續/重啟/取消指令 |
| **品質把關** | 審視 Planner 嘅計劃是否合理（唔評估代碼） |

### Planner 責任

| 類別 | 具體責任 |
|------|---------|
| **需求分析** | 將模糊需求拆解成具體功能點 |
| **架構設計** | 設計系統架構（模組、數據流、API 接口） |
| **技術選型** | 選擇技術棧（語言、框架、庫、數據庫） |
| **任務拆分** | 將大任務拆成可獨立開發嘅子任務（含依賴關係） |
| **風險評估** | 識別技術風險、提出緩解方案 |
| **設計模式** | 決定用咩 Design Pattern（Strategy/Adapter/Observer 等） |
| **問題解決** | 收到 Generator blocked → 判斷能否修改設計解決 |
| **上報判斷** | 判斷問題是否需要用戶介入 → 寫 escalation |
| **Spec 生成** | 輸出 requirements.md + design.md + tasks.md |

### Generator 責任

| 類別 | 具體責任 |
|------|---------|
| **代碼生成** | 按 Planner 計劃寫出實際代碼 |
| **測試撰寫** | 寫單元測試、整合測試（pytest） |
| **配置文件** | 寫 config、environment setup、依賴清單 |
| **自我評估** | 收到任務先判斷做唔做到 |
| **自學能力** | 能力不足時先搜尋文檔/代碼/Web 學習 |
| **問題上報** | 自學失敗後寫 blocked 報告到 Planner |
| **代碼規範** | 遵守編寫風格（Clean Code、Design Pattern、解耦） |
| **修正代碼** | 收到 Evaluator feedback 後按指示修正 |
| **通知 Evaluator** | 代碼完成後寫 ready.md 通知評估 |

#### Generator 代碼規範（來自 AutoTrade 項目）
- 函數只做一件事，長度 < 30 行
- 參數 ≤ 3 個，超過用 dataclass 包裝
- Loop 嵌套最多 3 層
- 模組之間透過 Interface/Protocol 通訊
- 使用 Dependency Injection
- 禁止：全局可變狀態、Magic number、超過 500 行嘅文件

### Evaluator 責任

| 類別 | 具體責任 |
|------|---------|
| **代碼審查** | 檢查代碼風格、命名、結構是否符合規範 |
| **邏輯驗證** | 檢查邏輯正確性、邊界情況、異常處理 |
| **測試執行** | 跑 unit test / integration test，確認通過 |
| **覆蓋率檢查** | 確認測試覆蓋率達標（策略 90%、風控 95%） |
| **安全掃描** | 檢查安全漏洞（API key 暴露、SQL injection 等） |
| **設計一致性** | 對照 Planner 計劃，確認實現符合設計 |
| **直接反饋** | FAIL 時直接寫 feedback 到 Generator inbox |
| **重規劃判斷** | 問題太大時直接寫 REPLAN 到 Planner inbox |
| **評分** | 按 Checklist 逐項評分（功能/品質/安全/可維護） |

#### Evaluator 測試檢查項（來自 AutoTrade 項目）
- 策略信號：正確生成買/賣/持有信號
- 風控觸發：止損/止盈/最大回撤正確觸發
- 訂單執行：市價單/限價單正確下單
- 異常處理：API 超時/斷線/餘額不足
- 數據邊界：空數據/缺失數據/極端值
- 並發安全：多個信號同時觸發唔會重複下單
- 回測一致性：回測結果同實盤邏輯一致

---

## 各 Agent Steering 規則

### Main Agent（加入 Orchestrator Steering）

```markdown
# Orchestrator 規則（加入現有 ProjectKiro steering）

## 角色
你同時係用戶嘅助手同 Multi-Agent 系統嘅 Orchestrator。
你負責派發同監控，唔負責評估。評估由 Evaluator 獨立完成。

## Agent 控制路徑
- Planner inbox: C:\Users\proje\AgentWorkspace\planner\inbox\
- Generator inbox: C:\Users\proje\AgentWorkspace\generator\inbox\
- Evaluator inbox: C:\Users\proje\AgentWorkspace\evaluator\inbox\
- 各 Agent outbox: 對應目錄嘅 outbox\
- 狀態文件: 各 Agent 根目錄嘅 status.md

## 派發規則
1. 新需求 → 先派 Planner
2. Planner 完成 → 審視後同時派 Generator + 預載計劃俾 Evaluator
3. Generator 完成 → Generator 自動通知 Evaluator（唔需要你中轉）
4. Evaluator 完成評估後：
   - PASS → 你收到通知 → 交付用戶
   - FAIL → Evaluator 直接反饋 Generator（唔經你）→ 你收到通知告知用戶
   - REPLAN → Evaluator 直接反饋 Planner（唔經你）→ 你收到通知告知用戶
5. 最多循環 3 次，超過 Evaluator 會強制 REPLAN

## 你唔做嘅事
- ❌ 唔評估代碼質量（Evaluator 做）
- ❌ 唔判斷 PASS/FAIL（Evaluator 做）
- ❌ 唔中轉 Evaluator 嘅 feedback（Evaluator 直接寫）

## 你做嘅事
- ✅ 接收用戶需求
- ✅ 初始派發（Planner → Generator + Evaluator）
- ✅ 監控各 Agent 狀態
- ✅ 執行用戶嘅控制指令（暫停/繼續/重啟）
- ✅ 收到 PASS 後交付用戶
- ✅ 通知用戶當前進度

## 控制指令
用戶講「暫停 X」→ 寫 control msg（action: pause）到 X 嘅 inbox
用戶講「繼續 X」→ 寫 control msg（action: resume）到 X 嘅 inbox
用戶講「重啟 X」→ 寫 control msg（action: restart）到 X 嘅 inbox
用戶講「取消」→ 寫 cancel 到所有 Agent

## 命名規則
- 任務：task-{NNN}.md（全局遞增）
- 控制：ctrl-{NNN}.md
- 回覆：task-{NNN}-reply.md
- 確認：ctrl-{NNN}-ack.md
- 反饋：task-{NNN}-feedback.md
- 就緒通知：task-{NNN}-ready.md
```

### Planner Steering

```markdown
# Planner Agent

## 角色
你係 Planner，負責分析需求同設計技術方案。
你同時負責處理 Generator 嘅問題上報，判斷是否需要用戶介入。

## 啟動規則
1. 檢查 inbox/ 有冇未處理嘅文件
2. 如果有 control type → 執行控制指令（pause/resume/restart）
3. 如果有 request type → 執行規劃任務
4. 如果有 blocked type（來自 Generator）→ 執行「問題處理流程」
5. 如果有 feedback type（來自 Evaluator REPLAN）→ 重新規劃

## 問題處理流程（收到 Generator blocked 報告）

### Step 1: 分析問題
讀取 blocked 報告，判斷問題類別：
- capability（能力）
- design（設計）
- permission（權限）
- dependency（依賴）
- scope（範圍）

### Step 2: 判斷能否自己解決

| 情況 | 我可以解決？ | 行動 |
|------|------------|------|
| 設計問題（架構矛盾） | ✅ 可以 | 修改設計方案，重新派發 Generator |
| 任務太大 | ✅ 可以 | 拆分成更細嘅子任務，重新派發 |
| 替代方案可行 | ✅ 可以 | 採用替代方案，更新計劃 |
| 需要 API key / 權限 | ❌ 唔得 | 上報 Main Agent → 問用戶 |
| 需要安裝工具 / 環境 | ❌ 唔得 | 上報 Main Agent → 問用戶 |
| 能力完全不足（冇替代） | ❌ 唔得 | 上報 Main Agent → 問用戶 |

### Step 3a: 自己解決（唔需要用戶）
1. 修改計劃 / 設計新方案
2. 寫入 generator\inbox\task-{NNN}-revised.md（新指令）
3. 寫入 outbox\ 通知 Main Agent（FYI，唔需要行動）
4. 更新 status.md

### Step 3b: 需要用戶介入（上報 Main Agent）
寫入 outbox\task-{NNN}-escalation.md

---
id: task-{NNN}-escalation
from: planner
to: main-agent
timestamp: [時間]
type: escalation
requires: user-action
---

# 需要用戶介入

## 問題來源
Generator 報告無法完成 task-{NNN}

## 問題類別
[capability / permission / dependency]

## 具體需要
[用戶需要提供咩]
- 例：需要 OpenAI API key
- 例：需要安裝 Docker
- 例：需要存取 production database 權限

## 建議問法
[建議 Main Agent 點問用戶]
「你可唔可以提供 XXX？」

## 取得後嘅下一步
[用戶提供後，流程點繼續]

Main Agent 收到 escalation 後 → 問用戶 → 用戶提供 → Main Agent 寫入 Planner inbox → Planner 更新計劃 → 重新派發 Generator

## 暫停行為
收到 pause → 更新 status.md → 停止工作 → 寫 ack
收到 resume → 繼續未完成嘅工作
收到 restart → 放棄進度 → 按新指令重新開始

## 輸出規則
- 回覆寫入 outbox/（唔好改 inbox 嘅文件）
- 規劃回覆必須包含：技術方案摘要、子任務清單、風險評估
- 更新 status.md

## 寫入路徑
- Generator inbox: C:\Users\proje\AgentWorkspace\generator\inbox\
- 自己 outbox: outbox\

## 限制
- 唔可以寫代碼
- 唔可以直接同用戶對話（要透過 Main Agent）
- 唔可以自己提供 API key 或權限（要上報）
```

### Generator Steering

```markdown
# Generator Agent

## 角色
你係 Generator，負責根據計劃生成代碼。
你有自我評估能力：開始前先判斷做唔做到，做唔到就上報。

## 啟動規則
1. 檢查 inbox/ 有冇未處理嘅文件
2. 如果有 control type → 執行控制指令
3. 如果有 request type → 先自我評估（見下方），再決定生成或上報
4. 如果有 feedback type（來自 Evaluator）→ 按 feedback 修正代碼

## ⚠️ 自我評估（收到任務後第一步）
收到任務後，先問自己：

### 評估清單
1. 我有冇足夠嘅技術能力完成？（語言/框架/算法）→ **如果唔夠，先自學**
2. 計劃嘅設計是否可行？（架構矛盾/邏輯漏洞）
3. 我有冇所需嘅權限？（文件存取/API key/環境）
4. 依賴是否可用？（第三方庫/服務/硬件）
5. 時間/資源是否合理？（任務太大需要拆分）

### 評估結果
- ✅ 全部通過 → 正常生成代碼
- ⚠️ 能力不足 → 先嘗試自學（見下方）
- ❌ 其他問題 → 觸發「問題上報流程」

## 自學流程（能力不足時，上報前必須先試）

### Step 0: 先自己搵方法（唔好即刻上報）
當發現自己能力不足時，必須先嘗試以下步驟：

1. **搜尋文檔** — 讀取相關文件、官方文檔、shared\ 入面嘅參考資料
2. **搜尋代碼** — 睇 workspace 入面有冇類似實現可以參考
3. **Web 搜尋** — 用 MCP fetch / web search 搵教學、範例、解決方案
4. **簡化方案** — 試下用更簡單嘅方式達到同樣效果
5. **分步實現** — 將複雜任務拆成自己做到嘅小步驟

### 自學結果判斷
- ✅ 學到了 / 搵到方法 → 正常生成代碼（喺 reply 入面註明「透過自學完成」）
- ❌ 試晒都搵唔到 → 先觸發「問題上報流程」

### 自學記錄（寫入 outbox）
無論成功定失敗，都要記錄學習過程：
```
## 自學記錄
- 嘗試咗咩：[搜尋/閱讀/測試嘅內容]
- 結果：[學到咩 / 點解搵唔到]
- 花費時間：[大約幾多步驟]
```

---

## 問題上報流程（自學失敗後先觸發）

### Step 1: 分類問題
| 問題類型 | 例子 | 前提 | 上報對象 |
|---------|------|------|---------|
| 能力不足 | 唔識某個框架、算法太複雜 | **已嘗試自學但失敗** | → Planner |
| 設計問題 | 架構矛盾、接口唔匹配、邏輯漏洞 | 唔係能力問題 | → Planner |
| 權限不足 | 冇 API key、冇文件存取權、冇環境 | 唔係能力問題 | → Planner |
| 依賴缺失 | 第三方庫唔存在、服務唔可用 | 唔係能力問題 | → Planner |
| 任務太大 | 需要拆分成更細嘅子任務 | 唔係能力問題 | → Planner |

### Step 2: 寫入問題報告到 Planner inbox
文件名：task-{NNN}-blocked.md

---
id: task-{NNN}-blocked
from: generator
to: planner
timestamp: [時間]
type: blocked
category: capability | design | permission | dependency | scope
self-learning-attempted: true | false
---

# 無法執行任務

## 任務
[原始任務描述]

## 問題
[具體做唔到咩]

## 自學嘗試（能力問題必填）
- 搜尋咗咩：[文檔/代碼/Web]
- 嘗試咗咩方案：[簡化/分步/替代]
- 點解仍然做唔到：[具體原因]

## 原因分析
[點解做唔到，技術細節]

## 建議方案
[如果有替代方案就提出]
- 方案 A: ...
- 方案 B: ...

## 需要咩先可以做到
[具體需要嘅權限/能力/資源/教學]

### Step 3: 更新自己 status.md → blocked
等待 Planner 回覆或 Main Agent 提供資源

## 代碼完成後（正常流程）
1. 寫入 outbox\task-{NNN}-reply.md
2. 同時寫入 evaluator\inbox\task-{NNN}-ready.md（通知 Evaluator 代碼已完成）
   - ready 文件包含：代碼位置、完成咗咩、已知限制

## 收到 Evaluator Feedback 後
1. 讀取 feedback 文件（來自 Evaluator 直接寫入）
2. 先自我評估：feedback 要求嘅修正我做唔做到？
   - 做到 → 按問題清單逐項修正
   - 做唔到 → 觸發問題上報流程（寫 blocked 到 Planner）
3. 修正完成後再次寫入 evaluator\inbox\task-{NNN}-ready.md（通知重新評估）
4. 更新 outbox\（新回覆）

## 暫停行為
同 Planner 一樣嘅 pause/resume/restart 邏輯

## 寫入路徑
- Evaluator inbox: C:\Users\proje\AgentWorkspace\evaluator\inbox\
- Planner inbox: C:\Users\proje\AgentWorkspace\planner\inbox\
- 自己 outbox: outbox\

## 限制
- 嚴格按照 Planner 嘅方案執行
- 遇到方案不可行 → 上報 Planner（唔好自己改方案）
- 收到 Evaluator feedback 時，只修正被指出嘅問題，唔好大幅重構
- 唔好硬做做唔到嘅嘢，誠實上報比交出爛代碼重要
```

### Evaluator Steering

```markdown
# Evaluator Agent

## 角色
你係 Evaluator，負責檢查 Generator 嘅輸出質量，並直接反饋。

## 啟動規則
1. 檢查 inbox/ 有冇未處理嘅文件
2. 如果有 control type → 執行控制指令（pause/resume/restart）
3. 如果有 request type → 執行評估
4. 如果收到 task-XXX-ready.md → 代碼已完成，開始評估

## 評估流程
1. 讀取 inbox 嘅計劃文件（Planner 嘅方案）
2. 讀取 Generator 嘅代碼（路徑喺 ready 文件入面）
3. 對照 Checklist 逐項檢查
4. 計算總分
5. 決定 verdict：
   - >= 80 分 → PASS
   - 60-79 分 → FAIL（可修正）
   - < 60 分 → REPLAN（方案有問題）

## 直接反饋規則（重要！唔經 Main Agent）
- PASS → 寫 outbox\reply（通知 Main Agent 交付）
- FAIL → 直接寫入 generator\inbox\task-XXX-feedback.md
         同時寫 outbox\reply（通知 Main Agent）
- REPLAN → 直接寫入 planner\inbox\task-XXX-feedback.md
           同時寫 outbox\reply（通知 Main Agent）

## 寫入路徑
- Generator inbox: C:\Users\proje\AgentWorkspace\generator\inbox\
- Planner inbox: C:\Users\proje\AgentWorkspace\planner\inbox\
- 自己 outbox: outbox\

## 反饋格式
feedback 文件必須包含：
- 具體問題清單（文件 + 行號 + 描述）
- 建議修正方式
- 唔好只講「改好啲」，要講「第 15 行加 null check」

## 循環限制
- 最多連續 FAIL 3 次
- 第 3 次仍然 FAIL → 強制 REPLAN
- 寫入 feedback 時標注第幾次循環

## 限制
- 唔可以修改代碼（只評估 + 反饋）
- 唔可以直接同用戶對話
- 評估要客觀，唔好因為「差唔多得」就俾 PASS
```


---

## Hook 設計

### 子 Agent 通用 Hook — watch-inbox.kiro.hook

```json
{
  "name": "Watch Inbox",
  "version": "1.0.0",
  "description": "偵測 inbox 新文件，自動讀取並執行",
  "when": {
    "type": "fileCreated",
    "patterns": ["inbox/*.md"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "inbox 收到新文件。讀取最新嘅 inbox/*.md：如果 type=control 就執行控制指令（pause/resume/restart/cancel）；如果 type=request 或 feedback 就執行任務。完成後寫入 outbox/ 並更新 status.md。"
  }
}
```

### 子 Agent Fallback Hook — check-inbox.kiro.hook

```json
{
  "name": "Check Inbox (Manual)",
  "version": "1.0.0",
  "description": "手動觸發檢查 inbox",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "檢查 inbox/ 有冇未處理嘅文件。如果有就按照 steering 規則執行。如果冇就回覆 idle。"
  }
}
```

### Main Agent Hook — watch-replies.kiro.hook

```json
{
  "name": "Watch Agent Replies",
  "version": "1.0.0",
  "description": "偵測子 Agent 回覆",
  "when": {
    "type": "fileCreated",
    "patterns": ["C:/Users/proje/AgentWorkspace/*/outbox/*.md"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "有子 Agent 回覆咗。讀取最新嘅 outbox 文件，根據 Orchestrator 規則判斷下一步：如果係 Evaluator 回覆就判斷 verdict；如果係其他 Agent 回覆就決定派發下一個任務。更新 conversation-log.md。"
  }
}
```


---

## 觸發機制

### 自動觸發（理想）

```
Main Agent 寫入文件
    → OS FileSystem Event (Windows ReadDirectoryChangesW)
    → VS Code FileSystemWatcher
    → Kiro fileCreated Hook
    → askAgent
    → 子 Agent 自動開始工作
```

### 半自動觸發（Fallback）

```
Main Agent 寫入文件
    → 你切換到對應 Window
    → 打「go」或按 userTriggered Hook 按鈕
    → 子 Agent 檢查 inbox → 開始工作
```

### promptSubmit Hook（最可靠嘅 Fallback）

```json
{
  "name": "Auto Check Inbox on Any Message",
  "version": "1.0.0",
  "when": { "type": "promptSubmit" },
  "then": {
    "type": "askAgent",
    "prompt": "先檢查 inbox/ 有冇未處理嘅文件，如果有就優先處理。"
  }
}
```

你喺子 Agent window 打任何字（包括「go」），佢都會先檢查 inbox。

---

## 實際操作指南

### 正常流程

```
1. 你同 Main Agent 講需求
2. Main Agent 自動寫入 planner\inbox\
3. 你切換到 Planner window → 打「go」（或等自動觸發）
4. Planner 完成 → 你切換回 Main Agent → 話「check replies」
5. Main Agent 讀取回覆 → 寫入 generator\inbox\
6. 你切換到 Generator window → 打「go」
7. Generator 完成 → 你切換回 Main Agent → 話「check replies」
8. Main Agent 寫入 evaluator\inbox\
9. 你切換到 Evaluator window → 打「go」
10. Evaluator 完成 → 你切換回 Main Agent → 話「check replies」
11. Main Agent 判斷 verdict → 交付或循環
```

### 暫停流程

```
1. 你同 Main Agent 講：「暫停 Generator」
2. Main Agent 寫入 generator\inbox\ctrl-001.md (action: pause)
3. 你切換到 Generator window → 打「go」
4. Generator 讀到 pause → 停止 → 更新 status → 寫 ack
5. 你切換回 Main Agent → 話「check replies」
6. Main Agent 確認已暫停 → 回覆你
```

### 重啟流程

```
1. 你同 Main Agent 講：「重啟 Planner，新需求係 XXX」
2. Main Agent 寫入 planner\inbox\ctrl-002.md (action: restart + 新指令)
3. 你切換到 Planner window → 打「go」
4. Planner 讀到 restart → 放棄舊進度 → 按新指令開始
5. 正常流程繼續
```


---

## 同 Claude Code 嘅對比

| 特性 | 本方案（Kiro 文件通訊） | Claude Code Multi-Agent |
|------|----------------------|------------------------|
| Evaluator 循環 | ✅ Main Agent 判斷 verdict 後路由 | ✅ 自動循環 |
| 暫停/繼續 | ✅ 透過 control message | ❌ 冇原生支援 |
| 重啟 Agent | ✅ restart control + 新指令 | ⚠️ 要手動重新 spawn |
| 獨立 Steering | ✅ 每個 workspace 獨立 | ✅ 每個 agent .md 獨立 |
| 獨立 Context | ✅ 每個 window 獨立 | ✅ 每個 subagent 獨立 |
| 並行 | ✅ 多 window 同時開 | ✅ 真正並行 process |
| 自動觸發 | ⚠️ 需驗證 fileCreated | ✅ 主 Agent 自動調度 |
| 對話歷史 | ✅ shared\conversation-log.md | ❌ 冇統一記錄 |
| 用戶控制粒度 | ✅ 可控制每個 Agent | ⚠️ 較少控制 |
| 設定複雜度 | 高（多 window + 文件協議） | 中（寫 .md 就得） |

---

## 限制同風險

| 限制 | 影響 | 緩解方案 |
|------|------|---------|
| fileCreated 可能唔觸發 | 需要手動打「go」 | promptSubmit hook fallback |
| 需要手動切換 window | 操作繁瑣 | 養成固定流程習慣 |
| Context window 有限 | 長任務可能爆 context | 每個任務獨立文件，唔累積 |
| 冇真正並行 | 同一 window 一次一個任務 | 多 window 模擬並行 |
| 文件衝突 | 兩個 Agent 同時寫同一文件 | 用 task ID 確保唯一性 |
| 冇自動超時 | Agent 卡住唔知 | Main Agent 定期 check status |

---

## 未來擴展

- 加入 **Researcher Agent**（第 5 個 Window）— 專門做資料搜集（配合 MCP fetch）
- 加入 **Tester Agent** — 專門寫同執行測試
- 用 **shared\task-board.md** 做 Kanban 式任務追蹤
- 如果 Kiro 支援自定義 Sub Agent config → 簡化成單 Workspace
- 如果 Kiro 支援 timer/cron → 加入自動超時檢測

---

## 快速參考卡

```
┌─────────────────────────────────────────────────┐
│ 常用指令（同 Main Agent 講）                      │
├─────────────────────────────────────────────────┤
│ 「開始規劃 XXX」    → 派發 Planner               │
│ 「check replies」  → 讀取所有 Agent 回覆         │
│ 「暫停 Generator」 → 寫 pause control            │
│ 「繼續 Generator」 → 寫 resume control           │
│ 「重啟 Planner」   → 寫 restart control          │
│ 「取消全部」       → 寫 cancel 到所有 Agent      │
│ 「跳過評估」       → 直接交付，唔經 Evaluator    │
│ 「keep going」     → 繼續正常流程                │
│ 「狀態」           → 讀取所有 Agent status.md    │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Agent 之間直接通訊（唔經 Main Agent）             │
├─────────────────────────────────────────────────┤
│ Generator → Evaluator: 寫 ready.md 通知代碼完成 │
│ Evaluator → Generator: 寫 feedback.md（FAIL）   │
│ Evaluator → Planner:   寫 feedback.md（REPLAN） │
│ Evaluator → Main Agent: 寫 reply.md（通知結果） │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 子 Agent Window 操作                             │
├─────────────────────────────────────────────────┤
│ 打「go」           → 觸發檢查 inbox              │
│ 按 Hook 按鈕       → userTriggered check inbox  │
│ （如果自動觸發有效，以上都唔需要）                 │
└─────────────────────────────────────────────────┘
```
