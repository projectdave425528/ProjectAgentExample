# Claude Code Harness Engineering 結構圖

> 整理自公開文檔同社區資料
> 對比用途：了解 Claude Code 的配置機制，同 Kiro 做比較
> 更新日期：2026-05-22

---

## 完整架構圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                         用戶（你）                                    │
│                    輸入指令 / 對話 / Slash Commands                    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Claude Code Agent（AI 大腦）                       │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  讀取        │  │  調用        │  │  監聽        │                 │
│  │  CLAUDE.md   │  │  Subagents   │  │  Hooks      │                 │
│  │  + Rules     │  │  + Skills    │  │             │                 │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                 │
│         │                │                │                         │
└─────────┼────────────────┼────────────────┼─────────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    .claude/ 目錄（Harness 核心）                      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ CLAUDE.md              ← 主記憶文件（等同 Kiro 的 Steering）   │   │
│  │                           每次 session 自動載入               │   │
│  │                           建議 < 200 行                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ rules/                 ← 模組化規則（等同 Kiro 多個 Steering） │   │
│  │ ├── code-style.md         代碼風格規則                        │   │
│  │ ├── testing.md            測試規範                            │   │
│  │ ├── security.md           安全規則                            │   │
│  │ └── *.md                  按主題拆分                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ hooks/                 ← 自動化觸發器（同 Kiro Hooks 類似）    │   │
│  │ ├── pre-commit.sh         commit 前執行                       │   │
│  │ ├── post-edit.sh          編輯後執行                          │   │
│  │ └── *.sh / *.json         事件驅動腳本                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ skills/                ← 技能包（同 Kiro Agent Skills 相同標準）│   │
│  │ ├── skill-name/                                               │   │
│  │ │   ├── SKILL.md          技能入口（frontmatter + 指令）      │   │
│  │ │   ├── scripts/          輔助腳本                            │   │
│  │ │   └── reference/        參考資料                            │   │
│  │ └── ...                                                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ agents/                ← Subagents（Kiro 冇呢個概念）          │   │
│  │ ├── code-reviewer.md      代碼審查 Agent                      │   │
│  │ ├── test-writer.md        測試撰寫 Agent                      │   │
│  │ └── *.md                  專門化子 Agent                      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ commands/              ← 自定義 Slash Commands                 │   │
│  │ ├── review.md             /review 命令                        │   │
│  │ ├── deploy.md             /deploy 命令                        │   │
│  │ └── *.md                  自定義 /命令                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ settings.json          ← 權限同配置                            │   │
│  │                           MCP servers、權限控制、模型選擇      │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 各文件作用詳解

### CLAUDE.md（主記憶）

```
位置：項目根目錄 / .claude/CLAUDE.md / ~/.claude/CLAUDE.md
作用：每次 session 自動載入的持久化指令
等同 Kiro：所有 Steering 文件合併成一個
```

| 特點 | 說明 |
|------|------|
| 自動載入 | 每次 session 開始時讀取 |
| 建議長度 | < 200 行（太長會降低遵從度） |
| 多層級 | 項目級 > 目錄級 > 全局級 |
| 格式 | 純 Markdown，冇 front matter |

---

### rules/（模組化規則）

```
位置：.claude/rules/*.md
作用：將 CLAUDE.md 拆分成多個主題文件
等同 Kiro：多個 Steering 文件（但冇 inclusion 模式控制）
```

| 同 Kiro 的分別 | Claude Code | Kiro |
|---|---|---|
| 條件載入 | ❌ 全部自動載入 | ✅ fileMatch / manual / auto |
| 手動引用 | ❌ | ✅ `#文件名` |
| File Reference | ❌ | ✅ `#[[file:path]]` |

---

### hooks/（自動化）

```
位置：.claude/hooks/
作用：事件驅動的自動化腳本
等同 Kiro：.kiro/hooks/
```

| 對比 | Claude Code | Kiro |
|------|-------------|------|
| 格式 | Shell script 或 JSON | JSON（.kiro.hook） |
| 事件類型 | 較少（pre/post edit、commit） | 10 種 |
| 動作 | 執行命令 | askAgent + runCommand |
| preToolUse 攔截 | ✅ | ✅ |

---

### skills/（技能包）

```
位置：.claude/skills/ 或 ~/.claude/skills/
作用：可重用的專業能力包
等同 Kiro：完全相同（共用 AgentSkills 標準）
```

**Skills 可以喺 Kiro 同 Claude Code 之間互通。**

---

### agents/（Subagents）

```
位置：.claude/agents/ 或 ~/.claude/agents/
作用：專門化的子 Agent，處理特定任務
等同 Kiro：Kiro 有內建 Sub Agent（context-gatherer、general-task-execution），但自定義能力較弱
```

#### 內建 Sub Agents

| Agent | Model | 用途 | 工具權限 |
|-------|-------|------|---------|
| **Explore** | Haiku（快） | 搜尋/分析 codebase | 只讀 |
| **Plan** | 繼承主 Agent | 規劃前收集 context | 只讀 |
| **General-purpose** | 繼承主 Agent | 複雜多步驟任務 | 全部 |

#### 常見自定義 Sub Agent 類型

| Agent 類型 | 用途 | 工具權限 |
|-----------|------|---------|
| Planner | 分析需求、設計方案、拆分任務 | 只讀 |
| Generator | 根據計劃生成代碼/文件 | 全部 |
| Evaluator | 檢查輸出質量、驗證正確性 | 只讀 + 執行測試 |
| Researcher | 搜尋 codebase、收集資料 | 只讀 |
| Reviewer | 代碼審查、安全掃描 | 只讀 |
| Test Writer | 寫測試 | 全部 |

#### 核心協作模式：Planner → Generator → Evaluator

```
Planner（規劃）→ Generator（生成）→ Evaluator（評估）
                                         │
                              ✅ PASS → 交付
                              ❌ FAIL → 返回 Generator 重做
                              🔄 REPLAN → 返回 Planner 重新規劃
```

呢個係 Anthropic 官方推薦的 Evaluator-Optimizer Loop，詳見 `Claude_SubAgent_Workflow.md`。

#### Sub Agent 配置格式

```markdown
---
name: planner
description: Analyzes requirements and creates implementation plans
model: sonnet
tools:
  - Read
  - Grep
denied_tools:
  - Write
  - Edit
---

# Planner Agent
[指令內容]
```

#### Sub Agent 特性

| 特性 | 說明 |
|------|------|
| 獨立 context | 每個 subagent 有自己的 context window |
| 獨立 model | 可以指定 Haiku（快/平）或 Sonnet（強） |
| 工具限制 | 可以限制只讀、禁止寫入等 |
| 記憶 | 可配置 persistent memory（`~/.claude/agent-memory/`） |
| 唔能嵌套 | Subagent 唔能再 spawn subagent |
| 載入 CLAUDE.md | 除 Explore/Plan 外，其他 subagent 都會載入 |

---

### commands/（Slash Commands）

```
位置：.claude/commands/
作用：自定義 /命令，快速觸發特定工作流
等同 Kiro：❌ Kiro 用 Steering manual inclusion 代替
```

例子：
- `/review` → 執行代碼審查流程
- `/deploy` → 執行部署流程
- `/test` → 執行測試流程

---

### settings.json（系統配置）

```
位置：.claude/settings.json
作用：權限控制、MCP 配置、模型選擇
等同 Kiro：.kiro/settings/mcp.json（但 Kiro 冇權限系統）
```

---

## Kiro vs Claude Code 對照表

| 機制 | Kiro 文件 | Claude Code 文件 | 差異 |
|------|-----------|-----------------|------|
| 主記憶 | `.kiro/steering/*.md` | `CLAUDE.md` + `.claude/rules/` | Kiro 有 4 種 inclusion 模式 |
| 自動化 | `.kiro/hooks/*.kiro.hook` | `.claude/hooks/` | Kiro 有 10 種事件 |
| 技能包 | `~/.kiro/skills/` | `~/.claude/skills/` | 相同標準，可互通 |
| 結構化開發 | `.kiro/specs/` | ❌ 冇 | Kiro 獨有 |
| 子 Agent | ❌ 冇 | `.claude/agents/` | Claude Code 獨有 |
| Slash 命令 | ❌ 冇 | `.claude/commands/` | Claude Code 獨有 |
| 工具連接 | `.kiro/settings/mcp.json` | `settings.json` 內 | 類似 |
| 權限控制 | ❌ 冇 | `settings.json` 內 | Claude Code 獨有 |

---

## 一句話總結

```
Claude Code：
  CLAUDE.md + rules = 記憶
  hooks             = 自動化
  skills            = 技能
  agents            = 子 Agent（獨有）
  commands          = 快捷命令（獨有）
  settings.json     = 權限 + 工具

Kiro：
  steering          = 記憶（更精細的載入控制）
  hooks             = 自動化（更多事件類型）
  skills            = 技能（同標準）
  specs             = 結構化開發（獨有）
  mcp.json          = 工具
```

---

## 參考資源

| 資源 | 連結 |
|------|------|
| Claude Code 官方 .claude 目錄文檔 | https://code.claude.com/docs/en/claude-directory |
| .claude 目錄完整指南 | https://computingforgeeks.com/claude-code-dot-claude-directory-guide/ |
| Claude Code Harness Engineering 完整指南 | https://www.paradime.io/guides/claude-code-skills-plugins-rules-guide |
| CLAUDE.md + Rules + Hooks + Skills 地圖 | https://mer.vin/2026/05/claude-code-claude-directory-claude-md-rules-hooks-and-skills-map/ |
| .claude 目錄解剖 | https://codewithmukesh.com/blog/anatomy-of-the-claude-folder/ |
| Claude Code 完整指南（Hooks, MCP, Skills） | https://www.blakecrosley.com/guide/claude-code |
