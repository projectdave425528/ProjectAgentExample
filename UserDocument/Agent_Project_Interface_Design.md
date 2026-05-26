# Agent-Project Interface 設計文件

> 整理日期：2026-05-27
> 來源：ProjectKiro 學習筆記 + 大公司做法研究

---

## 核心問題

**點樣設計令 Agent 同 Project 互不影響？**
- 改 Agent（steering、hooks、prompt）→ Project 唔受影響
- 改 Project（代碼、架構、技術棧）→ Agent 唔受影響

---

## 設計原則：Convention over Configuration

目錄結構 = Interface。唔需要 contract.md 文件，約定好目錄格式就係 contract。

---

## 三層分離架構

```
Project/                    ← 項目本身（代碼、配置、業務邏輯）
├── src/
├── docs/
└── ...

Agent/                      ← Agent 定義（可隨時修改）
├── .kiro/steering/         ← 行為規則
├── .kiro/hooks/            ← 自動化觸發
└── .kiro/agents/           ← Sub-agent 定義

Interface（紀錄層）/        ← 兩者之間嘅唯一接觸點
├── inbox/                  ← Project → Agent 嘅任務
├── outbox/                 ← Agent → Project 嘅結果
└── state.md                ← 當前狀態（可選）
```

---

## Interface 文件說明

### inbox/（任務輸入）

| 欄位 | 說明 |
|------|------|
| 性質 | 一次性任務文件 |
| 生命週期 | 用完可刪/歸檔 |
| 寫入者 | Orchestrator / 用戶 |
| 讀取者 | 目標 Agent |
| 格式 | `task-{id}.md` |

### outbox/（結果輸出）

| 欄位 | 說明 |
|------|------|
| 性質 | 一次性結果文件 |
| 生命週期 | 用完可刪/歸檔 |
| 寫入者 | 目標 Agent |
| 讀取者 | Orchestrator / 用戶 |
| 格式 | `task-{id}-reply.md` |

### session log（歷史紀錄）

| 欄位 | 說明 |
|------|------|
| 性質 | 累積歷史（append-only） |
| 生命週期 | 永久保留 |
| 用途 | 回顧、debug、審計 |
| 位置 | `UserConfig/sessions/` |

### conversation-log vs session log

| | conversation-log | session log |
|---|---|---|
| 內容 | 每個任務一行摘要 | 完整對話記錄 |
| 用途 | 快速回顧流程 | 詳細 debug |
| 是否必要 | 可選（如果 session log 夠用就唔需要） |

---

## 改動自由度

### Agent 改動（唔影響 Project）

| 改動 | 影響 |
|------|------|
| 改 steering | ✅ 唔影響（Project 只睇 outbox） |
| 改 hooks | ✅ 唔影響 |
| 改 prompt 風格 | ✅ 只要 outbox 格式唔變 |
| 改 Agent 數量 | ✅ Orchestrator 負責調度 |
| 換 LLM model | ✅ 唔影響 |

### Project 改動（唔影響 Agent）

| 改動 | 影響 |
|------|------|
| 改代碼結構 | ✅ 唔影響（Agent 只睇 inbox） |
| 改技術棧 | ⚠️ 需要更新 inbox 嘅 context 資訊 |
| 改需求 | ✅ 寫新 inbox task 就得 |

### 唯一 Breaking Change

**inbox/outbox 嘅 message 格式改變** — 呢個等同於改 API contract，需要兩邊同步更新。

---

## 大公司做法參考

### 1. Google ADK — Microservices 模式

- Agent 係獨立 microservice，各自部署
- 用 A2A Protocol（Agent-to-Agent）通訊
- Agent 有自己嘅 repo、config、獨立部署
- Project 只定義「需要邊啲 Agent」+ 「點樣 orchestrate」

### 2. Microsoft — Agent Registry

- 中央 Registry 登記所有 Agent 嘅能力、endpoint、版本
- Project 透過 Registry 查詢 Agent，唔直接 import
- 支援 Modular Monolith（開發）→ Distributed（production）

### 3. Anthropic — Interface Layer（Managed Agents）

- Agent runtime 虛擬化成 3 個獨立 interface 層
- Agent 行為同部署環境完全分離

### 4. 分散式系統經典模式

| 模式 | 原理 | 對應你嘅設計 |
|------|------|------------|
| Blackboard | 共享空間，Agent 讀寫 | inbox/outbox |
| Pub-Sub | 發布事件，訂閱者處理 | Hook 觸發 |
| Message Queue | 中間緩衝，異步處理 | inbox 排隊 |

---

## 對應 Kiro 嘅實現

### 目錄結構（Convention = Interface）

```
C:\Users\proje\ProjectAgentExample\
├── main-agent/
│   ├── .kiro/steering/     ← Agent 行為
│   ├── .kiro/hooks/        ← 自動化
│   ├── inbox/              ← 接收任務
│   └── outbox/             ← 回覆結果
├── planner/
│   ├── .kiro/steering/
│   ├── inbox/
│   └── outbox/
├── generator/
│   └── ...
└── evaluator/
    └── ...
```

### 調用方式（CLI）

```powershell
kiro-cli chat --agent [agent-name] "[prompt]"
```

- CLI 獨立開 Kiro instance
- 讀取目標目錄嘅 .kiro/steering/ 同 hooks/
- 唔需要目標目錄喺 workspace 入面

### 流程

```
用戶需求
  → Orchestrator 寫 inbox/task-001.md
  → CLI 調用 Planner
  → Planner 寫 outbox/task-001-reply.md
  → Orchestrator 讀取 → 寫 Generator inbox
  → CLI 調用 Generator
  → Generator 寫 outbox
  → Orchestrator 讀取 → 寫 Evaluator inbox
  → CLI 調用 Evaluator
  → PASS → 交付
  → FAIL → 回 Generator（最多 3 次）
```

---

## Kiro 特有注意事項

### Hook 衝突問題

- Kiro 會遞歸掃描 workspace 所有 `.kiro/hooks/`
- 子項目嘅 hook 會同根目錄衝突
- 解決：子項目放 workspace 外面，或加 `"enabled": false`

### Steering 載入

- Single-Folder：只有根目錄 `.kiro/steering/` 生效
- Multi-Root：每個 folder 獨立載入（但全部 always 都會消耗 Token）
- 最佳做法：子項目放外面，用 CLI 調用時自動讀取自己嘅 steering

### Multi-Root vs Single-Folder

| | Single-Folder | Multi-Root |
|---|---|---|
| Hook 隔離 | ❌ 全部觸發 | ❌ 仍然全部觸發 |
| Steering 隔離 | ✅ 只有根目錄 | ❌ 全部載入 |
| 最佳用法 | 日常工作 | 需要同時睇多個項目 |

**結論：子項目放 workspace 外面 + CLI 調用 = 最乾淨嘅隔離。**

---

## 設計決策記錄

| 日期 | 決策 | 原因 |
|------|------|------|
| 2026-05-26 | 子項目搬出 ProjectKiro repo | 避免 hook 衝突 + 獨立演進 |
| 2026-05-26 | 用 `enabled: false` 停用子項目 hook | 即時解決重複觸發 |
| 2026-05-26 | 保留 .code-workspace 但唔強制用 | Multi-Root 唔解決 hook 問題 |
| 2026-05-26 | inbox/outbox 格式 = contract | Convention over Configuration |
| 2026-05-26 | 唔需要 conversation-log | session log 已夠用 |
