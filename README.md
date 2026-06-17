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

| Layer | 文件類型 | inclusion | 用途 |
|-------|---------|-----------|------|
| **L1** | `role.md`、`navigation.md`、`anti-amnesia.md` | `always` | 身份 + 核心規則 + 導航 + 防失憶 |
| **L2** | `tools.md`、`project-file-paths.md`、`project-protocols-comm.md`、`deterministic-first.md`、`agent-config-file-paths.md` | `always` | 工具權限 + 路徑 + 通訊 + 原則 |
| **L3** | `role-execution.md`、`role-constraints.md`、`project-protocols-*.md`、`domain-knowledge-*.md` | `manual` | 完整流程、格式、測試規則、領域知識 |

> 理念：L1/L2 保持精簡（每次都用到嘅嘢），L3 按需 `fs_read`。

### 2.2 Steering 架構（每個 Agent 通用）

```
{agent}/.kiro/steering/
├── role.md                          ← L1 always（身份 + 核心規則）
├── navigation.md                    ← L1 always（文件清單 + 幾時讀）
├── anti-amnesia.md                  ← L1 always（防失憶）
├── tools.md                         ← L2 always（工具權限）
├── agent-config-file-paths.md       ← L2 always（配置路徑索引）
├── project-file-paths.md            ← L2 always（Project 路徑查表）
├── project-protocols-comm.md        ← L2 always（通訊協議）
├── deterministic-first.md           ← L2 always（確定性原則）
├── project-protocols-checkpoint.md  ← L3 manual（Checkpoint 規則）
├── project-protocols-decision-log.md ← L3 manual（Decision Log 規則）
├── project-protocols-memory.md      ← L3 manual（Memory 更新）
├── project-protocols-record-write.md ← L3 manual（寫入失敗處理）
├── project-protocols-format.md      ← L3 manual（格式一致性）
├── project-protocols-error-handling.md ← L3 manual（Error 處理）
├── project-protocols-size-rules.md  ← L3 manual（大任務拆分）
├── project-protocols-shell-policy.md ← L3 manual（Shell 使用政策）
├── role-execution.md                ← L3 manual（任務執行流程）
├── role-constraints.md              ← L3 manual（行為邊界）
└── domain-knowledge-*.md            ← L3 manual（領域知識，各 Agent 唔同）
```

### 2.3 Context Isolation（上下文隔離）

Sub Agent 唔需要知道完整大局，只需知自己嘅「介面定位」（上游邊個、下游邊個、output 點處理）。Worker 專注做好被派嘅任務，由 Main Agent 掌握大局。

### 2.4 Deterministic-First 原則 — 確定性任務用代碼

> **「可確定嘅嘢用代碼，唔確定嘅嘢用 AI」**

當 Task/Step 有標準答案、可驗證、重複性高、唔容許錯誤、或有明確規則時，
Agent 必須編寫 JS 腳本執行，唔可以用 LLM 推理代替。

腳本模板：`scripts/deterministic/_templates/`

### 2.5 Anti-Amnesia — 防止 Context Compaction 導致失憶

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

### 2.6 Decision Log — 每個 Step 記錄決策推理

每個 Agent 每完成一個 Step，必須記錄決策過程（零例外）：
- **有決定**（揀方案、設計選擇、判斷分數）→ 寫獨立 Decision Log 文件
- **冇決定**（純讀取 / 純格式化 / 機械操作）→ Checkpoint 加一行 `decision: mechanical — 無決策`

路徑：`ProjectRecord/{project}/decision-logs/{agent}/`
命名：`decision-log-{assignment-id}-step{N}-{step-name}.md`
同 Checkpoint 獨立存在：Checkpoint = 做咗咩（恢復用）；Decision Log = 點解咁做（審計用）

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
│   └── hooks/
│       ├── auto-log-session.kiro.hook        ← agentStop → 自動寫 session log
│       ├── auto-commit-config.kiro.hook      ← fileEdited (.kiro/) → 自動 commit
│       ├── watch-agent-replies.kiro.hook     ← fileCreated (outbox/) → 處理 reply
│       ├── sync-config-from-github.kiro.hook ← userTriggered → 同步 config
│       └── remind-update-config-deleted.kiro.hook ← fileDeleted (.kiro/) → 提醒更新
├── README.md                                 ← 本文件
├── .gitignore
├── scripts/
│   └── deterministic/
│       ├── _templates/
│       │   ├── deterministic-template.js
│       │   └── validator-template.js
│       └── README.md
├── UserConfig/
│   ├── sessions/                             ← 通用對話記錄（跨 Project）
│   └── session-log-entry-template.md
├── UserDocument/                             ← 通用設計文件
│
└── main-agent/                               ← Main Agent workspace
    ├── .kiro/
    │   ├── steering/                         ← Main Agent 規則（見 §2.2）
    │   ├── agents/                           ← Sub Agent 定義
    │   │   ├── planner.json
    │   │   ├── generator.json
    │   │   └── evaluator.json
    │   ├── hooks/
    │   │   ├── auto-log-session.kiro.hook
    │   │   ├── watch-planner-reply.kiro.hook
    │   │   ├── watch-generator-reply.kiro.hook
    │   │   └── watch-evaluator-reply.kiro.hook
    │   └── specs/
    │
    ├── Agents/                               ← 3 個 Sub Agent 各自嘅 steering
    │   ├── planner/.kiro/steering/           ← 見 §2.2 通用結構
    │   │   └── + domain-knowledge-tech-stack.md
    │   ├── generator/.kiro/steering/
    │   │   ├── + domain-knowledge-test-rules.md
    │   │   └── + domain-knowledge-code-standards.md
    │   └── evaluator/.kiro/steering/
    │       └── + domain-knowledge-evaluation-criteria.md
    │
    └── ProjectRecord/                        ← 所有 Project 記錄 + 產出
        ├── active-project.md                 ← 當前 active project（切換用）
        ├── templates/
        │   ├── assignment-template.md
        │   ├── assignment-reply-template.md
        │   ├── checkpoint-template.md
        │   ├── decision-log-template.md
        │   ├── conversation-log-entry-template.md
        │   ├── search-index-entry-template.md
        │   ├── verdict-template.md
        │   ├── progress-marker-template.md
        │   ├── session-log-entry-template.md
        │   ├── examples/
        │   └── specs/
        │
        └── {project-name}/                   ← 每個 Project 獨立空間（見 §6）
```

> ⚠️ Sub Agent 嘅 steering 存喺 `Agents/{agent}/`，但**運行時 CWD 係 `main-agent/`**，
> 所以 `./ProjectRecord/...` 解析到 `main-agent/ProjectRecord/`。

---

## 4. 每個 Agent 嘅 Steering 文件

### Main Agent（Orchestrator）
| 文件 | 層 | 幾時用 |
|------|----|--------|
| `role.md` | L1 | 身份 + 核心規則 |
| `navigation.md` | L1 | 文件清單 + 幾時讀 |
| `anti-amnesia.md` | L1 | 防失憶 |
| `tools.md` | L2 | 工具權限 |
| `agent-config-file-paths.md` | L2 | 配置路徑索引 |
| `project-file-paths.md` | L2 | Project 路徑 + 目錄結構圖 |
| `project-protocols-comm.md` | L2 | Sub Agent 調用規則 |
| `project-protocols-decision-log.md` | L3 | 每 Step 寫 Decision Log |
| `role-execution.md` | L3 | 派工 / 收 reply / 做決定時 |
| `role-constraints.md` | L3 | blocked / 循環限制 |
| `project-protocols-checkpoint.md` | L3 | Checkpoint 規則 |
| `project-protocols-git.md` | L3 | Git 操作前 |
| 其他 `project-protocols-*.md` | L3 | 按需讀取 |

### Planner
| 額外文件 | 用途 |
|---------|------|
| `domain-knowledge-tech-stack.md` | 選技術方案時 |

### Generator
| 額外文件 | 用途 |
|---------|------|
| `domain-knowledge-test-rules.md` | **寫 code 前必讀** |
| `domain-knowledge-code-standards.md` | 命名/安全/錯誤處理 |

### Evaluator
| 額外文件 | 用途 |
|---------|------|
| `domain-knowledge-evaluation-criteria.md` | 評分計算時 |

---

## 5. Agent 溝通流程

### 5.1 通訊媒介：文件

```
Main Agent ──寫 Assignment──▶ inbox/{agent}/assignment-{id}.md
                                      │
                              Sub Agent 讀取 + 執行
                                      │
Main Agent ◀──讀 Reply──── outbox/{agent}/assignment-{id}-reply-{status}.md
```

### 5.2 完整一輪流程

```
1. 用戶 → Main Agent 講需求
2. Main 讀 active-project.md → 確認當前 Project
3. Main 生成 Assignment ID（讀 SearchIndex 最後一行 +1）
4. Main 寫 inbox/planner/ → 調用 Planner
5. Planner 設計方案 → 寫 outbox/planner/ reply
6. Main 讀 reply → 寫 inbox/generator/ → 調用 Generator
7. Generator 寫 code+test → output/ + outbox/generator/ reply
8. Main 確認有 test → 寫 inbox/evaluator/ → 調用 Evaluator
9. Evaluator 跑 test + 評分 → outbox/evaluator/ verdict
10. Main 讀 verdict：PASS → 交付 / FAIL → 退回 / REPLAN → 重設計
11. 全程每步：checkpoint + decision-log + conversation-log + SearchIndex
```

### 5.3 調用 Sub Agent

| 方法 | 指令 | 幾時用 |
|------|------|--------|
| **Kiro CLI**（優先） | `kiro-cli chat --agent {name} "{prompt}"` | kiro-cli 可用 |
| **invoke_sub_agent**（Fallback） | `invoke_sub_agent` + `contextFiles` | kiro-cli 唔得時 |

### 5.4 自動化 Hooks

| Hook | 位置 | 觸發 | 做咩 |
|------|------|------|------|
| `auto-log-session` | Root + Main | agentStop | 自動寫 session log |
| `watch-planner-reply` | Main | fileCreated (outbox/planner/) | 讀 Planner reply |
| `watch-generator-reply` | Main | fileCreated (outbox/generator/) | 讀 Generator reply |
| `watch-evaluator-reply` | Main | fileCreated (outbox/evaluator/) | 讀 Evaluator reply |
| `auto-commit-config` | Root | fileEdited (.kiro/) | 自動 commit config |
| `sync-config-from-github` | Root | userTriggered | 同步 config |
| `remind-update-config-deleted` | Root | fileDeleted (.kiro/) | 提醒更新 config |

---

## 6. Project 結構 + 切換/新增

### 6.1 每個 Project 嘅獨立空間
```
ProjectRecord/{project-name}/
├── specs/                    ← requirements.md / design.md / tasks.md
├── memory/                   ← {main-agent,planner,generator,evaluator}-memory.md
├── inbox/                    ← 收件（planner/generator/evaluator/main-agent）
├── outbox/                   ← 發件（同上）
├── checkpoints/              ← 執行記錄（斷線恢復，按 agent 分）
├── decision-logs/            ← 決策推理記錄（審計/學習，按 agent 分）
├── output/                   ← Generator 生成嘅代碼
├── control/                  ← 控制指令
├── SearchIndex.md            ← 搜尋索引
├── conversation-log.md       ← 對話記錄（append-only）
├── UserConfig/sessions/      ← 本 Project session 記錄
└── UserDocument/             ← 本 Project 用戶文件
```

### 6.2 切換 Project
改 `ProjectRecord/active-project.md` 嘅 `current:` 值。

### 6.3 新增 Project
1. 執行 `node scripts/deterministic/create-project.js <project-name>`
2. 改 `active-project.md` 嘅 `current`

> 或手動：建 §6.1 全部子目錄 + 空白 SearchIndex + conversation-log。

---

## 7. 點樣開始用

1. 開 Kiro → **Open Folder** → 揀 `main-agent/`
2. 確認 `ProjectRecord/active-project.md` 指向你想做嘅 Project
3. 直接同 Main Agent 講需求
4. Main Agent 自動調度 Planner → Generator → Evaluator
5. 完成後 Main Agent 問你要唔要 Git 操作

> 💡 Root 層放跨 Project 嘅通用規則、session log、hooks。日常開發喺 `main-agent/`。

---

## 8. 維護指引

### 修改 Config 後必須檢查本文件

任何對 `.kiro/steering/`、`.kiro/hooks/`、`templates/`、`ProjectRecord/` 結構嘅修改，
都應該同步更新本 README。Root Agent 有 hook 自動提醒評估。

### 設計原則總結
- **漸進式披露**：L1/L2 always 精簡，L3 按需 → 慳 token
- **單一邏輯來源**：每個 protocol 一份文件，複製去各 Agent
- **導航清晰**：navigation.md + project-file-paths.md 回答「有咩文件、幾時讀」
- **零例外記錄**：Checkpoint（做咗咩）+ Decision Log（點解咁做）
- **防失憶**：progress-marker 每步更新，~20 tokens/step
