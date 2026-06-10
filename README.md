# ProjectAgentExample

> 一個 **Multi-Agent 協作系統**，用 Orchestrator-Worker 模式 + 漸進式披露（Progressive Disclosure）設計，
> 以最少 Token 完成「需求分析 → 代碼生成 → 品質驗證」嘅完整開發流程。

---

## 1. 系統概覽

**1 個 Orchestrator（Main Agent）+ 3 個 Worker（Sub Agent）**，透過**文件**（inbox/outbox）通訊：

```
              ┌─────────────────────────────┐
   用戶 ───────▶│      Main Agent (調度)       │◀─────── 交付成品
              └──────────────┬──────────────┘
                             │ 派 Assignment（寫 inbox）
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     ┌───────────┐    ┌───────────┐    ┌───────────┐
     │  Planner  │    │ Generator │    │ Evaluator │
     │ 分析+設計  │    │  寫 code  │    │  審查評分  │
     └───────────┘    └───────────┘    └───────────┘
```

**標準流程：**
```
用戶需求 → Planner（計劃 + Test Criteria）
        → Generator（code + test）
        → Evaluator（執行 test + 評分）
              ├─ PASS (≥80)    → 交付
              ├─ FAIL (60-79)  → 退回 Generator（最多 3 次）
              └─ REPLAN (<60)  → 退回 Planner（最多 2 次）
```

**Agent 職責 + 工具權限：**

| Agent | 職責 | fs_read | fs_write | execute_bash |
|-------|------|:---:|:---:|:---:|
| Main | 調度、判斷、交付（唔寫 code/唔改 code/唔跑 test） | ✅ | ✅ | ✅ Git/環境/時間 |
| Planner | 需求分析、架構、任務拆分、Specs（唔寫 code） | ✅ | ✅ | ❌ |
| Generator | 按計劃寫 code + test | ✅ | ✅ | ✅ 裝 dep/驗證 test |
| Evaluator | 跑 test + 評分（唔改 code） | ✅ | ✅ | ✅ 跑 test |

---

## 2. 設計重點

### 2.1 漸進式披露（Progressive Disclosure）— 慳 Token

每個 Agent 嘅 steering 規則分三層，**按需載入**：

| Layer | 文件 | 載入時機 | 用途 |
|-------|------|---------|------|
| **L1** | `00-index.md`、`02-file-map.md` | `always`（每次自動載入） | 身份 + 核心規則 + 導航地圖 |
| **L2** | `01-comm-system.md` | `always` | 通訊協議 |
| **L3** | `details/*.md`、`shared/*.md` | `manual`（需要時先 `fs_read`） | 完整職責、格式、測試規則、共用規則 |

> 理念：L1/L2 保持精簡（每次都用到嘅嘢），詳細規則放 L3，Agent 執行具體步驟時先讀。

### 2.2 三件套 always-on（每個 Agent 啟動即載入）

```
00-index.md     →「我係邊個 + 核心規則 + 啟動流程」
01-comm-system  →「我同其他 Agent 點通訊（收發路徑/格式）」
02-file-map     →「有咩文件、幾時讀邊份、點搵 Project 資料」← 導航地圖
```

CLI 模式下，呢三份喺 agent JSON 嘅 `resources` 列明，保證載入。

### 2.3 File Map（導航地圖）— Agent 點搵文件

`02-file-map.md` 係每個 Agent 嘅「目錄」，回答三條問題：
1. **我有咩工具權限**（fs_read / fs_write / execute_bash）
2. **有咩 steering 文件、幾時讀邊份**（L1/L2/L3 清單 + 使用時機）
3. **點搵 Project 內容**（active-project → SearchIndex → inbox/outbox/memory/specs）

> ⚠️ File Map 係「參考地圖」唔係「強制」。真正「必讀」嘅 L3（例如 Generator 寫 code 前讀 `details/test-rules.md`）寫咗入 `00-index.md` 嘅啟動流程步驟，確保命中。

### 2.4 Context Isolation（上下文隔離）

Sub Agent 唔需要知道完整大局，只需知自己嘅「介面定位」（上游邊個、下游邊個、output 點處理）。Worker 專注做好被派嘅任務，由 Main Agent 掌握大局。

### 2.5 共用規則（shared/）— 單一邏輯來源

`error-handling`、`context-management`、`avoid-shell` 三份共用規則，每個 Agent 嘅 workspace 都有一份本地副本（`shared/`），確保跨 workspace 都讀到。

### 2.6 Deterministic-First 原則 — 確定性任務用代碼

> **「可確定嘅嘢用代碼，唔確定嘅嘢用 AI」**

當 Task/Step 有標準答案、可驗證、重複性高、唔容許錯誤、或有明確規則時，
Agent 必須編寫 JS 腳本執行，唔可以用 LLM 推理代替。

- **Planner**：標記 Step 類型（`deterministic` / `ai-driven`），提供 input/output 規格
- **Generator**：遇到 deterministic Step → 寫 JS 腳本放 `scripts/deterministic/`
- **Evaluator**：跑腳本驗證，睇 exit code（0=pass, 1=fail），唔用 LLM 判斷

腳本模板：`scripts/deterministic/_templates/`

### 2.7 Anti-Amnesia — 防止 Context Compaction 導致失憶

所有 Agent（Root/Main/Sub）都有 `anti-amnesia.md`（inclusion: always）。
當執行多步驟任務時，每個 Step 開始前讀取 `progress-marker.md`，完成後覆蓋更新。

Progress Marker 格式（覆蓋式，永遠 5 行，~20 tokens）：
```
# Progress
task: {任務描述}
last_completed: Step {N} - {描述}
next: Step {N+1} - {描述}
total: {總步數}
```

路徑規則：
- Project 操作 → `ProjectRecord/{project}/progress-marker.md`
- 非 Project 操作 → Agent 目錄 `./progress-marker.md`

與 Checkpoint 並行：Marker = 極簡狀態（做到邊）；Checkpoint = 詳細記錄（做過咩）。
---

## 3. 實際目錄結構

```
ProjectAgentExample/                          ← Root（頂層 workspace）
├── .kiro/
│   ├── steering/
│   │   ├── role.md                           ← Root 身份 + 核心規則（always）
│   │   ├── navigation.md                     ← 文件導航（always）
│   │   ├── tools.md                          ← 工具權限（always）
│   │   ├── agent-config-file-paths.md        ← 配置路徑索引（always）
│   │   ├── deterministic-first.md            ← 確定性任務用腳本原則（always）
│   │   ├── anti-amnesia.md                   ← 防失憶規則（always）
│   │   ├── role-execution.md                 ← 操作流程（manual）
│   │   └── role-constraints.md               ← 行為邊界（manual）
│   └── hooks/                                ← Root 層自動化
│       ├── auto-log-session.kiro.hook        ← 每次對話完自動寫 session log
│       ├── watch-agent-replies.kiro.hook     ← 偵測 outbox 新 reply 自動處理
│       ├── auto-commit-config.kiro.hook
│       ├── sync-config-from-github.kiro.hook
│       └── remind-update-config-deleted.kiro.hook
├── README.md                                 ← 本文件
├── scripts/
│   └── deterministic/                        ← 確定性任務腳本
│       ├── _templates/                       ← 腳本模板
│       │   ├── deterministic-template.js     ← 通用模板
│       │   └── validator-template.js         ← 格式驗證模板
│       └── README.md
├── UserConfig/sessions/                      ← 通用對話記錄（跨 Project）
├── UserConfig/session-log-entry-template.md  ← Root Agent Session Log 格式模板
├── UserDocument/                             ← 通用設計文件
│
└── main-agent/                               ← Main Agent workspace（日常開發喺呢度開）
    ├── .kiro/
    │   ├── steering/                         ← Main Agent 規則
    │   │   ├── 00-index.md                   ← L1 always（身份+規則+啟動）
    │   │   ├── 02-file-map.md                ← L1 always（導航地圖）
    │   │   ├── 01-comm-system.md             ← L2 always（通訊系統）
    │   │   ├── details/                      ← L3 manual
    │   │   │   ├── operations.md             ← 自動測試/格式/Checkpoint/Specs/記憶
    │   │   │   ├── comm-detail.md            ← 完整目錄圖 + Message 格式
    │   │   │   ├── role-detail.md            ← 完整職責 + 循環限制
    │   │   │   └── git-rules.md              ← Git 操作規則
    │   │   └── shared/                       ← L3 manual（共用規則本地副本）
    │   │       ├── error-handling.md
    │   │       ├── context-management.md
    │   │       └── avoid-shell.md
    │   ├── agents/                           ← CLI Sub Agent 定義（含 resources）
    │   │   ├── planner.json
    │   │   ├── generator.json
    │   │   └── evaluator.json
    │   └── hooks/                            ← Main 層自動化（watch reply、log）
    │
    ├── Agents/                               ← 3 個 Sub Agent 各自嘅 steering
    │   ├── planner/.kiro/steering/
    │   │   ├── role.md  navigation.md        ← L1 always（身份 + 導航）
    │   │   ├── tools.md  project-file-paths.md  ← L2 always（工具 + 路徑）
    │   │   ├── deterministic-first.md        ← L2 always（確定性原則）
    │   │   ├── anti-amnesia.md               ← L1 always（防失憶）
    │   │   ├── project-protocols-*.md        ← L3 manual（各種 protocol）
    │   │   └── domain-knowledge-*.md         ← L3 manual（領域知識）
    │   ├── generator/.kiro/steering/
    │   │   ├── role.md  navigation.md        ← L1 always
    │   │   ├── tools.md  project-file-paths.md  ← L2 always
    │   │   ├── deterministic-first.md        ← L2 always（確定性原則）
    │   │   ├── anti-amnesia.md               ← L1 always（防失憶）
    │   │   ├── project-protocols-*.md        ← L3 manual
    │   │   └── domain-knowledge-*.md         ← L3 manual（test-rules + code-standards）
    │   └── evaluator/.kiro/steering/
    │       ├── role.md  navigation.md        ← L1 always
    │       ├── tools.md  project-file-paths.md  ← L2 always
    │       ├── deterministic-first.md        ← L2 always（確定性原則）
    │       ├── anti-amnesia.md               ← L1 always（防失憶）
    │       ├── project-protocols-*.md        ← L3 manual
    │       └── domain-knowledge-*.md         ← L3 manual（evaluation-criteria）
    │
    └── ProjectRecord/                        ← 所有 Project 記錄 + 產出
        ├── active-project.md                 ← 當前 active project（切換用）
        ├── templates/                        ← 共用 Message 模板
        │   ├── assignment-template.md        ← 派工格式（範例喺 examples/）
        │   ├── assignment-reply-template.md  ← 回覆格式
        │   ├── checkpoint-template.md
        │   ├── conversation-log-entry-template.md
        │   ├── search-index-entry-template.md
        │   ├── verdict-template.md
        │   ├── progress-marker-template.md   ← Anti-Amnesia Progress Marker 格式
        │   ├── session-log-entry-template.md ← Session Log 統一格式模板
        │   ├── examples/                     ← 完整範例（manual 載入）
        │   └── specs/                        ← requirements/design/tasks template
        │
        └── {project-name}/                   ← 每個 Project 獨立空間（見 §6）
```

> ⚠️ 重點：Sub Agent 嘅 steering 存喺 `Agents/{agent}/`，但**運行時工作目錄（CWD）係 `main-agent/`**，
> 所以佢哋嘅 `./ProjectRecord/...` 解析到 `main-agent/ProjectRecord/`，完全 access 到。
> `Agents/{agent}/` 只係「存 steering 嘅櫃」，唔係困住 Agent 嘅範圍。

---

## 4. 每個 Agent 嘅 Steering 文件（點運用）

每個 Agent 啟動就有齊 **3 份 always-on**（00-index + 01-comm-system + 02-file-map），
其餘 L3 文件喺需要時先 `fs_read`。

### Main Agent（Orchestrator）
| 文件 | 層 | 幾時用 |
|------|----|--------|
| `00-index.md` | L1 | 身份 + 14 條核心規則（🚨/⚠️/💡 分級）+ Error/Context 處理 + 啟動流程 |
| `02-file-map.md` | L1 | 導航：工具權限 + 文件清單 + 點搵 Project + Sub Agent 速查 |
| `01-comm-system.md` | L2 | 調用 Sub Agent 方法 + contextFiles 表 + Assignment ID 規則 |
| `details/operations.md` | L3 | 派工/收 reply/寫記錄前讀 |
| `details/comm-detail.md` | L3 | 要完整目錄圖 / Message 格式時 |
| `details/role-detail.md` | L3 | 處理 blocked / 循環限制時 |
| `details/git-rules.md` | L3 | Git commit/push 前 |

### Planner / Generator / Evaluator（Worker）
| 文件 | 層 | 幾時用 |
|------|----|--------|
| `00-index.md` | L1 | 身份 + 核心規則（分級）+ Error/Context 處理 + 啟動流程 |
| `02-file-map.md` | L1 | 導航：工具權限 + 文件清單 + 點搵 Project |
| `01-comm-system.md` | L2 | 收件/發件路徑 + frontmatter 格式 |
| `details/workflow.md` | L3 | **開始任務前必讀**（啟動/Checkpoint/格式/寫入/記憶） |
| `details/role-detail.md` | L3 | 完整職責 / 自學 / escalation |
| `details/output-format.md` | L3 | 寫 outbox 輸出時 |
| `details/test-rules.md` ⭐ | L3 | **Generator 專屬**：寫 code 前必讀（測試規則） |
| `details/code-standards.md` | L3 | **Generator 專屬**：寫 code 時 |
| `shared/*.md`（3 份） | L3 | error 處理 / 任務太大 / 想用 shell 時 |

---

## 5. Agent 溝通流程 + 點讀取 Project 資料

### 5.1 通訊媒介：文件（唔直接對話）

Agent 之間透過 ProjectRecord 嘅 inbox/outbox 文件交換訊息：

```
Main Agent ──寫 Assignment──▶ inbox/{agent}/assignment-{id}.md
                                      │
                              Sub Agent 讀取 + 執行
                                      │
Main Agent ◀──讀 Reply──── outbox/{agent}/assignment-{id}-reply-{status}.md
```

### 5.2 完整一輪流程（用戶需求 → 交付）

```
1. 用戶 → Main Agent 講需求
2. Main 讀 active-project.md 確認當前 Project
3. Main 生成 Assignment ID（讀 SearchIndex 最後一行 +1）
4. Main 寫 inbox/planner/assignment-{id}.md → 調用 Planner
5. Planner 讀 inbox → 設計方案 → 寫 outbox/planner/...-reply-completed.md
6. Main 讀 Planner reply → 寫 inbox/generator/ → 調用 Generator
7. Generator 讀 inbox + Planner 計劃 → 寫 code+test 到 output/ → 寫 outbox/generator/
8. Main 確認有 test → 寫 inbox/evaluator/ → 調用 Evaluator
9. Evaluator 讀代碼 + 跑 test → 寫 verdict 到 outbox/evaluator/
10. Main 讀 verdict：
      PASS   → 交付俾用戶
      FAIL   → 開新 Assignment 派返 Generator（≤3 次）
      REPLAN → 開新 Assignment 派返 Planner（≤2 次）
11. 全程每步 append conversation-log + SearchIndex + checkpoint
```

### 5.3 調用 Sub Agent 嘅兩個方法

| 方法 | 指令 | 幾時用 |
|------|------|--------|
| **方法 1：Kiro CLI**（優先） | `kiro-cli chat --agent {name} "{prompt}"` | kiro-cli 可用 |
| **方法 2：invoke_sub_agent**（Fallback） | `invoke_sub_agent` + `contextFiles` | kiro-cli 唔得時 |

兩個方法都喺 `main-agent/` 為 CWD 運行，所以 Sub Agent 都 access 到 `./ProjectRecord/`。

### 5.4 點搵 Project 資料（所有 Agent 通用）

**黃金法則：先查 SearchIndex，唔好逐個文件揭。**

```
1. 確認 Project：讀 ./ProjectRecord/active-project.md 嘅 current 值
2. 搵記錄：讀 ./ProjectRecord/{current}/SearchIndex.md
            用 關鍵字/ID/Agent/Status 篩選 → 只讀對應文件
3. 攞任務：./ProjectRecord/{current}/inbox/{自己}/assignment-{id}.md
4. 睇上游成果：./ProjectRecord/{current}/outbox/{上游 agent}/
5. 睇代碼：./ProjectRecord/{current}/output/assignment-{id}/
6. 睇 Spec：./ProjectRecord/{current}/specs/{requirements,design,tasks}.md
7. 自己記憶：./ProjectRecord/{current}/memory/{自己}-memory.md
```

### 5.5 訊息格式 + Status

| 訊息 | 文件 | 關鍵欄位 |
|------|------|---------|
| Assignment | `inbox/{agent}/assignment-{id}.md` | From/To/Type/需求/Context/驗證標準 |
| Reply | `outbox/{agent}/assignment-{id}-reply-{status}.md` | AssignmentStatus/結果/Memory 已更新/Usage |

**Status**：`completed`（Planner/Generator 完成）、`blocked`（需幫助）、
`verdict-pass`/`verdict-fail`/`verdict-replan`（Evaluator 判決）、`escalation`（需用戶決定）。

**Assignment ID**：三位數字零填充（001→002），讀 SearchIndex 最後一行 +1。

### 5.6 自動化 Hooks（減少人手）

| Hook | 觸發 | 做咩 |
|------|------|------|
| `auto-log-session` | 每次對話完（agentStop） | 自動寫 session log |
| `watch-agent-replies` | outbox 有新 reply（fileCreated） | 自動讀 reply + 判斷下一步 |

---

## 6. Project 結構 + 切換/新增

### 6.1 每個 Project 嘅獨立空間
```
ProjectRecord/{project-name}/
├── specs/                    ← requirements.md / design.md / tasks.md
├── memory/                   ← {main-agent,planner,generator,evaluator}-memory.md
├── inbox/                    ← 收件（按 agent type 分：planner/generator/evaluator/main-agent）
├── outbox/                   ← 發件（同上分法）
├── checkpoints/              ← 執行記錄（斷線恢復，按 agent 分）
├── output/                   ← Generator 生成嘅代碼
├── control/                  ← 控制指令
├── SearchIndex.md            ← 搜尋索引（搵記錄入口）
├── conversation-log.md       ← 對話記錄（append-only）
├── UserConfig/sessions/      ← 本 Project session 記錄
└── UserDocument/             ← 本 Project 用戶文件
```

### 6.2 切換 Project
改一個文件即可：`ProjectRecord/active-project.md` 嘅 `current:` 值。
所有 Agent 啟動時讀呢個值決定操作邊個 Project。

### 6.3 新增 Project
1. 喺 `ProjectRecord/` 建新目錄 `{新 Project 名}/`
2. 複製 §6.1 標準結構（specs/memory/inbox/outbox/checkpoints/output/control）
3. 建空白 `SearchIndex.md` + `conversation-log.md`
4. 改 `active-project.md` 嘅 `current` 指向新 Project

---

## 7. 點樣開始用

1. 開 Kiro → **Open Folder** → 揀 `main-agent/`
2. 確認 `ProjectRecord/active-project.md` 指向你想做嘅 Project（或新增一個）
3. 直接同 Main Agent 講你嘅需求
4. Main Agent 自動調度 Planner → Generator → Evaluator，記錄寫入 `ProjectRecord/{active-project}/`
5. 完成後 Main Agent 問你要唔要 Git 操作（commit/push）

> 💡 Root 層（頂層 folder）放跨 Project 嘅通用規則、session log、自動化 hooks。日常開發喺 `main-agent/`。

---

## 8. 優化歷程（已完成）

本系統經過 5 個 Phase 優化，由「規則散亂、L1 過肥」變成「漸進式披露、導航清晰」：

| Phase | 內容 | 結果 |
|-------|------|------|
| **1. L1 瘦身** | 拆肥大嘅 00-index，非核心搬 L3 | Main 232→90、Generator 239→81、Planner 189→75、Evaluator 198→77 |
| **2. 抽共用規則** | error-handling / context-management 做 canonical + 本地副本 | 4 Agent 對稱，單一邏輯來源 |
| **3. Template 精簡** | 格式定義同範例分離 | assignment 187→27、reply 248→44，範例搬 examples/ |
| **4. 規則分級** | 核心規則加 🚨 Critical / ⚠️ Important / 💡 Guideline | 4 Agent 完成 |
| **5. comm-system 瘦身** | 完整目錄圖 + Message 格式搬 L3 | Main comm-system 200→108 |
| **+ 導航地圖** | 每個 Agent 加 `02-file-map.md`（always） | 工具權限 + 文件清單 + 點搵 Project |
| **+ avoid-shell 共用** | 搬入各 Agent shared/，L1 留精簡提醒 | always-on 27→4 行 |
| **+ Deterministic-First** | 確定性任務必須寫 JS 腳本，唔用 LLM 推理 | 所有 Agent 加入原則 + 模板 |
| **+ Anti-Amnesia** | 防 compaction 失憶，每步讀/寫 progress marker | 5 行覆蓋式，~20 tokens/step |

### 設計原則總結
- **漸進式披露**：L1/L2 always 精簡，L3 按需 `fs_read` → 慳 token
- **單一邏輯來源**：共用規則 canonical + 本地副本 → 跨 workspace 可靠
- **導航清晰**：file-map 答「有咩文件、幾時讀、點搵 Project」
- **規則聚焦**：分級 + 必讀寫入啟動流程 → 提高服從性
