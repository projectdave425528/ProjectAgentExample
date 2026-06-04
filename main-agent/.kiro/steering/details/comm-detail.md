---
inclusion: manual
description: Main Agent 通訊細則（L3 - 手動載入）— 完整目錄結構 + Message 格式
---

# Main Agent 通訊細則

> 本文件係 L3（manual）。由 `01-comm-system.md`（L2）瘦身搬出。
> Message 格式以 `./ProjectRecord/templates/` 嘅 template 為準，本文件只係快速參考。

## 完整目錄結構
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
    ├── checkpoints/             ← Checkpoint 文件（每個 Agent 獨立子目錄）
    │   ├── main-agent/
    │   ├── planner/
    │   ├── generator/
    │   └── evaluator/
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

## Message 格式（快速參考）
> 完整定義同範例見 `./ProjectRecord/templates/assignment-template.md`、`assignment-reply-template.md`、`conversation-log-entry-template.md`。

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
