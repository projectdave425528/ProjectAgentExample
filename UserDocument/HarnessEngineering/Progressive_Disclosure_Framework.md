# Progressive Disclosure Framework for AI Agent
# AI Agent 漸進式披露框架

> 版本：1.0.0  
> 建立日期：2026-05-23  
> 用途：AI Agent 知識管理、動態內容定位、雙向搜尋

---

## 目錄

<!-- @toc -->
1. [核心概念](#核心概念)
2. [三層架構](#三層架構)
3. [標記語法](#標記語法)
4. [定位策略](#定位策略)
5. [搜尋方式](#搜尋方式)
6. [文件格式範例](#文件格式範例)
7. [維護指引](#維護指引)
8. [Agent 通訊擴展](#agent-通訊擴展)
9. [快速參考卡](#快速參考卡)
<!-- /@toc -->

---

## 核心概念

<!-- @core-concept -->
[concept] [progressive-disclosure] [overview]

### 什麼是漸進式披露？

只俾 Agent 睇佢而家需要嘅資訊，其他嘢等需要時先載入。

### 設計目標

| 目標 | 說明 |
|------|------|
| **減少 Token 消耗** | 唔需要一次載入所有內容 |
| **提高搜尋效率** | 用戶同 AI 都可以快速定位 |
| **支援動態內容** | 經常修改嘅文件都可以準確定位 |
| **雙向搜尋** | Ctrl+F 同 grep_search 都 work |

### 適用場景

- Steering 文件（AI 規則）
- Session log（對話記錄）
- 項目文件（需求、設計、架構）
- Agent 記憶系統
<!-- /@core-concept -->

---

## 三層架構

<!-- @three-layers -->
[architecture] [layers] [structure]

### 架構圖

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Index（索引）                                  │
│  ├─ 永遠載入                                            │
│  ├─ 名稱 + 關鍵字標籤 [tag]                             │
│  └─ 指向 Layer 2 / Layer 3                              │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Summary（摘要）                                │
│  ├─ 需要時載入                                          │
│  ├─ 結構化摘要 + 章節錨點                               │
│  └─ 指向 Layer 3 詳情位置                               │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Detail（詳情）                                 │
│  ├─ 執行時載入                                          │
│  ├─ 完整內容 + 行內標記                                 │
│  └─ 錨點區塊標記                                        │
└─────────────────────────────────────────────────────────┘
```

### 對應 Kiro 設定

| 層級 | Kiro 機制 | 載入時機 |
|------|----------|---------|
| Layer 1 | Steering (always) | 每次對話自動載入 |
| Layer 2 | Steering (manual) | 用戶 `#引用` 時載入 |
| Layer 3 | File Reference / Skills | 執行任務時載入 |

### 內容分配原則

| 層級 | 內容類型 | 大小限制 |
|------|---------|---------|
| L1 Index | 名稱 + 一句描述 + 關鍵字 | < 50 行 |
| L2 Summary | 結構化摘要 + 重點列表 | < 200 行 |
| L3 Detail | 完整內容 + 代碼 + 範例 | 無限制 |
<!-- /@three-layers -->

---

## 標記語法

<!-- @markup-syntax -->
[syntax] [markup] [tags]

### 統一標記系統（用戶 + AI 通用）

| 標記類型 | 語法 | 用途 | 穩定性 |
|---------|------|------|:------:|
| **關鍵字標籤** | `[keyword]` | 主題分類搜尋 | ⭐⭐⭐ |
| **錨點 ID** | `<!-- @anchor-id -->` | 精確定位區塊 | ⭐⭐⭐ |
| **錨點區塊** | `<!-- @id --> ... <!-- /@id -->` | 標記內容範圍 | ⭐⭐⭐ |
| **唯一短語** | `@unique: xxx` | 段落識別 | ⭐⭐ |
| **Heading** | `## Section Name` | 章節結構 | ⭐⭐ |
| **行號** | `#L50` 或 `#L50-L80` | 靜態文件定位 | ⭐ |

### 關鍵字標籤規範

```markdown
# 正確用法
[token] [context] [limit]
[risk] [formula] [calculation]

# 錯誤用法
token, context, limit     ← 冇方括號，搜尋困難
#token #context           ← 同 Markdown heading 混淆
```

### 錨點區塊規範

```markdown
<!-- @anchor-id:簡短描述 -->
[keyword1] [keyword2]

內容區塊...

<!-- /@anchor-id -->
```

**規則：**
- 錨點 ID 用英文小寫 + 連字號（kebab-case）
- 描述用中文或英文都可以
- 開始同結束標記必須配對
<!-- /@markup-syntax -->

---

## 定位策略

<!-- @positioning-strategy -->
[positioning] [strategy] [dynamic]

### 靜態 vs 動態文件

| 定位方式 | 靜態文件 | 動態文件（經常修改） |
|---------|:-------:|:------------------:|
| 行號 `#L50` | ✅ 穩定 | ❌ 會失效 |
| Heading `## Section` | ✅ 穩定 | ⚠️ 改名會失效 |
| 錨點 `<!-- @id -->` | ✅ 穩定 | ✅ 跟住內容走 |
| 關鍵字 `[tag]` | ✅ 穩定 | ✅ 搜尋永遠有效 |

### 動態文件定位優先級

| 優先級 | 方法 | 語法 | 適用場景 |
|:------:|------|------|---------|
| 1 | **錨點 ID** | `<!-- @anchor-id -->` | 重要段落，必須精確定位 |
| 2 | **關鍵字標籤** | `[tag1] [tag2]` | 主題分類，搜尋用 |
| 3 | **唯一短語** | `@unique: xxx` | 段落開頭標記 |
| 4 | **Heading** | `## Section Name` | 章節結構 |
| 5 | **行號** | `#L50-L80` | 只用於靜態文件 |

### 定位選擇決策樹

```
文件會經常修改？
├─ 是 → 用錨點 + 關鍵字
│       ├─ 重要段落 → 加 <!-- @anchor-id -->
│       └─ 一般內容 → 加 [keyword] 標籤
└─ 否 → 可以用行號
        ├─ 穩定段落 → #L50-L80
        └─ 可能改動 → 仍建議用錨點
```
<!-- /@positioning-strategy -->

---

## 搜尋方式

<!-- @search-methods -->
[search] [user] [agent]

### 雙向搜尋對照表

| 標記 | 用戶搜尋 | AI Agent 搜尋 |
|------|---------|--------------|
| `[keyword]` | Ctrl+F `[keyword]` | `grep_search "\[keyword\]"` |
| `## Section` | 目錄跳轉 | `grep_search "## Section"` |
| `<!-- @anchor -->` | Ctrl+F `@anchor` | `grep_search "@anchor"` |
| `@unique: xxx` | Ctrl+F `@unique:` | `grep_search "@unique: xxx"` |

### AI Agent 搜尋流程

```
用戶問：「Risk 公式係咩？」

方法 A：錨點搜尋（最準確）
1. grep_search "@risk-formula" → 搵到錨點位置
2. 讀取錨點區塊內容
3. 回答用戶

方法 B：關鍵字搜尋（最靈活）
1. grep_search "\[risk\].*\[formula\]" → 搵到相關段落
2. 讀取上下文
3. 回答用戶

方法 C：唯一短語搜尋（備用）
1. grep_search "@unique: Risk calculation"
2. 讀取該段落
3. 回答用戶
```

### 搜尋優先順序

```
1. 先搵錨點 → grep_search "@anchor-id"
2. 搵唔到 → 搵關鍵字 → grep_search "\[keyword\]"
3. 仲搵唔到 → 搵唯一短語 → grep_search "@unique:"
4. 最後 → 全文搜尋
```
<!-- /@search-methods -->

---

## 文件格式範例

<!-- @file-templates -->
[template] [format] [example]

### Index 文件範例

```markdown
# 知識庫索引

<!-- @index-main -->
[index] [knowledge-base]

| 主題 | 關鍵字 | 定位方式 | 位置 |
|------|--------|---------|------|
| Risk 公式 | `[risk]` `[formula]` | 錨點 | `@risk-formula` in `rules.md` |
| Token 限制 | `[token]` `[limit]` | 錨點 | `@token-limit` in `config.md` |
| 交易策略 | `[trade]` `[strategy]` | 關鍵字 | 搜尋 `[trade]` in `strategy.md` |

## 快速搜尋指引
- 用戶：Ctrl+F 輸入 `[keyword]` 搵相關主題
- AI：`grep_search "\[keyword\]"` 搵所有相關位置
<!-- /@index-main -->
```

### Summary 文件範例

```markdown
# Risk 管理摘要

<!-- @risk-summary -->
[risk] [management] [overview]

## 重點
1. 單筆風險上限：2%
2. 日風險上限：6%
3. 強制止損觸發：-10%

## 詳情入口
| # | 內容 | 定位 |
|---|------|------|
| 1 | 計算公式 | `@risk-formula` in `detail.md` |
| 2 | 觸發條件 | `@risk-trigger` in `detail.md` |
| 3 | 歷史案例 | 搜尋 `[risk] [case]` |
<!-- /@risk-summary -->
```

### Detail 文件範例

```markdown
# Risk 管理詳情

<!-- @risk-formula:風險計算公式 -->
[risk] [formula] [calculation]

@unique: Risk calculation formula v2

**公式：**
Risk = Position × Volatility × Multiplier

**參數：**
- Position：持倉金額
- Volatility：波動率（ATR）
- Multiplier：風險係數（預設 1.5）
<!-- /@risk-formula -->

---

<!-- @risk-trigger:風險觸發條件 -->
[risk] [trigger] [condition]

@unique: Risk trigger conditions

**觸發條件：**
1. 單筆虧損 > 2% → 強制平倉
2. 日虧損 > 6% → 暫停交易
3. 連續虧損 3 次 → 減半倉位
<!-- /@risk-trigger -->
```
<!-- /@file-templates -->

---

## 維護指引

<!-- @maintenance -->
[maintenance] [guideline] [update]

### 日常維護

| 操作 | 做法 |
|------|------|
| 新增重要段落 | 加 `<!-- @anchor-id -->` 錨點 |
| 修改內容 | 錨點 ID 保持不變，內容隨便改 |
| 刪除段落 | 同時更新 Index 移除引用 |
| 重組結構 | 錨點跟住內容搬，唔需要改 Index |
| 改關鍵字 | 更新所有引用該關鍵字嘅位置 |

### 錨點命名規範

| 類型 | 格式 | 例子 |
|------|------|------|
| 功能區塊 | `@feature-name` | `@risk-formula` |
| 配置區塊 | `@config-name` | `@config-token-limit` |
| 規則區塊 | `@rule-name` | `@rule-stop-loss` |
| 流程區塊 | `@flow-name` | `@flow-order-execution` |

### 關鍵字分類建議

| 類別 | 關鍵字例子 |
|------|----------|
| 主題 | `[risk]` `[token]` `[trade]` |
| 類型 | `[formula]` `[rule]` `[config]` |
| 狀態 | `[draft]` `[final]` `[deprecated]` |
| 優先級 | `[critical]` `[important]` `[optional]` |
<!-- /@maintenance -->

---

## Agent 通訊擴展

<!-- @agent-communication -->
[agent] [communication] [multi-agent]

### 擴展標記（Multi-Agent 系統用）

| 標記 | 語法 | 用途 |
|------|------|------|
| Agent 輸出 | `<!-- @agent:agent-name:task-id -->` | 標記某個 Agent 嘅輸出 |
| Agent 引用 | `[→ @agent:planner:task-001]` | 引用另一個 Agent 嘅輸出 |
| User 指令 | `<!-- @user:instruction-id -->` | 標記用戶重要指令 |
| 對話錨點 | `<!-- @conv:topic-keyword -->` | 標記對話主題 |

### Agent 通訊記錄範例

```markdown
<!-- @agent:planner:task-001 -->
[agent] [planner] [task-001]

**Planner 輸出：**
1. 分析需求 → Generator
2. 生成代碼 → Evaluator
3. 評估結果 → 返回 Planner
<!-- /@agent:planner:task-001 -->

---

<!-- @agent:generator:task-001 -->
[agent] [generator] [task-001]

**Generator 輸出：**
引用 Planner 指令：[→ @agent:planner:task-001]

生成代碼：...
<!-- /@agent:generator:task-001 -->
```

### Agent 搜尋方式

```
搵 Planner 嘅輸出：
grep_search "@agent:planner"

搵特定任務：
grep_search "@agent:.*:task-001"

搵所有 Agent 通訊：
grep_search "@agent:"
```
<!-- /@agent-communication -->

---

## 快速參考卡

<!-- @quick-reference -->
[reference] [cheatsheet]

### 標記速查

| 用途 | 語法 |
|------|------|
| 關鍵字 | `[keyword]` |
| 錨點開始 | `<!-- @anchor-id:描述 -->` |
| 錨點結束 | `<!-- /@anchor-id -->` |
| 唯一短語 | `@unique: xxx` |
| Agent 標記 | `<!-- @agent:name:task -->` |

### 搜尋速查

| 目標 | AI 指令 |
|------|--------|
| 搵關鍵字 | `grep_search "\[keyword\]"` |
| 搵錨點 | `grep_search "@anchor-id"` |
| 搵 Agent | `grep_search "@agent:name"` |
| 搵唯一短語 | `grep_search "@unique:"` |

### 定位優先級

```
動態文件：錨點 > 關鍵字 > 唯一短語 > Heading
靜態文件：行號 > 錨點 > 關鍵字
```
<!-- /@quick-reference -->

---

*文件結束*
