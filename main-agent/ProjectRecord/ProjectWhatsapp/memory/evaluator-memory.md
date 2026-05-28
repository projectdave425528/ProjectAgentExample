# Evaluator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | Verdict | 主要問題 |
|---|------|---------|---------|----------|
| 1 | 2026-05-28 | Task 1: 項目初始化 + Data Models（54 tests） | PASS (88) | 無 critical issue；建議加 JSON round-trip test、更新 Design Spec 嘅 date→transaction_date |

## 項目標準
- Python 3.9+、Pydantic v2、pytest
- Config 優先順序：env vars > yaml > defaults
- TransactionRecord 用 `transaction_date`（唔係 `date`）— Pydantic v2 type annotation 衝突
- 所有 model validators 必須覆蓋 boundary values（0.0、1.0）
- Test 必須覆蓋 Happy Path + Error Path + Edge Case（Planner Test Criteria）

## 評估經驗
- Pydantic v2 field name 唔可以同 type annotation 同名（date: date 會衝突）— Generator 嘅改名決策合理
- Config loader 用 env mapping dict 係常見 pattern，但日後加 field 要記得同步
- conftest.py fixtures 提供 reusable test data，品質好
- 54 tests 對於 4 個 model + 1 個 config loader 嚟講覆蓋度足夠
