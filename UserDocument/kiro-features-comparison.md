# Kiro 核心功能比較

> 呢份文件解釋 Kiro 嘅各種擴展機制：Skill、Steering、Hook、Spec、MCP，以及佢哋嘅分別同使用場景。

---

## 總覽

| 功能 | 一句話定義 | 觸發方式 | 影響範圍 |
|------|-----------|---------|---------|
| **Skill** | 預建嘅專業能力包（知識 + 工具指引） | Agent 自動偵測 / 用戶手動啟動 | 單次對話 |
| **Steering** | 持久性規則同指引 | 每次對話自動載入 / 手動讀取 | 所有對話 |
| **Hook** | 事件驅動嘅自動化動作 | IDE 事件觸發（file edit/create/delete/agent stop 等） | 跨對話 |
| **Spec** | 結構化嘅需求→設計→任務工作流 | 用戶啟動 Spec session | 單個 feature |
| **MCP** | 外部工具/服務嘅連接協議 | Agent 調用 MCP tool | 跨對話 |

---

## 1. Skill（技能）

### 係咩
預先打包嘅「專業知識 + 最佳實踐 + 工具使用指引」。好似請咗一個特定領域嘅專家幫手。

### 特點
- 按需載入（唔會一直佔 context）
- 由 keywords 觸發（Agent 偵測到相關詞就自動啟動）
- 包含 SKILL.md（知識文檔）+ 可選嘅 steering files
- 冇自己嘅工具 — 用 Kiro 現有工具

### 例子
- `frontend-design` — 建 UI 時啟動，提供設計原則同 component 建議
- `claude-api` — 用 Anthropic SDK 時啟動，提供 prompt caching 同最佳實踐
- `pdf` — 處理 PDF 文件時啟動

### 適用場景
- 需要特定領域知識
- 需要遵守特定風格/標準
- 一次性任務，唔需要持久規則

---

## 2. Steering（指引/規則）

### 係咩
持久性嘅行為規則，寫喺 `.kiro/steering/` 入面。每次對話都會載入（always）或按需讀取（manual）。

### 特點
- 文件形式（`.md`）
- 分層載入：`always`（自動載入）/ `manual`（按需讀取）/ `fileMatch`（特定文件觸發）
- 可以 reference 其他文件（`#[[file:path]]`）
- Workspace level + Agent level 可以疊加

### 例子
- `role.md` — Agent 身份同核心規則
- `project-protocols-comm.md` — Agent 通訊格式
- `domain-knowledge-code-standards.md` — 代碼規範

### 適用場景
- 團隊標準（coding style、commit message format）
- Agent 行為限制（唔好做咩、必須做咩）
- Project 特定嘅路徑/結構/規則

### 同 Skill 嘅分別
| | Skill | Steering |
|---|-------|---------|
| 持久性 | 單次對話 | 跨所有對話 |
| 載入方式 | 按需（keyword 觸發） | always 或 manual |
| 內容類型 | 專業知識 + 最佳實踐 | 規則 + 約束 + 流程 |
| 誰寫 | Kiro 官方 / 社區 | 用戶自己 |

---

## 3. Hook（鉤子/自動化）

### 係咩
事件驅動嘅自動化。當 IDE 發生特定事件時，自動執行指定動作。

### 特點
- JSON 格式（`.kiro.hook`）
- 事件觸發（唔係人手觸發）
- 兩種動作：`askAgent`（提醒 agent）/ `runCommand`（跑 shell）
- 可以過濾文件 pattern / tool type

### 事件類型
| 事件 | 觸發時機 |
|------|---------|
| `fileEdited` | 用戶保存文件 |
| `fileCreated` | 新建文件 |
| `fileDeleted` | 刪除文件 |
| `agentStop` | Agent 完成執行 |
| `promptSubmit` | 用戶發送 message |
| `preToolUse` | Agent 即將調用工具 |
| `postToolUse` | Agent 完成工具調用 |
| `preTaskExecution` | Spec task 開始前 |
| `postTaskExecution` | Spec task 完成後 |
| `userTriggered` | 用戶手動按按鈕 |

### 例子
- 文件保存後自動 lint
- Agent 完成後自動記錄 session log
- Sub Agent 寫 outbox 後自動通知 Main Agent
- 調用 write 工具前自動 review

### 適用場景
- CI/CD 式嘅自動化
- 監聽文件變化做 reactive 操作
- 攔截 agent 操作做 access control

### 同 Steering 嘅分別
| | Steering | Hook |
|---|---------|------|
| 觸發方式 | 被動（agent 讀取） | 主動（事件驅動） |
| 動作 | 影響 agent 行為 | 執行具體操作 |
| 時機 | 對話開始時 | 任何時候（事件發生時） |

---

## 4. Spec（規格/規範）

### 係咩
結構化嘅 feature 開發工作流。將用戶需求拆解成 Requirements → Design → Tasks，然後逐步實作。

### 特點
- 三階段：Requirements → Design → Tasks
- 每個 Task 有明確嘅 acceptance criteria
- Tasks 之間有依賴關係（DAG）
- Agent 按 Task 順序執行，可 parallel
- 有 approval gates（Supervised mode）

### 文件結構
```
.kiro/specs/{feature}/
├── requirements.md
├── design.md
└── tasks.md
```

### 適用場景
- 複雜 feature 開發（多文件、多步驟）
- 需要用戶 review 每個階段
- 需要明確嘅 acceptance criteria
- 團隊協作（多人 review spec）

### 同 Steering 嘅分別
| | Steering | Spec |
|---|---------|------|
| 用途 | 定義「點做」嘅規則 | 定義「做咩」嘅計劃 |
| 持久性 | 跨所有對話 | 單個 feature |
| 內容 | 通用規則 | 具體需求 + 設計 + 任務 |

---

## 5. MCP（Model Context Protocol）

### 係咩
外部工具同服務嘅標準連接協議。等 Agent 可以用第三方 API/工具。

### 特點
- JSON 配置（`mcp.json`）
- Server-based（每個 MCP server 提供多個 tools）
- 支持 auto-approve（免確認調用）
- User level + Workspace level 配置

### 配置位置
- User level：`~/.kiro/settings/mcp.json`
- Workspace level：`.kiro/settings/mcp.json`

### 例子
- AWS Documentation MCP — 查 AWS 文檔
- Database MCP — 直接 query database
- Playwright MCP — 控制瀏覽器做 UI 測試

### 適用場景
- 需要存取外部系統（DB、API、文件系統）
- 需要特定工具能力（瀏覽器控制、圖片處理）
- 整合第三方服務

### 同 Skill 嘅分別
| | Skill | MCP |
|---|-------|-----|
| 提供咩 | 知識 + 指引 | 實際工具能力 |
| 依賴 | 冇（純文字） | 需要 server 運行 |
| 安裝 | 內建 / 一鍵啟動 | 需要配置 + 可能要裝 runtime |

---

## 使用場景決策表

| 我想... | 用咩 |
|---------|------|
| 加一條永久規則（例如「回覆用廣東話」） | **Steering** |
| 保存後自動跑 lint | **Hook** |
| 做一個完整嘅 feature（多步驟） | **Spec** |
| 用第三方 API/工具 | **MCP** |
| 臨時需要專業知識（例如建 PDF） | **Skill** |
| 監聽文件變化做 reactive 操作 | **Hook** |
| 定義 agent 嘅身份同限制 | **Steering** |
| 攔截 agent 操作做 review | **Hook**（preToolUse） |
| 建立 requirements → design → tasks 工作流 | **Spec** |
| 連接數據庫 / 瀏覽器 / 外部服務 | **MCP** |

---

## 組合使用

呢啲功能唔係互斥，通常組合使用：

```
Steering（規則） → 定義 Agent 行為
    + Hook（自動化） → 監聽事件觸發動作
    + Spec（計劃） → 結構化 feature 開發
    + MCP（工具） → 連接外部服務
    + Skill（知識） → 按需載入專業能力
```

例如你嘅 ProjectAgentExample：
- **Steering** 定義每個 Agent 嘅角色同規則
- **Hook** 自動記錄 session log + 監聽 outbox 回覆
- **Spec** 可以俾 Planner 產出 requirements/design/tasks
- **MCP** 可以加 Playwright 做 UI 測試
