# Kiro Harness Engineering 機制完整指南

> 整理自 Kiro 官方文檔 [kiro.dev/docs](https://kiro.dev/docs)
> 更新日期：2026-05-20

---

## 概覽

Kiro 的 Harness Engineering 係指一套**控制 AI Agent 執行任務的框架**，由五個核心機制組成：

```
Kiro Harness Engineering
├── Specs          → 結構化開發流程
├── Steering       → 持久化 AI 指引
├── Hooks          → 事件驅動自動化
├── MCP Servers    → 外部工具連接
└── Agent Skills   → 可重用 AI 技能包
```

---

## 一、Specs（規格驅動開發）

### 簡介

Specs 係將高層次想法轉化為詳細實施計劃的結構化工件，提供系統化的開發流程，包含清晰的追蹤和問責機制。

### 三個核心文件

| 文件 | 用途 |
|------|------|
| `requirements.md` | 用 EARS 格式記錄用戶故事同驗收標準 |
| `bugfix.md` | Bug 分析（現有行為 / 預期行為 / 不變行為） |
| `design.md` | 技術架構、Sequence Diagram、組件設計、錯誤處理 |
| `tasks.md` | 可追蹤的實施任務清單，支援並行執行 |

### Spec 類型（4種）

#### 1. Feature Spec — Requirements-First
- **適合**：由需求出發，產品驅動開發，Greenfield 項目
- **流程**：Requirements → Design → Tasks
- **特點**：先定義系統行為，再設計技術方案

#### 2. Feature Spec — Design-First
- **適合**：已有架構設計，技術限制嚴格，從其他工具移植設計文件
- **流程**：Design → Requirements → Tasks
- **特點**：先確定技術可行性，再推導需求範圍

#### 3. Feature Spec — Quick Plan
- **適合**：對功能已有充分了解，信任 Kiro 輸出
- **流程**：一次過自動生成三個文件，無需逐步審批
- **特點**：回答澄清問題後直接跳到 Task 清單

#### 4. Bugfix Spec
- **適合**：系統性診斷同修復 Bug，防止回歸
- **流程**：Bug Analysis → Fix Design → Tasks
- **特點**：識別根本原因，驗證修復不影響其他功能

### EARS 需求格式

```
WHEN [條件/事件] THE SYSTEM SHALL [預期行為]
```

例子：
```
WHEN a user submits a form with invalid data
THE SYSTEM SHALL display validation errors next to the relevant fields
```

### Task 並行執行機制

Kiro 分析 `tasks.md` 的依賴關係，建立 Dependency Graph，分組成 Wave 執行：

- **Wave 1**：所有無依賴的 Task，並行執行
- **Wave 2**：依賴 Wave 1 完成的 Task，並行執行
- **Wave N**：依此類推，直到全部完成

### 何時用 Spec vs Vibe

| 用 Spec | 用 Vibe |
|---------|---------|
| 複雜功能需要結構化規劃 | 快速探索性編碼 |
| Bug 修復需防止回歸 | 目標不明確的原型開發 |
| 需要團隊協作文件 | |
| 需求或設計需要反覆迭代 | |

---

## 二、Steering（持久化 AI 指引）

### 簡介

Steering 透過 Markdown 文件給予 Kiro 持久化的 workspace 知識，無需在每次對話中重複解釋規範，確保 Kiro 一致遵循既定模式、庫和標準。

### 文件範圍（3種）

| 範圍 | 位置 | 用途 |
|------|------|------|
| **Workspace** | `.kiro/steering/*.md` | 只適用於當前 workspace |
| **Global** | `~/.kiro/steering/*.md` | 適用於所有 workspace |
| **Team** | 透過 MDM/Group Policy 推送至 `~/.kiro/steering/` | 整個團隊共用標準 |

> 衝突時：Workspace Steering 優先於 Global Steering

### 三個內建基礎文件

| 文件 | 用途 |
|------|------|
| `product.md` | 產品目的、目標用戶、核心功能、業務目標 |
| `tech.md` | 技術棧、框架、開發工具、技術限制 |
| `structure.md` | 文件結構、命名規範、Import 模式、架構決策 |

生成方式：Kiro Panel → Steering → Generate Steering Docs

### Inclusion 模式（4種）

#### 1. Always（預設）
```yaml
---
inclusion: always
---
```
- 每次對話自動載入
- 適合：核心標準、技術棧、安全政策、編碼規範

#### 2. FileMatch（條件載入）
```yaml
---
inclusion: fileMatch
fileMatchPattern: "components/**/*.tsx"
---
```
多個 Pattern：
```yaml
---
inclusion: fileMatch
fileMatchPattern: ["**/*.ts", "**/*.tsx", "**/tsconfig.*.json"]
---
```
- 只有處理符合 Pattern 的文件時才載入
- 適合：組件規範、API 設計規則、測試方法、部署程序

#### 3. Manual（手動引用）
```yaml
---
inclusion: manual
---
```
- 在 Chat 中用 `#文件名` 手動引用
- 亦可用 `/` slash command 選擇
- 適合：偶爾用的指南、遷移程序、情境複雜的文件

#### 4. Auto（AI 自動判斷）
```yaml
---
inclusion: auto
name: api-design
description: REST API design patterns and conventions. Use when creating or modifying API endpoints.
---
```
- AI 根據 description 判斷請求是否相關時自動載入
- 亦支援 slash command 手動觸發
- 適合：複雜工作流、專業領域知識、詳細參考資料

### File References（引用 Workspace 文件）

```markdown
#[[file:<relative_file_name>]]
```

例子：
```markdown
#[[file:api/openapi.yaml]]
#[[file:components/ui/button.tsx]]
#[[file:.env.example]]
```

### 自動掃描機制

Kiro 啟動時**自動掃描**以下兩個固定位置，唔需要任何配置或目錄文件：

```
Global:     ~/.kiro/steering/*.md        ← 先讀
Workspace:  .kiro/steering/*.md          ← 後讀，有衝突時優先
```

同一目錄內按**文件名字母順序**載入，建議用數字前綴控制順序：
```
00-core-memory.md      ← 最先載入
01-session-context.md
02-project-structure.md
...
```

### AGENTS.md 支援

- 放喺 `~/.kiro/steering/` 或 workspace 根目錄
- 格式同 Steering 文件相同
- **唔支援** inclusion modes，永遠自動載入

### 常用 Steering 文件策略

| 文件名 | 內容 |
|--------|------|
| `api-standards.md` | REST 規範、錯誤格式、認證流程、版本策略 |
| `testing-standards.md` | 單元測試模式、Mock 方法、覆蓋率要求 |
| `code-conventions.md` | 命名規範、文件結構、Import 順序 |
| `security-policies.md` | 認證要求、數據驗證、輸入消毒標準 |
| `deployment-workflow.md` | 構建程序、環境配置、部署步驟 |

---

## 三、Hooks（事件驅動自動化）

### 簡介

Agent Hooks 係自動化觸發器，當 IDE 發生特定事件時自動執行預定義的 Agent 動作或 Shell 命令，消除重複性手動任務。

### 觸發事件類型（10種）

| 事件 | 觸發時機 | 常見用途 |
|------|---------|---------|
| `fileEdited` | 用戶儲存文件 | 自動 Lint、格式化、更新文件 |
| `fileCreated` | 用戶創建新文件 | 自動加入 boilerplate、更新 index |
| `fileDeleted` | 用戶刪除文件 | 清理相關引用、更新 import |
| `promptSubmit` | 發送訊息給 Agent | 前置檢查、注入額外 context |
| `agentStop` | Agent 執行完成 | 執行測試、生成報告 |
| `preToolUse` | 工具執行前 | 權限檢查、安全審計 |
| `postToolUse` | 工具執行後 | 驗證結果、記錄日誌 |
| `preTaskExecution` | Spec Task 設為 in_progress 前 | 前置條件檢查 |
| `postTaskExecution` | Spec Task 設為 completed 後 | 執行測試、更新文件 |
| `userTriggered` | 用戶手動點擊觸發 | 按需執行的自動化任務 |

### Hook 動作類型（2種）

| 動作 | 用途 | 配置欄位 |
|------|------|---------|
| `askAgent` | 發送 Prompt 給 AI Agent | `prompt` |
| `runCommand` | 執行 Shell 命令 | `command` |

### Hook 文件格式（JSON Schema）

```json
{
  "name": "string（必填）",
  "version": "string（必填）",
  "description": "string（選填）",
  "when": {
    "type": "事件類型（必填）",
    "patterns": ["文件 Pattern 陣列（file 事件必填）"],
    "toolTypes": ["工具類型（preToolUse/postToolUse 必填）"]
  },
  "then": {
    "type": "askAgent 或 runCommand",
    "prompt": "string（askAgent 必填）",
    "command": "string（runCommand 必填）"
  }
}
```

### toolTypes 有效值

| 類別 | 說明 |
|------|------|
| `read` | 讀取文件工具 |
| `write` | 寫入文件工具 |
| `shell` | Shell 命令工具 |
| `web` | 網頁相關工具 |
| `spec` | Spec 相關工具 |
| `*` | 所有工具 |
| regex pattern | 例如 `.*sql.*` 匹配 MCP 工具名稱 |

### Hook 文件位置

- `.kiro/hooks/*.json`（Workspace 級別）

### Hook 範例

#### 儲存 TypeScript 文件時自動 Lint
```json
{
  "name": "Lint on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.ts", "*.tsx"]
  },
  "then": {
    "type": "runCommand",
    "command": "npm run lint"
  }
}
```

#### 寫入操作前審查
```json
{
  "name": "Review Write Operations",
  "version": "1.0.0",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Verify this write operation follows our coding standards"
  }
}
```

#### Spec Task 完成後執行測試
```json
{
  "name": "Run Tests After Task",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "runCommand",
    "command": "npm run test"
  }
}
```

### Hook 實例：Steering 自動 Staging

當 Steering 文件被修改後，自動 `git add` 到 staging area，等用戶自行決定是否 commit：

```json
{
  "name": "Auto Stage Steering Changes",
  "version": "1.0.0",
  "description": "當 Steering 文件被修改後，自動 git add，等用戶自行 commit",
  "when": {
    "type": "fileEdited",
    "patterns": [".kiro/steering/*.md"]
  },
  "then": {
    "type": "runCommand",
    "command": "git add .kiro/steering/"
  }
}
```

效果：
```
Kiro 修改 Steering → Hook 自動 git add → 用戶決定 commit 或 restore
```

### preToolUse 重要規則

- 若 Hook 輸出顯示**拒絕存取**，必須**禁止**重試該工具調用
- 若 Hook 輸出**無拒絕跡象**，必須用**完全相同的參數**重新調用工具
- 注意**循環依賴**：Hook A 需要調用 Tool X → Tool X 觸發 Hook A → 無限循環

---

## 四、MCP Servers（外部工具連接）

### 簡介

Model Context Protocol (MCP) 透過連接專門的外部 Server，擴展 Kiro 的能力，提供額外的工具和 Context。

### 配置文件位置

| 位置 | 範圍 |
|------|------|
| `.kiro/settings/mcp.json` | Workspace 級別 |
| `~/.kiro/settings/mcp.json` | 全局（User 級別） |

> 優先級：Workspace > User（後者覆蓋前者）

### 配置格式

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx 或 npx 或 python",
      "args": ["server-package@latest"],
      "env": {
        "API_KEY": "your-key"
      },
      "disabled": false,
      "autoApprove": ["tool-name"]
    }
  }
}
```

### 常用 MCP Server 範例

#### Fetch（抓取網頁內容）
```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "disabled": false
    }
  }
}
```

#### Playwright（瀏覽器自動化）
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "disabled": false
    }
  }
}
```

### 支援功能

- 外部 API 同服務整合
- 專業知識庫連接
- 自定義工具開發
- `#` mention 引用 Server 提供的 Prompt Templates
- Server Elicitation（工具執行中請求額外輸入）

### 前置條件

- `uvx` 命令：需安裝 [uv](https://docs.astral.sh/uv/getting-started/installation/)
- `npx` 命令：需安裝 [Node.js](https://nodejs.org)

---

## 五、Agent Skills（可重用 AI 技能包）

### 簡介

Skills 係包含指令、腳本和資源的 Folder，Kiro 動態載入以提升特定任務的表現。

### 文件位置

| 位置 | 範圍 |
|------|------|
| `.kiro/skills/` | Workspace 級別 |
| `~/.kiro/skills/` | 全局（所有 Workspace） |

### Skill 結構

每個 Skill 係一個有 `SKILL.md` 的 Folder：

```
skill-name/
└── SKILL.md    ← 包含 YAML frontmatter + 指令內容
```

### SKILL.md 格式

```markdown
---
name: my-skill-name
description: 清晰描述這個 Skill 做咩同何時使用
---

# My Skill Name

[指令內容]

## Examples
- 使用例子 1
- 使用例子 2

## Guidelines
- 指引 1
- 指引 2
```

### Anthropic 官方 Skills（17個）

**Creative & Design**
| Skill | 用途 |
|-------|------|
| `algorithmic-art` | 用 p5.js 生成算法藝術（seeded randomness） |
| `brand-guidelines` | Anthropic 品牌色彩同排版規範 |
| `canvas-design` | 生成 .png / .pdf 視覺設計 |
| `frontend-design` | 高質量前端界面設計 |
| `slack-gif-creator` | 製作 Slack 用的動態 GIF |
| `theme-factory` | 為 artifacts 套用主題樣式（10種預設主題） |

**Development & Technical**
| Skill | 用途 |
|-------|------|
| `claude-api` | Claude API / Anthropic SDK 開發輔助 |
| `mcp-builder` | 建立高質量 MCP Server |
| `web-artifacts-builder` | 複雜多組件 HTML artifacts（React/Tailwind/shadcn） |
| `webapp-testing` | 用 Playwright 測試 Web App |

**Enterprise & Communication**
| Skill | 用途 |
|-------|------|
| `doc-coauthoring` | 協作撰寫文件（規格、提案、技術文件） |
| `internal-comms` | 內部溝通文件（狀態報告、通訊、FAQ） |
| `skill-creator` | 創建同優化新 Skill |

**Document Skills**
| Skill | 用途 |
|-------|------|
| `docx` | Word 文件處理 |
| `pdf` | PDF 處理（提取、合併、分割、OCR） |
| `pptx` | PowerPoint 處理 |
| `xlsx` | Excel 試算表處理 |

---

## 六、架構層次總覽

```
┌─────────────────────────────────────────┐
│              你的指令 / 對話              │  ← 用戶
├─────────────────────────────────────────┤
│         Agent Skills（技能層）            │  ← ~/.kiro/skills/
├─────────────────────────────────────────┤
│         Steering（知識層）               │  ← .kiro/steering/
├─────────────────────────────────────────┤
│    Specs（規劃層）  │  Hooks（自動化層）   │  ← .kiro/specs/ / .kiro/hooks/
├─────────────────────────────────────────┤
│         Kiro Agent（執行層）              │  ← Harness 核心
├─────────────────────────────────────────┤
│    MCP Servers（工具層）                  │  ← .kiro/settings/mcp.json
└─────────────────────────────────────────┘
```

---

## 七、Session 類型

| 類型 | 說明 |
|------|------|
| **Vibe** | 對話式問答同探索性編碼 |
| **Spec** | 結構化 Requirements → Design → Tasks 工作流 |

---

## 八、Autonomy 模式

| 模式 | 說明 |
|------|------|
| **Autopilot**（預設） | Kiro 自主完成任務，用戶可隨時查看、回滾或中斷 |
| **Supervised** | 每個 Turn 後暫停等待審批，以 Hunk 為單位接受/拒絕文件修改 |

---

## 九、記憶系統（4層架構）

```
┌─────────────────────────────────────────────────┐
│  第四層：Bedrock AgentCore Memory（跨session長期）│ ← 需額外設定 AWS MCP
├─────────────────────────────────────────────────┤
│  第一層：Steering Files（永久規範記憶）            │ ← 最重要，本地 .md 文件
│  ~/.kiro/steering/ + .kiro/steering/             │
├─────────────────────────────────────────────────┤
│  第二層：Codebase Index（代碼語義記憶）            │ ← 自動建立
├─────────────────────────────────────────────────┤
│  第三層：Session History（對話短期記憶）           │ ← IDE History 按鈕
└─────────────────────────────────────────────────┘
```

| 層次 | 機制 | 持久性 | 設定難度 |
|------|------|--------|---------|
| Steering Files | `.kiro/steering/*.md` | 永久 | 低 |
| Codebase Index | 自動掃描 | 重啟後重建 | 零 |
| Session History | IDE Chat History | 關閉後仍在 | 零 |
| AgentCore Memory | AWS Bedrock MCP | 跨 session | 高 |

### Session 管理（IDE）

| 操作 | 方法 |
|------|------|
| 睇歷史 session | Chat Panel → **History** 按鈕 |
| 還原舊 session | History → 選擇 session → 還原 |
| 匯出對話 | 右鍵 Chat Tab → **Export Conversation**（.md 格式） |
| 開新 session | Chat Panel → **`+`** 按鈕 |

### Steering + Git 版本控制（推薦）

```powershell
# 初始化
git init
git add .kiro\steering\
git commit -m "chore: initial steering setup"

# 每次更新後
git add .kiro\steering\
git commit -m "steering: update session context"
git push

# Restore 某個版本
git checkout <commit-hash> -- .kiro\steering\01-session-context.md
```

---

## 參考資源

| 資源 | 連結 |
|------|------|
| 官方文檔首頁 | https://kiro.dev/docs |
| Specs 文檔 | https://kiro.dev/docs/specs |
| Steering 文檔 | https://kiro.dev/docs/steering |
| Hooks 文檔 | https://kiro.dev/docs/hooks |
| MCP 文檔 | https://kiro.dev/docs/mcp |
| 第一個項目教程 | https://kiro.dev/docs/getting-started/first-project |
| AgentSkills 標準 | https://agentskills.io |
| Harness + Kiro 整合 | https://www.harness.io/blog/amazon-kiro-and-harness |
