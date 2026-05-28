# Generator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | 結果 | 學到咩 |
|---|------|---------|------|--------|
| 1 | 2026-05-28 | Task 1: 項目初始化 + Data Models | completed (54 tests pass) | Pydantic v2.13+ 唔允許 field name 同 imported type 同名（`date` field 要改名為 `transaction_date`）；用 `DateType` alias import 解決 |
| 2 | 2026-05-28 | Task 2: WhatsApp Text Parser — Regex Patterns | completed (105 tests pass) | 用第一個 `: ` 作為 sender/content 分隔符處理 sender 含冒號情況；parse_timestamp 嘗試 3 種日期順序（YYYY/MM/DD → DD/MM/YYYY → MM/DD/YYYY）；系統訊息用 keyword-in-content 偵測 |
| 3 | 2026-05-28 | Task 3: WhatsApp Text Parser — 主解析邏輯 | completed (28 tests, syntax verified) | Pending State Pattern 適合逐行解析多行訊息；encoding detection 用 try-read-1024-bytes 方式比 chardet 更輕量；逐行 `for line in f` 天然支援大文件 |

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

## 常見錯誤
- Pydantic v2 field name 唔可以同 type annotation 同名（例如 `date: date` 會報 `unevaluable-type-annotation`）
- 舊版 conftest.py 可能有 encoding 問題，需要重寫
- `__pycache__` 同名目錄會導致 pytest import mismatch，要清理
- `split_sender_content` 同時存在於 patterns.py 同 utils.py — 後續 Task 應統一到一個位置
- 逐行讀取時要注意 `\n\r` strip — 用 `rstrip("\n\r")` 而非 `strip()` 避免刪除有意義嘅前導空格
