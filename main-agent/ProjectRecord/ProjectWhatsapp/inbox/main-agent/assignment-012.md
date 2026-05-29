# Assignment 012

- **From**: main-agent
- **To**: main-agent (self) + generator + evaluator
- **Timestamp**: 2026-05-28T21:45:00+08:00
- **Type**: integration-fix-notice
- **TaskRef**: Test-Env Integration Fix（跨 Task 2-4）
- **TaskID**: ProjectWhatsapp/Test-Env-Fix
- **TaskStatus**: completed（Main Agent 已修正）

---

## 通知內容
Main Agent 喺建立合併測試環境（test-env）時發現 3 個 integration 問題，已自行修正。通知所有 Agent 更新知識。

---

## 發現嘅問題

### 問題 1: match_message_line 唔處理系統訊息（Critical）
- **位置**：`src/parser/patterns.py` — `match_message_line()`
- **原因**：WhatsApp 系統訊息格式 `[timestamp] content`（冇 `: ` 分隔符），`split_sender_content` 返回 None 後直接返回 None → 系統訊息被跳過
- **修正**：冇 `: ` 時返回 `(timestamp, "", content)` 而唔係 `None`
- **影響**：Task 3 text_parser 需要配合處理 empty sender

### 問題 2: Floating point precision（Minor）
- **位置**：`src/analyzer/ocr_analyzer.py` — `_calculate_confidence()`
- **原因**：`0.3 + 0.35 + 0.35 = 0.9999999999999999`（IEEE 754）
- **修正**：加 `round(score, 2)`

### 問題 3: text_parser 未處理 empty sender
- **位置**：`src/parser/text_parser.py` — `_process_line()`
- **原因**：match_message_line 返回 empty sender 時，ParsedMessage 嘅 sender min_length=1 會 fail
- **修正**：empty sender 時用 content 作為 sender（系統訊息嘅 content 就係完整描述）

---

## 修正摘要
| 文件 | 修正 |
|------|------|
| `src/parser/patterns.py` | match_message_line 冇 `: ` 時返回 (ts, "", content) |
| `src/parser/text_parser.py` | empty sender 時用 content 作為 sender |
| `src/analyzer/ocr_analyzer.py` | confidence 加 round(score, 2) |
| `tests/test_parser.py` | 改為 content search 唔依賴 hardcoded index |

---

## 教訓（所有 Agent 共用）
1. **系統訊息格式同普通訊息唔同** — 冇 sender: content 結構，只有 [timestamp] description
2. **Floating point 加法要 round** — 特別係用嚟做 assert 比較時
3. **Integration test 會暴露單元測試搵唔到嘅問題** — 各 Task 獨立 pass 唔代表合併後 pass

---

## 對各 Agent 嘅建議

### Generator
- 後續 Task 注意：系統訊息嘅 sender 會係 content 本身
- 後續 Task 注意：confidence 計算要 round
- 唔需要做任何嘢（已修正）

### Evaluator
- 評估 parser 時，確認系統訊息格式有被 test 覆蓋
- 評估 confidence 計算時，加入 boundary value test（exact 1.0 case）
- 未來建議加 "integration readiness" 檢查項
- 唔需要做任何嘢（已修正）

---

## 測試結果
- 修正前：40 passed, 5 failed
- 修正後：45 passed, 0 failed (0.61s)
