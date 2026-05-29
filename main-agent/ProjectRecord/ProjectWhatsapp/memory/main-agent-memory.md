# Main Agent Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | 結果 | 備註 |
|---|------|---------|------|------|
| 1 | 2026-05-28 | Specs 全部重寫（Planner） | completed | 12 Tasks + Test Criteria |
| 2 | 2026-05-28 | Task 1 項目初始化 + Data Models | PASS (88/100) | TransactionRecord.date → transaction_date |
| 3 | 2026-05-28 | Task 2 Regex Patterns | PASS (85/100) | 105 tests |
| 4 | 2026-05-28 | Task 3 Text Parser 主邏輯 | PASS (90/100) | 28 tests |
| 5 | 2026-05-28 | Task 4 Image Analyzer OCR | FAIL→PASS (88/100) | 首次 FAIL 因 test import 錯誤，修改後 PASS |

## 調度經驗
- invoke_sub_agent 方法可用，kiro-cli 未測試
- Generator FAIL 後按 Evaluator 建議修改，一次就 PASS — 具體修改建議（含代碼範例）最有效
- SearchIndex encoding 問題需要手動修復（中文亂碼）
- **Integration gap 係常見問題** — 各 Task 獨立 PASS 唔代表合併後冇問題
- **系統訊息格式同普通訊息唔同** — 冇 sender: content 結構
- **Floating point 加法要 round** — 特別係 confidence 計算
- **Main Agent 自己做嘅操作都要寫 checkpoint** — 唔好因為唔係正式 assignment 就跳過

## 項目知識
- 技術棧：Python 3.9+、Pydantic v2、Click、openpyxl、pytesseract、OpenAI Vision API
- 架構：Pipeline（TextParser → ImageAnalyzer → RecordBuilder → ExcelExporter）
- TransactionRecord.date 改名為 transaction_date（Pydantic v2 兼容）
- Config loader 優先順序：env vars > yaml > defaults
- test-env/ 係合併測試環境（Task 1-4 所有代碼），45 tests all pass
- 系統訊息嘅 sender 會係 content 本身（因為冇 `: ` 分隔符）
- confidence 計算用 round(score, 2) 避免 floating point 問題
