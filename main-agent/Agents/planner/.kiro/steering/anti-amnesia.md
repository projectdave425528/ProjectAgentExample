---
inclusion: always
description: Anti-Amnesia 規則（L1 - 永遠載入，零例外，適用所有 Agent）
---

# Anti-Amnesia 規則

> 🔒 本規則唔可以跳過。你可能經歷過 context compaction 而唔自知。

## 核心原則

Context compaction 會壓縮對話歷史，但 **唔會壓縮 steering**。
所以呢條規則每次都會出現喺你嘅 system prompt — 即使你唔記得之前做過咩。

## 規則（零例外）

### 觸發條件

當你正在執行**多步驟任務**（建多個文件、修改多個 Agent、批量操作）時：

### 每個 Step 開始前：讀 Progress Marker

**每個 Step 開始之前**，必須讀取 progress marker：

1. 根據任務類型確認 marker 路徑（見下方）
2. 檢查 `progress-marker.md` 是否存在
3. 如果存在 → 讀取內容，確認 `next` 欄位，從該 Step 繼續
4. 如果唔存在 → 正常開始，建立新 marker

### 每個 Step 完成後：覆蓋 Marker

用 `fs_write`（覆蓋）更新 marker，格式：

```markdown
# Progress
task: {任務描述}
last_completed: Step {N} - {描述}
next: Step {N+1} - {描述}
total: {總步數}
```

### 完成時：刪除 Marker

任務全部完成後，刪除 `progress-marker.md`。

## Progress Marker 路徑

| 任務類型 | 路徑 | 判斷標準 |
|---------|------|---------|
| Project 內容 | `./ProjectRecord/{active-project}/progress-marker.md` | 涉及寫 code、改 ProjectRecord、派 Assignment |
| Project 外內容 | `./progress-marker.md` | 改 steering、hooks、通用操作 |

判斷方式：
- 操作對象喺 `ProjectRecord/{project}/` 入面 → Project 路徑
- 操作對象喺 `.kiro/`、`Agents/`、其他 → Agent 目錄路徑

## 判斷「多步驟任務」

以下情況必須用 progress marker：
- 建立/修改 ≥ 3 個文件
- 操作涉及多個目標（多個 Agent / 多個 Protocol）
- 預計耗時 > 5 分鐘
- 用戶明確描述多個步驟

以下情況**唔需要**：
- 單文件修改
- 純問答/解釋
- 讀取 + 回覆

## Marker 大小限制

- **永遠只有 5 行**（header + 4 個欄位）
- 每次覆蓋，唔係 append
- ~20 tokens，成本極低

## 同 Checkpoint 嘅關係

| 機制 | 目的 | 並行？ |
|------|------|:---:|
| **Progress Marker** | 防失憶 — 知道「做到邊」 | ✅ |
| **Checkpoint** | 執行記錄 — 記錄「做過咩」（每步操作詳情） | ✅ |

兩者獨立運作，唔衝突。Checkpoint 係詳細記錄，Marker 係極簡狀態指標。
