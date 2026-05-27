# Claude Code Sub Agent 用法流程圖

> 整理自公開文檔同社區資料
> 更新日期：2026-05-22

---

## 概覽

Claude Code 的 Sub Agent 系統允許主 Agent 派任務俾多個專門化子 Agent，佢哋可以並行執行、透過共享狀態間接交流。

---

## 五種工作模式

---

### 模式 1：Sequential Flow（順序執行）

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Agent 1  │────▶│ Agent 2  │────▶│ Agent 3  │
│ 探索     │     │ 規劃     │     │ 執行     │
│          │     │          │     │          │
│ 分析代碼 │     │ 設計方案 │     │ 寫代碼   │
│ 搵依賴   │     │ 定架構   │     │ 寫測試   │
└──────────┘     └──────────┘     └──────────┘
     結果傳遞 →       結果傳遞 →
```

**適合場景：**
- 先了解 codebase → 再設計 → 再實現
- 每一步依賴上一步的結果
- 需要深度分析後再行動

**觸發方式：**
```
你：「幫我重構 auth 模組」
Claude：探索 → 規劃 → 執行（自動串聯）
```

---

### 模式 2：Operator（中央調度）

```
                    ┌──────────────┐
                    │   主 Agent    │
                    │  （調度員）    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Sub A    │ │ Sub B    │ │ Sub C    │
        │ 搜尋代碼 │ │ 寫測試   │ │ 重構     │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │   主 Agent    │
                    │  匯總 + 檢查  │
                    └──────────────┘
```

**適合場景：**
- 多個獨立任務可以同時做
- 需要最終匯總同品質檢查
- 任務之間冇依賴

**觸發方式：**
```
你：「幫我同時做 lint fix、寫 unit test、更新文件」
Claude：派三個 Sub Agent 並行 → 匯總結果
```

---

### 模式 3：Split and Merge（分拆合併）

```
                    ┌──────────────┐
                    │   主 Agent    │
                    │  拆分任務     │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Branch A │ │ Branch B │ │ Branch C │
        │ Feature 1│ │ Feature 2│ │ Feature 3│
        │          │ │          │ │          │
        │ 獨立     │ │ 獨立     │ │ 獨立     │
        │ Worktree │ │ Worktree │ │ Worktree │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │   主 Agent    │
                    │  Merge 所有   │
                    │  Branch       │
                    │  解決衝突     │
                    └──────────────┘
```

**適合場景：**
- 大型功能可以拆成獨立部分
- 各部分唔會修改相同文件
- 需要最終合併同衝突解決

**觸發方式：**
```
你：「幫我同時開發 payment、notification、dashboard 三個模組」
Claude：各自開 branch → 並行開發 → merge
```

**關鍵技術：Git Worktree**
```bash
git worktree add ../feature-1 -b feature/payment
git worktree add ../feature-2 -b feature/notification
git worktree add ../feature-3 -b feature/dashboard
```

---

### 模式 4：Agent Teams（自主協作）⭐

```
┌─────────────────────────────────────────────────────────┐
│                   共享 Task List                          │
│                  （tasks.md）                             │
│                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │ Agent A │    │ Agent B │    │ Agent C │            │
│  │         │    │         │    │         │            │
│  │ 1.讀取  │    │ 1.讀取  │    │ 1.讀取  │            │
│  │   Task  │    │   Task  │    │   Task  │            │
│  │   List  │    │   List  │    │   List  │            │
│  │         │    │         │    │         │            │
│  │ 2.Claim │    │ 2.Claim │    │ 2.Claim │            │
│  │   未完成│    │   未完成│    │   未完成│            │
│  │   Task  │    │   Task  │    │   Task  │            │
│  │         │    │         │    │         │            │
│  │ 3.執行  │    │ 3.執行  │    │ 3.執行  │            │
│  │         │    │         │    │         │            │
│  │ 4.標記  │    │ 4.標記  │    │ 4.標記  │            │
│  │   完成  │    │   完成  │    │   完成  │            │
│  └────┬────┘    └────┬────┘    └────┬────┘            │
│       │              │              │                  │
│       └──────────────┼──────────────┘                  │
│                      ▼                                  │
│              更新 Task List                              │
│              其他 Agent 可見                             │
└─────────────────────────────────────────────────────────┘
```

**協調機制：**
```
Task List（共享狀態）：
  - [x] Task 1: Setup DB schema        ← Agent A 完成
  - [x] Task 2: Create API routes      ← Agent B 完成
  - [ ] Task 3: Write frontend         ← Agent C 進行中
  - [ ] Task 4: Integration tests      ← 未 claim
  - [ ] Task 5: Documentation          ← 未 claim
```

**適合場景：**
- 多人協作的大型項目
- 任務可以獨立完成
- 需要避免重複工作

**Agent 之間「交流」的方式：**
```
唔係直接對話，而係透過：
1. 共享 Task List（讀寫同一個文件）
2. 共享文件系統（Agent A 寫的文件，Agent B 可以讀）
3. MCP Memory Server（共享記憶）
4. Git commits（睇到其他 Agent 的修改）
```

---

### 模式 5：Headless（全自動）

```
┌──────────┐     ┌──────────────────────────┐     ┌──────────┐
│ 觸發事件 │────▶│     Claude Code Agent     │────▶│ 輸出結果 │
│          │     │                          │     │          │
│ • CI/CD  │     │  自主完成所有步驟：        │     │ • PR     │
│ • Cron   │     │  1. 分析問題              │     │ • Report │
│ • Webhook│     │  2. 設計方案              │     │ • Deploy │
│          │     │  3. 寫代碼               │     │          │
└──────────┘     │  4. 寫測試               │     └──────────┘
                 │  5. 開 PR                │
                 │                          │
                 │  人類唔需要介入            │
                 └──────────────────────────┘
```

**適合場景：**
- CI/CD 自動修復
- 定期維護任務
- 自動回應 Issue

---

## Sub Agent 配置方式

### 文件結構
```
.claude/
└── agents/
    ├── code-reviewer.md      ← 代碼審查 Agent
    ├── test-writer.md        ← 測試撰寫 Agent
    ├── doc-generator.md      ← 文件生成 Agent
    └── security-auditor.md   ← 安全審計 Agent
```

### Agent 定義格式
```markdown
# Code Reviewer Agent

## Role
你係一個專門做代碼審查的 Agent。

## Instructions
1. 檢查代碼風格是否符合 .eslintrc
2. 檢查有冇安全漏洞
3. 檢查測試覆蓋率
4. 提供改善建議

## Tools
- 可以讀取文件
- 可以執行 lint 命令
- 唔可以修改文件（只讀）

## Output Format
- 列出問題清單
- 每個問題標注嚴重程度（Critical / Warning / Info）
```

---

## 實際使用流程

### 步驟 1：定義 Agents
```
.claude/agents/ 入面建立各個 Agent 的 .md 文件
```

### 步驟 2：觸發
```
你：「用 code-reviewer 同 test-writer 幫我檢查 src/ 目錄」
```

### 步驟 3：Claude 調度
```
主 Agent 讀取 agent 定義 → 派任務 → 並行執行
```

### 步驟 4：結果匯總
```
Sub Agent 各自完成 → 結果返回主 Agent → 匯總報告
```

---

## 核心協作模式：Planner → Generator → Evaluator

### 概念

呢個係 Multi-Agent 系統最常見的三角循環模式（Anthropic 官方稱為 Evaluator-Optimizer Loop）：

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│    ┌──────────┐     ┌──────────┐     ┌──────────┐      │
│    │ Planner  │────▶│Generator │────▶│Evaluator │      │
│    │ (規劃)   │     │ (生成)   │     │ (評估)   │      │
│    └──────────┘     └──────────┘     └────┬─────┘      │
│         ▲                                  │            │
│         │           ┌──────────┐           │            │
│         │           │ 反饋     │◀──────────┘            │
│         │           │ Feedback │                        │
│         │           └────┬─────┘                        │
│         │                │                              │
│         │    ┌───────────┴───────────┐                  │
│         │    │                       │                  │
│         │    ▼                       ▼                  │
│         │  通過 ✅                 拒絕 ❌               │
│         │  → 輸出結果              → 返回 Generator     │
│         │                           重新生成            │
│         │                                              │
│         └──────────── 如果需要重新規劃 ─────────────────┘
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 三個角色詳解

| 角色 | 職責 | 工具權限 | Model 建議 |
|------|------|---------|-----------|
| **Planner** | 分析需求、拆分任務、設計方案 | 只讀（Read/Search） | Sonnet（需要推理） |
| **Generator** | 根據計劃生成代碼/文件/方案 | 全部（Read/Write/Bash） | Sonnet（需要創造力） |
| **Evaluator** | 檢查輸出質量、驗證正確性 | 只讀 + 執行測試 | Haiku（快速判斷）或 Sonnet |

### 實際流程

```
Step 1: Planner
  輸入：用戶需求
  輸出：結構化任務清單 + 技術方案
  
Step 2: Generator
  輸入：Planner 的任務清單
  輸出：代碼 / 文件 / 配置
  
Step 3: Evaluator
  輸入：Generator 的輸出
  判斷：
    ✅ PASS → 交付結果
    ❌ FAIL → 反饋具體問題 → 返回 Generator 重做
    🔄 REPLAN → 問題太大 → 返回 Planner 重新規劃
```

### Claude Code 實現方式

```
.claude/agents/
├── planner.md          ← 規劃 Agent
├── generator.md        ← 生成 Agent
└── evaluator.md        ← 評估 Agent
```

#### planner.md
```markdown
---
name: planner
description: Analyzes requirements and creates structured implementation plans
model: sonnet
tools:
  - Read
  - Grep
  - Glob
denied_tools:
  - Write
  - Edit
  - Bash
---

# Planner Agent

## Role
分析需求，了解現有 codebase，設計技術方案，拆分成可執行任務。

## Process
1. 用 Explore 了解相關代碼結構
2. 識別影響範圍同依賴
3. 設計技術方案
4. 拆分成獨立任務（標注依賴關係）

## Output
- 技術方案摘要（< 500 字）
- 任務清單（JSON 格式，含 id、description、dependencies）
- 風險評估
```

#### generator.md
```markdown
---
name: generator
description: Implements code based on plans from the planner agent
model: sonnet
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Generator Agent

## Role
根據 Planner 的任務清單，逐步實現代碼。

## Rules
- 嚴格按照 Planner 的方案執行
- 每完成一個 Task 就標記完成
- 遇到方案不可行時，返回具體原因
- 寫完代碼必須確保可編譯
```

#### evaluator.md
```markdown
---
name: evaluator
description: Reviews and validates output from the generator agent
model: sonnet
tools:
  - Read
  - Grep
  - Glob
  - Bash
denied_tools:
  - Write
  - Edit
---

# Evaluator Agent

## Role
檢查 Generator 的輸出是否符合 Planner 的方案同品質標準。

## Checklist
1. 代碼是否可編譯/運行
2. 是否符合 Planner 的技術方案
3. 是否有明顯 bug 或安全問題
4. 測試是否通過
5. 代碼風格是否一致

## Output
- PASS：輸出符合要求，可以交付
- FAIL：列出具體問題，返回 Generator 修正
- REPLAN：方案有根本問題，需要返回 Planner
```

### 同其他模式的關係

```
Planner-Generator-Evaluator 係 Anthropic 官方 5 種模式之一：

1. Orchestrator-Workers    ← 中央調度（Operator 模式）
2. Evaluator-Optimizer     ← 就係 Planner-Generator-Evaluator ⭐
3. Routing                 ← 按任務類型分流
4. Parallelization         ← 並行執行
5. Sequential Pipeline     ← 順序執行
```

---

## 同 Kiro 的對比

| | Claude Code | Kiro |
|---|---|---|
| Planner | `.claude/agents/planner.md` | Spec（requirements.md + design.md） |
| Generator | `.claude/agents/generator.md` | Spec Task 執行 |
| Evaluator | `.claude/agents/evaluator.md` | Hook（postTaskExecution） |
| 循環反饋 | ✅ Agent 之間自動循環 | ⚠️ 需要手動觸發 |
| 自動重試 | ✅ Evaluator FAIL → Generator 重做 | ❌ |

**Kiro 的 Spec workflow 本質上就係 Planner-Generator 模式，但缺少 Evaluator 自動循環。**

---

```
Claude Code Multi-Agent：
┌─────────────────────────────────────────┐
│ 主 Agent                                │
│   ├── Sub Agent A（獨立 context）        │
│   ├── Sub Agent B（獨立 context）        │
│   └── Sub Agent C（獨立 context）        │
│                                         │
│ 交流方式：共享 Task List / 文件 / Memory │
│ 配置方式：.claude/agents/*.md            │
│ 並行方式：Git Worktree / 獨立 instance   │
└─────────────────────────────────────────┘

Kiro Multi-Agent：
┌─────────────────────────────────────────┐
│ 主 Agent                                │
│   ├── context-gatherer（內建）           │
│   ├── general-task-execution（內建）     │
│   └── custom-agent（可自定義 prompt）    │
│                                         │
│ 交流方式：只能透過主 Agent 中轉          │
│ 配置方式：custom-agent-creator 建立      │
│ 並行方式：Spec Task Wave 機制            │
└─────────────────────────────────────────┘
```

---

## 參考資源

| 資源 | 連結 |
|------|------|
| Claude Code Sub-Agents 完整指南 | https://www.aibuilderclub.com/blog/claude-code-sub-agents-guide |
| 5 種工作流模式 | https://popularaitools.ai/blog/claude-code-workflow-patterns-agentic-guide-2026 |
| Agent Teams 並行協作 | https://www.mindstudio.ai/blog/claude-code-agent-teams-parallel-workflows |
| Multi-Agent 協調模式（官方） | https://claude.com/blog/multi-agent-coordination-patterns |
| Claude Code 完整指南 | https://www.blakecrosley.com/guide/claude-code |
| Parallel Agents 完整指南 | https://www.vibecodingacademy.ai/blog/claude-code-subagents-complete-guide |
| Multi-Agent 系統 2026 指南 | https://www.eesel.ai/blog/claude-code-multiple-agent-systems-complete-2026-guide |
