# ProjectAgentExample

> Multi-Agent 漸進式披露設計範例
> 用 L1 Index（always）+ L2/L3 Detail（manual/read_file）減少 Token 消耗

---

## 架構

```
ProjectAgentExample/
├── main-agent/          ← Orchestrator（L1 < 50 行）
├── planner/             ← 需求分析 + 架構設計
├── generator/           ← 代碼生成
├── evaluator/           ← 代碼審查
├── output/              ← 生成嘅代碼
└── shared/              ← 通訊記錄 + 模板
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

## 使用方式

1. 開 Kiro → Open Folder → `main-agent/`
2. 同 Main Agent 講需求
3. Main Agent 自動調度 Planner → Generator → Evaluator
