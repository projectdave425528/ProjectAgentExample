---
inclusion: always
---

# Agent 通訊系統
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## Sub Agent 調用規則（優先順序）

### 方法 1：Kiro CLI（優先使用）
```powershell
# 如果 kiro-cli 已加入 PATH：
kiro-cli chat --agent [agent-name] "[prompt]"

# 如果未加入 PATH，用完整路徑（按你嘅安裝位置）：
# Windows 預設：& "$env:LOCALAPPDATA\Kiro-Cli\kiro-cli.exe" chat --agent [agent-name] "[prompt]"
```

**調用前必做：**
1. 寫 Assignment 到 inbox
2. 將相關 Sub Agent 嘅 steering 文件路徑傳入（透過 prompt 或 --context）
3. 確認 kiro-cli 可用（先跑 `kiro-cli --version`）

**如果 kiro-cli 失敗（command not found / error）→ 自動切換方法 2**

### 方法 2：invoke_sub_agent（Fallback）

**必須載入嘅 contextFiles（自動載入，唔使每次手動指定）：**

| Agent | contextFiles |
|-------|-------------|
| **所有 Agent 共用** | `./ProjectRecord/active-project.md` |
| | `./ProjectRecord/{active-project}/memory/{agent}-memory.md` |
| | `./ProjectRecord/templates/assignment-reply-template.md` |
| | `./ProjectRecord/{active-project}/specs/tasks.md`（如存在） |
| **Planner** | `./Agents/planner/.kiro/steering/00-index.md` |
| | `./Agents/planner/.kiro/steering/01-comm-system.md` |
| **Generator** | `./Agents/generator/.kiro/steering/00-index.md` |
| | `./Agents/generator/.kiro/steering/01-comm-system.md` |
| **Evaluator** | `./Agents/evaluator/.kiro/steering/00-index.md` |
| | `./Agents/evaluator/.kiro/steering/01-comm-system.md` |

**調用格式：**
```
invoke_sub_agent:
  name: "general-task-execution"
  prompt: "[assignment 內容]"
  contextFiles:
    - path: "./Agents/{agent}/.kiro/steering/00-index.md"
    - path: "./Agents/{agent}/.kiro/steering/01-comm-system.md"
    - path: "./ProjectRecord/active-project.md"
    - path: "./ProjectRecord/{active-project}/specs/tasks.md"
    - path: "./ProjectRecord/{active-project}/memory/{agent}-memory.md"
    - path: "./ProjectRecord/templates/assignment-reply-template.md"
```

**調用前必做：**
1. 寫 Assignment 到 inbox（同方法 1 一樣）
2. 確認 `{agent}` 同 `{active-project}` 已替換為實際值
3. Prompt 入面明確指示 Agent 角色 + 任務 + 輸出路徑
4. 如果 specs/ 入面嘅文件唔存在 → 移除該 contextFile（唔好報錯）

### 調用決策流程
```
嘗試 kiro-cli --version
    ↓
成功 → 用方法 1（Kiro CLI）
失敗 → 用方法 2（invoke_sub_agent + contextFiles）
```

## Agent 路徑表

| Agent | Name | 用途 |
|-------|------|------|
| Planner | `planner` | 分析需求、拆解任務、產出計劃 |
| Generator | `generator` | 根據計劃生成代碼 |
| Evaluator | `evaluator` | 驗證代碼質量、回報 PASS/FAIL/REPLAN |

## 文件記錄規則

### 目錄結構
```
./ProjectRecord/
├── active-project.md            ← 當前 active project（切換用）
├── templates/                   ← 共用 Message 模板
│
└── {active-project}/            ← 當前 Project 嘅所有記錄
    ├── specs/                   ← Spec 文件（requirements/design/tasks）
    ├── memory/                  ← Agent 記憶（每個 Agent 獨立文件）
    │   ├── main-agent-memory.md
    │   ├── planner-memory.md
    │   ├── generator-memory.md
    │   └── evaluator-memory.md
    ├── SearchIndex.md           ← 本 Project 嘅搜尋索引
    ├── conversation-log.md      ← 所有對話記錄（append-only）
    ├── control/                 ← 控制指令
    ├── output/                  ← 生成嘅代碼
    ├── inbox/                   ← 所有 Agent 嘅收件
    │   ├── planner/
    │   ├── generator/
    │   ├── evaluator/
    │   └── main-agent/
    └── outbox/                  ← 所有 Agent 嘅發件
        ├── planner/
        ├── generator/
        ├── evaluator/
        └── main-agent/
```

### 記錄時機
- **開始前**：讀取 `./ProjectRecord/active-project.md` 確認當前 Project
- **調用前**：寫任務到 `./ProjectRecord/{active-project}/inbox/{agent}/assignment-{id}.md`
- **收到回覆**：從 `./ProjectRecord/{active-project}/outbox/{agent}/assignment-{id}-reply-{status}.md` 讀取
- **每次交互**：append 到 `./ProjectRecord/{active-project}/conversation-log.md`
- **每次寫入**：append 到 `./ProjectRecord/{active-project}/SearchIndex.md`

## Assignment ID 生成規則

### ID 格式
- 三位數字，零填充：`001`、`002`、`003`...
- 全局遞增（同一個 Project 入面唔會重複）

### 生成方法
1. 讀取 `./ProjectRecord/{active-project}/SearchIndex.md`
2. 搵最後一行嘅 Assignment ID（第一欄）
3. +1 = 新 ID
4. 如果 SearchIndex 為空或唔存在 → 從 `001` 開始

### 例子
```
SearchIndex 最後一行：| 003 | evaluator | verdict | ...
新 Assignment ID = 004
```

## Message 格式

### Assignment Message（寫入 inbox）
```markdown
# Assignment {id}

- **From**: main-agent
- **To**: {agent-name}
- **Timestamp**: {ISO timestamp}
- **Type**: plan-request | generate-request | evaluate-request

## 需求
{具體內容}

## Context
{相關背景資訊}

## 預期輸出
{期望 Agent 回覆咩}
```

### Reply Message（從 outbox 讀取）
```markdown
# Assignment Reply: {id}

- **From**: {agent-name}
- **To**: main-agent
- **Timestamp**: {ISO timestamp}
- **AssignmentStatus**: completed | blocked | verdict-pass | verdict-fail | verdict-replan | escalation
- **TaskRef**: Task {task-number}: {task-title}
- **TaskID**: {active-project}/Task-{task-number}
- **TaskStatus**: in_progress → completed | blocked

## 驗證標準
- [x] {已完成嘅 outcome}
- [ ] {未完成嘅 outcome}

## 結果
{Agent 嘅回覆內容}

## 備註
{任何額外資訊}

## Memory 已更新
✅ / ❌

## Usage 估算
- **Context 使用率**: {百分比}%
- **估算 Token 數**: {input_tokens} input / {output_tokens} output
- **接近限額警告**: ⚠️ / ✅
```

### Conversation Log Entry
```markdown
---
## [{timestamp}] {from} → {to}

**Type**: {message-type}
**Status**: {status}
**Summary**: {一句話摘要}
```
