# Kiro CLI Multi-Agent 架構 v1.0

> 用 Kiro CLI Custom Agents 實現 Planner / Generator / Evaluator 循環
> Main Agent（IDE）做中央調度，透過 shell 調用 CLI Agent
> 全自動、獨立 context、唔需要切換 Window
> 設計日期：2026-05-24

---

## 架構總覽

```
┌─────────────────────────────────────────────────────────────────────┐
│                          用戶（你）                                   │
│                   只同 Main Agent 對話                                │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Main Agent (Kiro IDE)                                              │
│  Workspace: C:\Users\proje\ProjectKiro                              │
│                                                                     │
│  職責：接收需求 → 調用 CLI Agent → 判斷結果 → 循環/交付              │
│  控制：可暫停 / 重啟 / 跳過任何步驟                                   │
│  方式：透過 execute_pwsh 調用 kiro-cli                               │
└──────┬──────────────────────┬──────────────────────┬────────────────┘
       │                      │                      │
       │ kiro-cli             │ kiro-cli             │ kiro-cli
       │ --agent planner      │ --agent generator    │ --agent evaluator
       ▼                      ▼                      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ CLI Agent    │    │ CLI Agent    │    │ CLI Agent    │
│ Planner      │    │ Generator    │    │ Evaluator    │
│              │    │              │    │              │
│ 獨立 context │    │ 獨立 context │    │ 獨立 context │
│ 獨立 prompt  │    │ 獨立 prompt  │    │ 獨立 prompt  │
│ 執行完即結束 │    │ 執行完即結束 │    │ 執行完即結束 │
└──────────────┘    └──────────────┘    └──────────────┘
```

### 同 v2.0（Multi-Window）嘅分別

| | v2.0 Multi-Window | v1.0 Kiro CLI |
|---|---|---|
| 觸發方式 | 手動切換 window + 打「go」 | Main Agent 直接調用 CLI |
| 自動程度 | 半自動（需要人手） | 全自動 |
| 獨立 context | ✅ 每個 window 獨立 | ✅ 每次 CLI 調用獨立 |
| Hook 需要 | 需要但唔觸發 | 唔需要 |
| 並行能力 | 多 window 同時 | background process 同時 |
| Agent 間直接通訊 | 透過文件 | ❌ 全部經 Main Agent 路由 |


---

## 目錄結構

```
C:\Users\proje\ProjectKiro\
│
├── .kiro\
│   ├── steering\              ← Main Agent 規則
│   └── agents\                ← CLI Custom Agent 定義（新增）
│       ├── planner.json
│       ├── generator.json
│       └── evaluator.json
│
├── ProjectMultiAgent\
│   ├── planner\
│   │   ├── .kiro\steering\    ← Planner Steering（CLI resources 引用）
│   │   ├── inbox\             ← 任務文件（保留做記錄）
│   │   └── outbox\            ← 回覆文件（保留做記錄）
│   ├── generator\
│   │   ├── .kiro\steering\
│   │   ├── inbox\
│   │   └── outbox\
│   ├── evaluator\
│   │   ├── .kiro\steering\
│   │   ├── inbox\
│   │   └── outbox\
│   └── shared\
│       ├── conversation-log.md
│       └── control\commands.md
│
└── UserConfig\sessions\        ← 所有 Agent 嘅 session log
```

---

## Custom Agent 定義

### planner.json

```json
{
  "name": "planner",
  "description": "分析需求、設計架構、拆分任務",
  "prompt": "你係 Planner Agent。你嘅職責係分析需求、設計系統架構、選擇技術棧、拆分成可獨立開發嘅子任務。你唔可以寫代碼。你必須輸出：技術方案摘要、系統架構圖、子任務清單（含依賴關係）、風險評估。如果收到 feedback，按照 feedback 修改方案。",
  "tools": ["fs_read", "fs_write", "execute_bash"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["ProjectMultiAgent/planner/outbox/**", "ProjectMultiAgent/shared/**"]
    }
  },
  "resources": [
    "file://ProjectMultiAgent/planner/.kiro/steering/00-role.md"
  ]
}
```

### generator.json

```json
{
  "name": "generator",
  "description": "根據計劃生成代碼、寫測試",
  "prompt": "你係 Generator Agent。你嘅職責係根據 Planner 嘅計劃生成代碼。收到任務後先自我評估做唔做到：如果能力不足先嘗試自學（搜尋文檔/Web），自學失敗先回報 blocked。代碼規範：函數 < 30 行、參數 ≤ 3、Loop ≤ 3 層、用 Interface 通訊、DI。收到 Evaluator feedback 時只修正被指出嘅問題。",
  "tools": ["fs_read", "fs_write", "execute_bash"],
  "toolsSettings": {
    "fs_write": {
      "allowedPaths": ["ProjectMultiAgent/generator/outbox/**", "ProjectMultiAgent/shared/**"]
    }
  },
  "resources": [
    "file://ProjectMultiAgent/generator/.kiro/steering/00-role.md"
  ]
}
```

### evaluator.json

```json
{
  "name": "evaluator",
  "description": "審查代碼品質、跑測試、評分反饋",
  "prompt": "你係 Evaluator Agent。你嘅職責係檢查 Generator 嘅代碼質量。按 Checklist 評分：功能性(40%) + 代碼品質(30%) + 安全性(20%) + 可維護性(10%)。Verdict：>= 80 PASS、60-79 FAIL、< 60 REPLAN。FAIL 時提供具體修正建議（文件+行號+描述）。你唔可以修改代碼。最多連續 FAIL 3 次後強制 REPLAN。",
  "tools": ["fs_read", "execute_bash"],
  "toolsSettings": {},
  "resources": [
    "file://ProjectMultiAgent/evaluator/.kiro/steering/00-role.md"
  ]
}
```


---

## 完整工作流程

```
┌──────────────────────────────────────────────────────────────────┐
│ Phase 1: 用戶輸入需求                                             │
│ 用戶 → Main Agent：「幫我建立 XXX 系統」                           │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 2: Main Agent 調用 Planner CLI                              │
│                                                                  │
│ 命令：kiro-cli chat --agent planner "讀取任務並規劃..."           │
│                                                                  │
│ • 寫任務到 planner/inbox/（做記錄）                               │
│ • 調用 CLI → 等待完成 → 收到結果                                  │
│ • Planner 寫回覆到 planner/outbox/（做記錄）                      │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 3: Main Agent 審視計劃                                      │
│                                                                  │
│ • 讀取 Planner 回覆                                               │
│ • 判斷計劃質量（可問用戶確認）                                     │
│ • 如果有 escalation → 問用戶取得資源                              │
│ • OK → 進入 Phase 4                                              │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 4: Main Agent 調用 Generator CLI                            │
│                                                                  │
│ 命令：kiro-cli chat --agent generator "按以下計劃生成代碼..."     │
│                                                                  │
│ • 將 Planner 計劃作為 prompt 傳入                                 │
│ • 調用 CLI → 等待完成 → 收到結果                                  │
│ • Generator 寫代碼到 generator/outbox/                            │
│                                                                  │
│ 可能結果：                                                        │
│ • ✅ 代碼完成 → Phase 5                                          │
│ • ❌ blocked → Main Agent 判斷：                                  │
│   - 設計問題 → 重新調用 Planner                                   │
│   - 權限問題 → 問用戶                                             │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 5: Main Agent 調用 Evaluator CLI                            │
│                                                                  │
│ 命令：kiro-cli chat --agent evaluator "評估以下代碼..."           │
│                                                                  │
│ • 將計劃 + 代碼位置作為 prompt 傳入                               │
│ • 調用 CLI → 等待完成 → 收到 verdict                              │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Phase 6: Main Agent 判斷結果                                      │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────┐      │
│ │ PASS (>= 80 分)                                        │      │
│ │ → 交付俾用戶                                            │      │
│ └─────────────────────────────────────────────────────────┘      │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────┐      │
│ │ FAIL (60-79 分)                                        │      │
│ │ → 將 feedback 傳入，重新調用 Generator CLI              │      │
│ │ → 回到 Phase 4                                         │      │
│ └─────────────────────────────────────────────────────────┘      │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────┐      │
│ │ REPLAN (< 60 分)                                       │      │
│ │ → 將 feedback 傳入，重新調用 Planner CLI                │      │
│ │ → 回到 Phase 2                                         │      │
│ └─────────────────────────────────────────────────────────┘      │
│                                                                  │
│ 循環限制：最多 3 次 FAIL → 強制 REPLAN                            │
│ 最多 2 次 REPLAN → 問用戶點處理                                   │
└──────────────────────────────────────────────────────────────────┘
```


---

## 循環反饋流程圖

```
                    ┌─────────────┐
                    │   用戶需求   │
                    └──────┬──────┘
                           │
                           ▼
                  ┌─────────────────┐
          ┌──────│   Main Agent    │◀─────────────────┐
          │      │  (Orchestrator) │                  │
          │      └──┬──────────┬──┘                  │
          │         │          │                     │
          │  調用   │          │ 調用                 │
          │ Planner │          │ Generator           │
          │  CLI    │          │  CLI                 │
          │         ▼          ▼                     │
          │  ┌────────┐  ┌──────────┐               │
          │  │Planner │  │Generator │               │
          │  │  CLI   │  │   CLI    │               │
          │  └───┬────┘  └────┬─────┘               │
          │      │            │                     │
          │      │ 返回       │ 返回                 │
          │      │ 計劃       │ 代碼                 │
          │      ▼            ▼                     │
          │  Main Agent 收到結果                     │
          │      │                                  │
          │      │ 調用 Evaluator CLI               │
          │      ▼                                  │
          │  ┌──────────┐                           │
          │  │Evaluator │                           │
          │  │   CLI    │                           │
          │  └────┬─────┘                           │
          │       │                                 │
          │       │ 返回 verdict                    │
          │       ▼                                 │
          │  Main Agent 判斷                        │
          │       │                                 │
          │  ┌────┼────┐                            │
          │  │    │    │                            │
          │ PASS FAIL REPLAN                        │
          │  │    │    │                            │
          │  │    │    └────────────────────────────┘
          │  │    │         重新調用 Planner
          │  │    └──→ 重新調用 Generator（附 feedback）
          │  │
          │  ▼
          │  交付用戶
          │
          └── REPLAN 時重新調用 Planner
```


---

## 調用方式詳解

### Main Agent 調用 Planner

```powershell
# 方式 1：直接傳 prompt
& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent planner "分析以下需求並設計技術方案：[需求內容]"

# 方式 2：從文件讀取任務
Get-Content "ProjectMultiAgent\planner\inbox\task-001.md" | & "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent planner

# 方式 3：指定工作目錄
& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent planner --cwd "C:\Users\proje\ProjectKiro\ProjectMultiAgent\planner" "執行規劃任務"
```

### Main Agent 調用 Generator

```powershell
& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent generator "按以下計劃生成代碼：[Planner 嘅計劃內容]"
```

### Main Agent 調用 Evaluator

```powershell
& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent evaluator "評估以下代碼，對照計劃檢查：[計劃摘要 + 代碼位置]"
```

---

## 並行調用

### 獨立任務並行（Background Process）

```powershell
# 同時調用多個 Generator 做唔同子任務
Start-Process "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" -ArgumentList "chat --agent generator `"完成 Task 1: 項目骨架`"" -NoNewWindow
Start-Process "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" -ArgumentList "chat --agent generator `"完成 Task 3: 模板集合`"" -NoNewWindow
```

### 喺 Kiro IDE 入面用 invoke_sub_agent 並行

```
Main Agent 同時 invoke 多個 sub agent：
├── invoke_sub_agent("general-task-execution", "以 Planner 角色...")
├── invoke_sub_agent("general-task-execution", "以 Researcher 角色...")
```

---

## 用戶控制機制

| 用戶講 | Main Agent 做 |
|--------|--------------|
| 「開始規劃 XXX」 | 調用 Planner CLI |
| 「暫停」 | 停止當前流程，等用戶指示 |
| 「繼續」 | 繼續上次停止嘅步驟 |
| 「重啟 Planner」 | 重新調用 Planner CLI（新 prompt） |
| 「跳過評估」 | 唔調用 Evaluator，直接交付 |
| 「keep going」 | 繼續正常流程 |
| 「狀態」 | 報告當前進度（邊個 Phase） |
| 「取消」 | 停止所有流程 |

---

## 錯誤處理

| 情況 | Main Agent 行動 |
|------|----------------|
| CLI 調用超時 | 通知用戶，問是否重試 |
| Generator 回報 blocked | 判斷原因：設計問題 → 重調 Planner；權限問題 → 問用戶 |
| Evaluator 連續 3 次 FAIL | 強制 REPLAN，重調 Planner |
| 連續 2 次 REPLAN | 問用戶點處理（可能需求本身有問題） |
| CLI 返回空結果 | 重試一次，仍然空就通知用戶 |


---

## 同 v2.0（Multi-Window）嘅完整對比

| 特性 | v2.0 Multi-Window | v1.0 Kiro CLI |
|------|-------------------|---------------|
| 觸發方式 | 手動切換 window + 打「go」 | Main Agent 直接 shell 調用 |
| 自動程度 | 半自動 | ✅ 全自動 |
| 獨立 context | ✅ | ✅ |
| 獨立 Steering | ✅ 每個 window 獨立載入 | ✅ resources 引用 |
| Hook 需要 | 需要但實測唔觸發 | ❌ 唔需要 |
| Agent 間直接通訊 | ✅ Evaluator → Generator | ❌ 全部經 Main Agent |
| 並行 | 多 window 同時 | background process |
| 文件記錄 | inbox/outbox | inbox/outbox（保留做 audit） |
| 用戶介入 | 每步都要切換 | 只需要講需求 + 確認 |
| 安裝需求 | 無 | Kiro CLI |
| Credits 消耗 | IDE credits | CLI credits（同 pool） |

---

## 保留嘅設計（從 v2.0 繼承）

以下設計喺 CLI 版本仍然有效：

| 設計 | 用途 | 點用 |
|------|------|------|
| inbox/outbox 文件 | Audit trail | Main Agent 每次調用前寫 inbox，收到結果寫 outbox |
| Message 格式（frontmatter） | 結構化記錄 | 保持 id/from/to/timestamp/type/status |
| status.md | 狀態追蹤 | Main Agent 更新各 Agent 狀態 |
| conversation-log.md | 完整歷史 | Main Agent 每步追加記錄 |
| Steering 文件 | Agent 角色定義 | CLI resources 引用 |
| 自我評估（Generator） | 能力判斷 | 寫入 Agent prompt |
| 自學流程（Generator） | 先學再上報 | 寫入 Agent prompt |
| Evaluator Checklist | 評分標準 | 寫入 Agent prompt |
| 循環限制 | 防止無限 loop | Main Agent 計數 |

---

## 唔再需要嘅設計

| 設計 | 原因 |
|------|------|
| watch-inbox Hook | CLI 係被調用嘅，唔需要監聽 |
| watch-notify Hook | 同上 |
| auto-check-inbox Hook | 同上 |
| check-inbox Hook（userTriggered） | 同上 |
| notify-main.md | Main Agent 直接收到 CLI 返回值 |
| Evaluator 直接寫 Generator inbox | 改為經 Main Agent 路由 |
| Generator 直接寫 Evaluator inbox | 改為經 Main Agent 路由 |

---

## 安裝同設定

### 前提
- ✅ Kiro CLI 已安裝（`C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe`）
- ✅ 已登入（`& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe"` → 選擇認證方式）
- ✅ ProjectMultiAgent 目錄已建立

### 設定 Custom Agents
將 agent JSON 文件放入 `.kiro/agents/` 目錄：
```
C:\Users\proje\ProjectKiro\.kiro\agents\
├── planner.json
├── generator.json
└── evaluator.json
```

### 驗證
```powershell
& "C:\Users\proje\AppData\Local\Kiro-Cli\kiro-cli.exe" chat --agent planner "你係邊個？"
```

---

## 快速參考卡

```
┌─────────────────────────────────────────────────┐
│ Main Agent 流程                                  │
├─────────────────────────────────────────────────┤
│ 1. 收到用戶需求                                  │
│ 2. 調用 Planner CLI → 收到計劃                   │
│ 3. 審視計劃（問用戶確認）                         │
│ 4. 調用 Generator CLI → 收到代碼                 │
│ 5. 調用 Evaluator CLI → 收到 verdict            │
│ 6. PASS → 交付 / FAIL → 重做 / REPLAN → 重規劃 │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ CLI 命令                                         │
├─────────────────────────────────────────────────┤
│ & "...\kiro-cli.exe" chat --agent planner "..."  │
│ & "...\kiro-cli.exe" chat --agent generator "..."│
│ & "...\kiro-cli.exe" chat --agent evaluator "..."│
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 文件記錄（Audit Trail）                          │
├─────────────────────────────────────────────────┤
│ 調用前：寫 inbox/task-{NNN}.md                   │
│ 調用後：寫 outbox/task-{NNN}-reply.md            │
│ 每步：追加 shared/conversation-log.md            │
└─────────────────────────────────────────────────┘
```

---

## 待驗證事項

| 項目 | 狀態 | 備註 |
|------|------|------|
| Kiro CLI 登入 | ⬜ 待做 | 需要用戶手動認證 |
| Custom Agent JSON 格式 | ⬜ 待驗證 | 官方文檔嘅格式可能有更新 |
| CLI 能否讀取 workspace 外嘅文件 | ⬜ 待驗證 | toolsSettings 嘅 allowedPaths |
| CLI 嘅 stdout 格式 | ⬜ 待驗證 | Main Agent 點 parse 返回值 |
| 並行調用穩定性 | ⬜ 待驗證 | 多個 CLI process 同時跑 |
| Credits 消耗量 | ⬜ 待觀察 | 每次 CLI 調用消耗幾多 |
