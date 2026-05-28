# Evaluator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | Verdict | 主要問題 |
|---|------|---------|---------|----------|
| 1 | 2026-05-28 | Task 1: 項目初始化 + Data Models（54 tests） | PASS (88) | 無 critical issue；建議加 JSON round-trip test、更新 Design Spec 嘅 date→transaction_date |
| 2 | 2026-05-28 | Task 2: Regex Patterns + Utils（105 tests） | PASS (85) | split_sender_content 重複定義（patterns.py + utils.py）；_try_date_format 參數過多；日期順序嘗試邏輯缺文檔 |
| 3 | 2026-05-28 | Task 3: Text Parser 主解析邏輯（28 tests） | PASS (90) | _build_message 剛好 30 行（borderline）；pending state 用 dict 缺 type safety |

## 項目標準
- Python 3.9+、Pydantic v2、pytest
- Config 優先順序：env vars > yaml > defaults
- TransactionRecord 用 `transaction_date`（唔係 `date`）— Pydantic v2 type annotation 衝突
- 所有 model validators 必須覆蓋 boundary values（0.0、1.0）
- Test 必須覆蓋 Happy Path + Error Path + Edge Case（Planner Test Criteria）
- Regex patterns 用模組化設計（_DATE_PART、_DATE_SEP 等組件拼接）
- 所有 public functions 必須接受 None/empty 輸入唔 crash
- 函數 < 30 行、參數 ≤ 3（Generator 已遵守）

## 評估經驗
- Pydantic v2 field name 唔可以同 type annotation 同名（date: date 會衝突）— Generator 嘅改名決策合理
- Config loader 用 env mapping dict 係常見 pattern，但日後加 field 要記得同步
- conftest.py fixtures 提供 reusable test data，品質好
- 54 tests 對於 4 個 model + 1 個 config loader 嚟講覆蓋度足夠
- split_sender_content 重複定義係 Generator 已知嘅 tech debt，承諾 Task 3 統一
- parse_timestamp 嘅日期順序嘗試邏輯（YYYY/MM/DD → DD/MM/YYYY → MM/DD/YYYY）對歧義日期會偏向 DD/MM/YYYY — 呢個係合理嘅 design decision（歐洲/亞洲格式優先）
- 105 tests 對於 2 個 module（patterns.py + utils.py）嚟講覆蓋度充足
- Internal helpers 被直接 import 測試 — 對 utility module 可以接受，但唔建議對 business logic 咁做
- Pending State Pattern 係處理多行訊息嘅好方法 — 用 dict 追蹤當前未完成訊息，遇到新 timestamp 時 flush
- `for line in f` 逐行迭代係處理大文件嘅正確做法 — 唔會一次載入整個文件
- Encoding detection 用 try-read-1024-bytes 方法有局限性（前 1024 bytes valid 唔代表全文件 valid），但 latin-1 fallback 兜底足夠
- 28 tests 對於 1 個 module（text_parser.py，13 functions）嚟講覆蓋度充足
- AST 計算嘅函數行數包含 docstring — 評估時要區分「含 docstring 嘅總行數」同「實際邏輯行數」
- Task 3 成功解決 Task 2 嘅 split_sender_content 重複問題（直接用 match_message_line 返回 tuple）
