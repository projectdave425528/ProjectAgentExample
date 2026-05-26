# ProjectAgentExample

> Multi-Agent 漸進式披露設計範例
> 用 L1 Index（always）+ L2/L3 Detail（manual/read_file）減少 Token 消耗

---

## 架構

```
ProjectAgentExample/
├── main-agent/              ← Orchestrator（L1 < 50 行）
├── planner/                 ← 需求分析 + 架構設計
├── generator/               ← 代碼生成
├── evaluator/               ← 代碼審查
├── ProjectRecord/           ← 所有 Project 記錄 + 產出
│   ├── active-project.md    ← 當前 active project（切換用）
│   ├── templates/           ← 共用 Message 模板
│   └── {project-name}/     ← 每個 Project 獨立空間
│       ├── SearchIndex.md
│       ├── conversation-log.md
│       ├── control/
│       ├── output/
│       ├── planner/inbox+outbox
│       ├── generator/inbox+outbox
│       └── evaluator/inbox+outbox
├── UserConfig/sessions/     ← Session log（用戶對話記錄）
└── UserDocument/            ← 設計文件
```

## 漸進式披露設計

| Layer | 文件 | 載入時機 | 大小 |
|-------|------|---------|------|
| L1 | `00-index.md` | 每次對話自動載入 | < 50 行 |
| L2 | `01-comm-system.md` | 需要調用 Agent 時 | < 100 行 |
| L3 | `details/*.md` | 執行具體任務時 | 無限制 |

## Token 節省

每次對話只載入 ~50 行（L1 Index），需要時先讀 L2/L3。
比傳統方式（全部 always）節省約 70% Token。

## 多 Project 支援

- 每個 Project 有獨立嘅 inbox/outbox、SearchIndex、output
- 切換 Project：改 `ProjectRecord/active-project.md` 嘅 `current:` 值
- 新增 Project：喺 `ProjectRecord/` 下建新目錄，複製結構即可

## 使用方式

1. 開 Kiro → Open Folder → `main-agent/`
2. 同 Main Agent 講需求
3. Main Agent 讀取 `active-project.md` → 自動調度 Planner → Generator → Evaluator
4. 所有記錄寫入 `ProjectRecord/{active-project}/`
