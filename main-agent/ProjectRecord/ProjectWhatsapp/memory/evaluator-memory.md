# Evaluator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | Verdict | 主要問題 |
|---|------|---------|---------|----------|
| 1 | 2026-05-28 | Task 3: Text Parser 主解析邏輯（28 tests） | PASS (90) | _build_message 剛好 30 行（borderline）；pending state 用 dict 缺 type safety |
| 2 | 2026-05-28 | Task 4: Image Analyzer Base + OCR（首次評估） | FAIL (72) | Test import 路徑錯誤；OCR test mock 目標唔匹配 lazy import；extract_amounts 唔支援多金額/去重 |
| 3 | 2026-05-28 | Task 4: Image Analyzer Base + OCR（修改後重評） | PASS (88) | 5 個問題全部解決；_parse_amount 重複定義（minor）；module-level import trade-off 可接受 |
| 4 | 2026-05-30 | Task 6: Transaction Record Builder 配對邏輯（17 tests） | PASS (85) | match_images_to_messages 邏輯行數 36（超 30 行 borderline）；重複 filename image_results 會產生重複 pair |

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
- **Lazy import pattern（喺 function 入面 import）會導致 module-level mock 失效** — test 必須 patch 原始 module（如 `pytesseract.image_to_string`）或者將 import 移到 module level
- **Convenience wrapper functions 應該放喺對應嘅模組** — 唔好放喺另一個模組然後 test import 原始模組，會造成 ImportError
- **Test 同 source 嘅 interface 一致性** — 寫 test 前要確認 import path 同 function signature 正確
- **FAIL → 修改 → 重評流程有效** — Generator 按方案 A 修改後全部問題解決，證明具體修改建議（含代碼範例）對 Generator 最有幫助
- **Module-level convenience function + class API 並存** — 好嘅設計 pattern，但要注意 helper function 唔好重複定義（DRY）
- **finditer + set 去重** — 處理多 pattern 多 match 嘅標準做法，保持 insertion order
- **Integration gap 係盲點** — 各 Task 獨立評估時 PASS，但合併後暴露 3 個問題：(1) 系統訊息冇 `: ` 被跳過 (2) floating point 0.3+0.35+0.35≠1.0 (3) text_parser 未處理 empty sender
- **系統訊息格式要特別注意** — WhatsApp 系統訊息冇 sender: content 結構，只有 [timestamp] description。評估 parser 時要確認呢類格式有被 test 覆蓋
- **Confidence 計算嘅 boundary value** — 要測試 exact 1.0 case（所有 component 都有時），floating point 加法可能唔等於預期值
- **未來建議**：評估時加一個 "integration readiness" 檢查項 — 確認 module 嘅 public API 同其他 module 嘅 import 一致
- **Matcher 模組嘅 index-based 配對策略** — 用 dict[str, ParsedMessage] 做 O(1) lookup 係正確做法，但要注意 index 只保留第一次出現嘅 message
- **函數行數 borderline 判斷** — 36 行含 6 行空行分隔，實際 statement 約 30 行。已做合理 delegation（3 個 helpers），進一步拆分反而降低可讀性。作為建議記錄但唔影響 PASS
- **重複 filename 嘅 image_results** — 當前實現允許多個同名 image 配對到同一 message。實際場景中每個 image file 應有唯一 filename，但 Task 7/8 整合時要注意呢個行為
