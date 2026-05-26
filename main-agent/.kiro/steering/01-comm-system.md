---
inclusion: manual
---

# Agent 通訊系統
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## CLI 調用格式

```powershell
# 如果 kiro-cli 已加入 PATH：
kiro-cli chat --agent [agent-name] "[prompt]"

# 如果未加入 PATH，用完整路徑（按你嘅安裝位置）：
# Windows 預設：& "$env:LOCALAPPDATA\Kiro-Cli\kiro-cli.exe" chat --agent [agent-name] "[prompt]"
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
shared/
├── conversation-log.md          ← 所有對話記錄（append-only）
├── control/                     ← 控制指令
└── templates/                   ← Message 模板

[agent]/
├── inbox/                       ← 接收任務
└── outbox/                      ← 回覆結果
```

### 記錄時機
- **調用前**：寫任務到目標 Agent 嘅 `inbox/task-{id}.md`
- **收到回覆**：從目標 Agent 嘅 `outbox/task-{id}-reply.md` 讀取
- **每次交互**：append 到 `shared/conversation-log.md`

## Message 格式

### Task Message（寫入 inbox）
```markdown
# Task {id}

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
# Reply: Task {id}

- **From**: {agent-name}
- **To**: main-agent
- **Timestamp**: {ISO timestamp}
- **Status**: completed | blocked | failed

## 結果
{Agent 嘅回覆內容}

## 備註
{任何額外資訊}
```

### Conversation Log Entry
```markdown
---
## [{timestamp}] {from} → {to}

**Type**: {message-type}
**Status**: {status}
**Summary**: {一句話摘要}
```
