# Generator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | 結果 | 學到咩 |
|---|------|---------|------|--------|
| 1 | 2026-05-28 | Task 3: WhatsApp Text Parser — 主解析邏輯 | completed (28 tests, syntax verified) | Pending State Pattern 適合逐行解析多行訊息；encoding detection 用 try-read-1024-bytes 方式比 chardet 更輕量；逐行 `for line in f` 天然支援大文件 |
| 2 | 2026-05-28 | Task 4: Image Analyzer（初版） | FAIL (evaluator 72分) | Test import 路徑同 source 唔一致；lazy import 令 mock patch 唔生效；convenience function 要放喺對應模組而非 ocr_analyzer |
| 3 | 2026-05-28 | Task 4: Image Analyzer（修正版 A010） | completed | 加 module-level convenience functions；移除 lazy import；extract_amounts 支援多金額 + 去重 |
| 4 | 2026-05-30 | Task 6: Transaction Record Builder — 配對邏輯 | completed (17 tests pass, 62 total) | 用 dict index 做 O(1) filename lookup；case-insensitive 用 .lower() key；needs_review 由 error 或 flag 決定；unmatched attachments 保留原始大小寫 |

## 項目知識
- 技術棧：Python 3.14、Pydantic 2.13.4、pytest 9.0.3
- TransactionRecord 用 `transaction_date` 而非 `date`（避免 Pydantic type annotation 衝突）
- Config loader 優先順序：env vars > yaml > defaults
- 所有 confidence field 有 0.0-1.0 validator
- 必填 str fields 用 `min_length=1` 確保唔為空
- MESSAGE_PATTERN 支援：24h/12h 時間、YYYY/MM/DD + DD/MM/YYYY + MM/DD/YYYY 日期順序、/ - . 分隔符
- `split_sender_content` 用第一個 `: ` 分割 — sender 含冒號時正確處理
- 系統訊息偵測用 keyword list（中英文），用 `in` 運算符匹配
- pytest-cov 未安裝喺當前環境
- text_parser.py 用 Pending State Pattern：dict 追蹤當前訊息，遇到新 match 時 flush
- encoding detection 順序：utf-8 → utf-8-sig → latin-1（讀 1024 bytes 測試）
- 空文件用 `path.stat().st_size == 0` 快速判斷
- **Builder module 結構**：`src/builder/` 包含 matcher.py（配對）、未來會有 extractor.py（提取）同 record_builder.py（整合）
- **MatchedPair model**：message + image_result + needs_review（Pydantic BaseModel）
- **MatchResult model**：matched_pairs + unmatched_images + unmatched_attachments
- **配對策略**：用 dict[lowercase_filename → first_message] 做 O(1) lookup，同一 filename 只配第一次出現

## 常見錯誤
- Pydantic v2 field name 唔可以同 type annotation 同名（例如 `date: date` 會報 `unevaluable-type-annotation`）
- 舊版 conftest.py 可能有 encoding 問題，需要重寫
- `__pycache__` 同名目錄會導致 pytest import mismatch，要清理
- `split_sender_content` 同時存在於 patterns.py 同 utils.py — 後續 Task 應統一到一個位置
- 逐行讀取時要注意 `\n\r` strip — 用 `rstrip("\n\r")` 而非 `strip()` 避免刪除有意義嘅前導空格
- **Test import 路徑必須同 source 一致** — 如果 test import `from src.analyzer.amount_extractor import extract_amounts`，source 必須有呢個 function
- **Lazy import 會令 module-level mock patch 失效** — 如果 test 用 `@patch("src.module.dependency")`，dependency 必須係 module-level import
- **Convenience function 放喺對應模組** — `extract_amounts` 放 `amount_extractor.py`，唔好放 `ocr_analyzer.py`
- **系統訊息冇 `: ` 分隔符** — `match_message_line` 要處理呢個情況，返回 (ts, "", content) 而唔係 None
- **Floating point 加法要 round** — `0.3 + 0.35 + 0.35 ≠ 1.0`，confidence 計算用 `round(score, 2)`
- **Integration test 會暴露單元測試搵唔到嘅問題** — 各 Task 獨立 pass 唔代表合併後 pass
- **Case-insensitive matching 用 .lower()** — 唔好用 .casefold()（對 ASCII filenames 冇分別但更簡單）
