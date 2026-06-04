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
  prompt: "[assignment 內容 + 明確指示 Agent 角色/任務/輸出路徑]"
  contextFiles: [見上表，按 {agent} 揀對應幾個]
```

**調用前必做：**
1. 寫 Assignment 到 inbox（同方法 1 一樣）
2. 確認 `{agent}` 同 `{active-project}` 已替換為實際值
3. 如果 specs/ 入面嘅文件唔存在 → 移除該 contextFile（唔好報錯）

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

> 完整目錄結構見 `details/comm-detail.md`。常用路徑：
> - `./ProjectRecord/active-project.md` — 當前 Project
> - `./ProjectRecord/{active-project}/inbox/{agent}/` — 收件
> - `./ProjectRecord/{active-project}/outbox/{agent}/` — 發件
> - `./ProjectRecord/{active-project}/{specs,memory,checkpoints,output,control}/`
> - `./ProjectRecord/{active-project}/{SearchIndex.md,conversation-log.md}`

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
> 完整 Message 格式（Assignment / Reply / Conversation Log）見 `./ProjectRecord/templates/` 嘅對應 template，
> 快速參考見 `details/comm-detail.md`。寫入前先讀 template 按格式填寫。
