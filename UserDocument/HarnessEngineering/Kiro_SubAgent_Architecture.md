# Kiro Sub Agent 架構：Planner-Generator-Evaluator

> 用 Multi-Root Workspace 實現獨立記憶、獨立 Spec 的三角循環
> 更新日期：2026-05-22

---

## 設計目標

```
✅ 每個 Agent 有獨立 Steering（記憶）
✅ 每個 Agent 有獨立 Specs（任務）
✅ 每個 Agent 有獨立 Hooks（自動化）
✅ Agent 之間可以透過共享文件交流
✅ 支援循環反饋（Evaluator → Generator → Evaluator）
```

---

## 目錄結構

```
C:\Users\proje\AgentWorkspace\
│
├── AgentWorkspace.code-workspace    ← Multi-Root 配置文件
│
├── planner\                         ← Root 1：Planner Agent
│   ├── .kiro\
│   │   ├── steering\
│   │   │   ├── 00-role.md           ← 「我係 Planner」
│   │   │   ├── 01-rules.md          ← 規劃規則
│   │   │   └── 02-output-format.md  ← 輸出格式要求
│   │   ├── hooks\
│   │   │   └── on-plan-complete.kiro.hook  ← 規劃完成後通知
│   │   └── specs\
│   │       └── current-task\
│   │           ├── requirements.md   ← 用戶原始需求
│   │           ├── design.md         ← 技術方案
│   │           └── tasks.md          ← 拆分的任務清單
│   └── output\
│       └── plan.json                 ← 輸出：結構化計劃
│
├── generator\                       ← Root 2：Generator Agent
│   ├── .kiro\
│   │   ├── steering\
│   │   │   ├── 00-role.md           ← 「我係 Generator」
│   │   │   ├── 01-rules.md          ← 代碼規範
│   │   │   └── 02-tech-stack.md     ← 技術棧限制
│   │   ├── hooks\
│   │   │   ├── on-code-complete.kiro.hook  ← 代碼完成後通知
│   │   │   └── lint-on-save.kiro.hook      ← 儲存時自動 lint
│   │   └── specs\
│   │       └── current-task\
│   │           └── tasks.md          ← 從 Planner 接收的任務
│   └── output\
│       └── src\                      ← 輸出：生成的代碼
│
├── evaluator\                       ← Root 3：Evaluator Agent
│   ├── .kiro\
│   │   ├── steering\
│   │   │   ├── 00-role.md           ← 「我係 Evaluator」
│   │   │   ├── 01-checklist.md      ← 評估清單
│   │   │   └── 02-standards.md      ← 品質標準
│   │   ├── hooks\
│   │   │   └── on-eval-complete.kiro.hook  ← 評估完成後通知
│   │   └── specs\
│   │       └── current-review\
│   │           └── tasks.md          ← 評估任務
│   └── output\
│       └── review.json               ← 輸出：評估結果（PASS/FAIL）
│
└── shared\                          ← 共享目錄（所有 Agent 可讀寫）
    ├── requirements\
    │   └── user-request.md           ← 用戶原始需求
    ├── handoff\
    │   ├── plan-to-generator.json    ← Planner → Generator 的交接
    │   ├── generator-to-evaluator.json ← Generator → Evaluator 的交接
    │   └── evaluator-feedback.json   ← Evaluator → Generator/Planner 的反饋
    └── final\
        └── deliverable\              ← 最終交付物
```

---

## .code-workspace 配置文件

```json
{
  "folders": [
    { "path": "planner", "name": "🧠 Planner" },
    { "path": "generator", "name": "⚡ Generator" },
    { "path": "evaluator", "name": "🔍 Evaluator" },
    { "path": "shared", "name": "📁 Shared" }
  ],
  "settings": {}
}
```

---

## 各 Agent 的 Steering 內容

### Planner — `planner/.kiro/steering/00-role.md`

```markdown
---
inclusion: always
---

# Planner Agent

## 角色
你係 Planner，負責分析需求同設計技術方案。

## 職責
1. 讀取 `shared/requirements/user-request.md` 了解用戶需求
2. 分析現有 codebase 結構
3. 設計技術方案（架構、數據流、API）
4. 拆分成可獨立執行的任務
5. 輸出結構化計劃到 `shared/handoff/plan-to-generator.json`

## 限制
- 唔可以寫代碼
- 唔可以修改 shared/final/ 目錄
- 只能輸出計劃文件

## 輸出格式
{
  "plan_id": "uuid",
  "summary": "技術方案摘要",
  "tasks": [
    {"id": 1, "description": "...", "dependencies": [], "estimated_complexity": "low/medium/high"}
  ],
  "risks": ["..."],
  "tech_decisions": [{"decision": "...", "rationale": "..."}]
}
```

### Generator — `generator/.kiro/steering/00-role.md`

```markdown
---
inclusion: always
---

# Generator Agent

## 角色
你係 Generator，負責根據 Planner 的計劃生成代碼。

## 職責
1. 讀取 `shared/handoff/plan-to-generator.json` 了解任務
2. 按任務清單逐步實現代碼
3. 確保代碼可編譯、可運行
4. 完成後輸出到 `shared/handoff/generator-to-evaluator.json`

## 限制
- 嚴格按照 Planner 的方案執行
- 唔可以修改 shared/requirements/
- 遇到方案不可行時，寫入 evaluator-feedback.json 請求 REPLAN

## 代碼規範
- 所有代碼寫入 generator/output/src/
- 必須包含基本錯誤處理
- 必須有 type hints（Python）或 TypeScript
```

### Evaluator — `evaluator/.kiro/steering/00-role.md`

```markdown
---
inclusion: always
---

# Evaluator Agent

## 角色
你係 Evaluator，負責檢查 Generator 的輸出質量。

## 職責
1. 讀取 `shared/handoff/generator-to-evaluator.json` 了解要評估咩
2. 讀取 Generator 的代碼（generator/output/src/）
3. 按 Checklist 逐項檢查
4. 輸出評估結果到 `shared/handoff/evaluator-feedback.json`

## Checklist
- [ ] 代碼是否可編譯/運行
- [ ] 是否符合 Planner 的技術方案
- [ ] 有冇明顯 bug 或安全問題
- [ ] 代碼風格是否一致
- [ ] 有冇缺少錯誤處理
- [ ] 命名是否清晰

## 輸出格式
{
  "verdict": "PASS | FAIL | REPLAN",
  "score": 0-100,
  "issues": [
    {"severity": "critical|warning|info", "file": "...", "line": N, "description": "..."}
  ],
  "feedback_to": "generator | planner",
  "message": "具體反饋內容"
}
```

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                     用戶輸入需求                              │
│              寫入 shared/requirements/user-request.md         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 1: 切換到 Planner root                                  │
│                                                             │
│ Kiro 讀取 planner/.kiro/steering/ → 知道自己係 Planner       │
│ 讀取 shared/requirements/ → 了解需求                         │
│ 輸出 shared/handoff/plan-to-generator.json                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: 切換到 Generator root                                │
│                                                             │
│ Kiro 讀取 generator/.kiro/steering/ → 知道自己係 Generator   │
│ 讀取 shared/handoff/plan-to-generator.json → 了解任務        │
│ 生成代碼到 generator/output/src/                             │
│ 輸出 shared/handoff/generator-to-evaluator.json              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 切換到 Evaluator root                                │
│                                                             │
│ Kiro 讀取 evaluator/.kiro/steering/ → 知道自己係 Evaluator   │
│ 讀取 shared/handoff/generator-to-evaluator.json              │
│ 檢查 generator/output/src/ 的代碼                            │
│ 輸出 shared/handoff/evaluator-feedback.json                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: 判斷結果                                             │
│                                                             │
│ ✅ PASS → 複製到 shared/final/deliverable/ → 完成            │
│ ❌ FAIL → 切換回 Generator root → 根據 feedback 修正         │
│ 🔄 REPLAN → 切換回 Planner root → 重新規劃                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 實際操作步驟

### 1. 建立 Multi-Root Workspace

```powershell
# 建立目錄結構
mkdir C:\Users\proje\AgentWorkspace
mkdir C:\Users\proje\AgentWorkspace\planner\.kiro\steering
mkdir C:\Users\proje\AgentWorkspace\planner\.kiro\hooks
mkdir C:\Users\proje\AgentWorkspace\planner\.kiro\specs
mkdir C:\Users\proje\AgentWorkspace\generator\.kiro\steering
mkdir C:\Users\proje\AgentWorkspace\generator\.kiro\hooks
mkdir C:\Users\proje\AgentWorkspace\generator\.kiro\specs
mkdir C:\Users\proje\AgentWorkspace\evaluator\.kiro\steering
mkdir C:\Users\proje\AgentWorkspace\evaluator\.kiro\hooks
mkdir C:\Users\proje\AgentWorkspace\evaluator\.kiro\specs
mkdir C:\Users\proje\AgentWorkspace\shared\requirements
mkdir C:\Users\proje\AgentWorkspace\shared\handoff
mkdir C:\Users\proje\AgentWorkspace\shared\final
```

### 2. 建立 .code-workspace 文件

用 Kiro 開啟：`File → Open Workspace from File`

### 3. 寫入各 Agent 的 Steering

每個 root folder 的 `.kiro/steering/` 寫入對應角色的指令。

### 4. 使用方式

```
1. 將需求寫入 shared/requirements/user-request.md
2. 喺 Kiro Chat 切換到 Planner root → 話「開始規劃」
3. Planner 完成後，切換到 Generator root → 話「開始生成」
4. Generator 完成後，切換到 Evaluator root → 話「開始評估」
5. 根據 Evaluator 結果決定下一步
```

---

## 限制同注意事項

| 限制 | 說明 |
|------|------|
| 唔係真正並行 | 同一時間只有一個 Agent 執行，需要手動切換 |
| 需要手動切換 root | Kiro 唔會自動切換 Agent 角色 |
| 共享文件做交接 | Agent 之間透過 JSON 文件交流，唔係直接對話 |
| 冇自動循環 | FAIL 後需要你手動切換回 Generator |

---

## 同 Claude Code 的對比

| | Kiro（Multi-Root 方案） | Claude Code |
|---|---|---|
| 獨立記憶 | ✅ 每個 root 有獨立 steering | ✅ 每個 agent 有獨立 .md |
| 獨立 Spec | ✅ 每個 root 有獨立 specs | ❌ 冇 Spec 概念 |
| 自動切換 | ❌ 需手動 | ✅ 主 Agent 自動調度 |
| 並行執行 | ❌ 同一時間一個 | ✅ 真正並行 |
| 自動循環 | ❌ 需手動 | ✅ Evaluator FAIL 自動重試 |
| 結構化規劃 | ✅ Spec workflow | ❌ |

---

## 未來改進方向

如果 Kiro 日後支援：
- **自定義 Sub Agent 配置文件**（類似 `.claude/agents/`）
- **Agent 之間自動路由**
- **定時觸發**

就可以實現完全自動的 Planner-Generator-Evaluator 循環。

---

## 參考

| 資源 | 連結 |
|------|------|
| Kiro Multi-Root Workspace 文檔 | https://kiro.dev/docs/editor/multi-root-workspaces |
| Anthropic Multi-Agent 模式 | https://claude.com/blog/multi-agent-coordination-patterns |
| Claude Code Sub Agents 文檔 | https://code.claude.com/docs/en/sub-agents |
