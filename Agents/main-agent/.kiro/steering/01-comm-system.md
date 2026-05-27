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
ProjectRecord/
├── active-project.md            ← 當前 active project（切換用）
├── templates/                   ← 共用 Message 模板
│
└── {active-project}/            ← 當前 Project 嘅所有記錄
    ├── specs/                   ← Spec 文件（requirements/design/tasks）
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
- **開始前**：讀取 `ProjectRecord/active-project.md` 確認當前 Project
- **調用前**：寫任務到 `ProjectRecord/{active-project}/inbox/{agent}/assignment-{id}.md`
- **收到回覆**：從 `ProjectRecord/{active-project}/outbox/{agent}/assignment-{id}-reply-{status}.md` 讀取
- **每次交互**：append 到 `ProjectRecord/{active-project}/conversation-log.md`
- **每次寫入**：append 到 `ProjectRecord/{active-project}/SearchIndex.md`

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
