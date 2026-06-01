# Assignment 016

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-30T11:11:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 7: Transaction Record Builder — 交易資訊提取
- **TaskID**: ProjectWhatsapp/Task-7
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 7 代碼（extractor.py + status_resolver.py）。執行 unit tests 並驗證結果。

## Context
- 代碼位置：`ProjectRecord/ProjectWhatsapp/output/assignment-015/`
  - `src/builder/extractor.py` — 交易資訊提取模組
  - `src/builder/status_resolver.py` — 付款狀態判斷模組
  - `tests/test_builder/test_extractor.py` — extractor 單元測試（46 tests）
  - `tests/test_builder/test_status_resolver.py` — status_resolver 單元測試（23 tests）
- Generator 回覆：`ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-015-reply-completed.md`
- 依賴嘅已完成模組：
  - `test-env/src/builder/matcher.py` — MatchedPair、MatchResult
  - `test-env/src/models/message.py` — ParsedMessage
  - `test-env/src/models/image_result.py` — ImageAnalysisResult
  - `test-env/src/models/transaction.py` — TransactionRecord

## 驗證標準
- [ ] `extractor.py` 實現交易資訊提取
- [ ] 客戶名稱從 sender 欄位提取（空字串 → "Unknown"）
- [ ] 維修項目用關鍵字匹配（換屏、換電池、維修、整機等）
- [ ] 數量提取：支援「3部」「x2」「×3」「2台」「兩部」等格式，預設為 1
- [ ] 報價金額用 regex 從對話提取（$xxx、xxx蚊、xxx元）— 為單價
- [ ] 支援廣東話金額表達（「三百」「五百蚊」等）
- [ ] `status_resolver.py` 判斷付款狀態（比較 報價×數量 vs 實收）
- [ ] 處理一個客戶多次交易（按時間窗口分組）
- [ ] Unit tests 覆蓋 Happy Path / Error Path / Edge Case
- [ ] 所有 test pass
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] 代碼有 type hints 同 docstrings

## Test Criteria（從 specs 複製）
- **Happy Path**: 對話含 "換屏 $500" 時正確提取 repair_item="換屏", quoted_amount=500, quantity=1；對話含 "換屏 x3 $500" 時 quantity=3；sender="陳大文" 時 customer_name="陳大文"；報價500×2=1000 實收1000時 status="paid"
- **Error Path**: 對話完全無金額相關內容時 quoted_amount=None 且唔 crash；sender 為空字串時 customer_name 設為 "Unknown"
- **Edge Case**: 廣東話 "三百蚊" 正確轉換為 300；廣東話 "兩部" 正確轉換為 quantity=2；同一客戶 2 小時內有 2 筆唔同金額交易時分為 2 個 record；報價500×2=1000 實收700時 status="partial"

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
