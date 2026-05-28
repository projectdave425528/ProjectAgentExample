# Generator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | 結果 | 學到咩 |
|---|------|---------|------|--------|
| 1 | 2026-05-28 | Task 1: 項目初始化 + Data Models | completed (54 tests pass) | Pydantic v2.13+ 唔允許 field name 同 imported type 同名（`date` field 要改名為 `transaction_date`）；用 `DateType` alias import 解決 |

## 項目知識
- 技術棧：Python 3.14、Pydantic 2.13.4、pytest 9.0.3
- TransactionRecord 用 `transaction_date` 而非 `date`（避免 Pydantic type annotation 衝突）
- Config loader 優先順序：env vars > yaml > defaults
- 所有 confidence field 有 0.0-1.0 validator
- 必填 str fields 用 `min_length=1` 確保唔為空

## 常見錯誤
- Pydantic v2 field name 唔可以同 type annotation 同名（例如 `date: date` 會報 `unevaluable-type-annotation`）
- 舊版 conftest.py 可能有 encoding 問題，需要重寫
- `__pycache__` 同名目錄會導致 pytest import mismatch，要清理
