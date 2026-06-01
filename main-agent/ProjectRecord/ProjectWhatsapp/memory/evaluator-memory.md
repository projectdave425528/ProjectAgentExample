# Evaluator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | Verdict | 主要問題 |
|---|------|---------|---------|----------|
| 1 | 2026-05-30 | Task 10: CLI 入口 + 主流程串接（14 CLI tests + 254 total pass） | PASS (88) | `config` 參數缺 type hint；bare `list` 缺 element type；Pipeline 設計清晰，錯誤處理完善 |
| 2 | 2026-05-31 | Task 11: 端到端整合測試（6 E2E tests） | PASS (88) | Happy Path 重複 pipeline 執行；column index magic number；整體覆蓋度優秀 |
| 3 | 2026-05-31 | Task 12: 文檔 + README（內容審查） | PASS (92) | 全部 section 齊全；FAQ 6 個；Tesseract 安裝指南完整；建議加 macOS/Linux 提示 |

## 項目標準
- Python 3.9+、Pydantic v2、pytest
- Config 優先順序：env vars > yaml > defaults
- TransactionRecord 用 `transaction_date`（唔係 `date`）— Pydantic v2 type annotation 衝突
- 所有 model validators 必須覆蓋 boundary values（0.0、1.0）
- Test 必須覆蓋 Happy Path + Error Path + Edge Case（Planner Test Criteria）
- Regex patterns 用模組化設計（_DATE_PART、_DATE_SEP 等組件拼接）
- 所有 public functions 必須接受 None/empty 輸入唔 crash
- 函數 < 30 行、參數 ≤ 3（Generator 已遵守）
- Decimal 用於金額計算（避免 floating point 問題）

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
- **group_by_time_window 45 行（含 15 行 docstring）** — 實際邏輯約 30 行（borderline）。建議提取 `_should_merge()` helper 但唔影響 PASS。連續兩個 Task 都有 borderline 行數問題，Generator 應注意
- **Duck typing 用於跨模組接口** — `extract_from_matched_pair(pair)` 冇 type hint，依賴 duck typing。雖然 test 用 MagicMock 可以 pass，但日後 refactor 時缺少 type checker 保護。建議用 Protocol 或 string annotation
- **Decimal 用於金額** — 正確避免 floating point 問題。`_calculate_confidence` 用 float 但只做加法且 round(2)，0.3+0.35+0.35=1.0 在 float 下精確（已有 test 驗證）
- **Dead code path 識別** — `_extract_chinese_amount` 嘅 `f"{text}蚊"` 永遠唔會觸發（因為 `text in content` 已經 match 並 return）。唔影響功能但增加維護負擔
- **`__import__()` inline import 係 anti-pattern** — 喺 `_build_unmatched_single` 用 `__import__("datetime").date.today()` 避免 module-level import，但降低可讀性。應該直接用已 import 嘅 type 或加一行 module-level import
- **`id()` 作為 dict key** — 用 object memory address 做 mapping key 喺 function scope 內安全（所有 object alive），但語義唔清晰。用 enumerate index 更直觀
- **Pipeline 設計模式** — record_builder 作為 orchestrator 只負責調度（match → extract → group → resolve → assemble），每個步驟委託專門模組。呢個係好嘅 separation of concerns
- **Unmatched image 處理** — 即使冇 match 到 message，仍然產出 record（flagged needs_review=True）。呢個設計確保唔會遺漏任何付款證據
- **Excel Exporter 模組化設計** — formatters.py 獨立於 Excel 邏輯，可以單獨測試同重用。`__init__.py` 提供乾淨嘅 public API。呢個係好嘅 package 設計 pattern
- **openpyxl ws 參數 duck typing** — openpyxl 嘅 type stubs 唔完整，所以 `ws` 參數用 duck typing 係合理嘅 trade-off。但建議至少加 `# type: ignore` 或 `Worksheet` annotation
- **format_amount 返回 str 寫入 Excel** — 總計行用 string 格式，唔支援 Excel 內計算。作為報表匯出用途可接受，但如果需要 Excel formula 功能就要改為 numeric type
- **CLI 入口 Click pattern** — `@click.group()` + `@cli.command()` 係標準做法。Click options 數量唔受「參數 ≤ 3」限制（framework constraint）。Helper functions 正確保持 ≤ 3 params
- **Lazy import for optional dependencies** — `_run_ocr_analysis` 內 import `OcrAnalyzer` 係正確做法，避免 Tesseract 未安裝時 CLI 完全無法啟動
- **bare `list` type hint 係 recurring issue** — Task 9 同 Task 10 都有呢個問題。Generator 應統一用 generic type（`list[T]`）而唔係 bare `list`
- **E2E test 嘅 class-level fixture 優化** — Happy Path 3 個 test 重複執行相同 pipeline，可以用 `@pytest.fixture(scope="class")` 或 session fixture 減少重複。但唔影響正確性
- **E2E fixture 設計** — sample_chat.txt 包含多種金額格式（$500、三百蚊、$1,200）係好嘅做法，測試 parser 嘅多格式支援
- **文檔評估要點** — README 必須有：簡介、功能列表、安裝步驟、快速開始、項目結構。usage.md 必須有：CLI 參數表、配置選項、輸出格式、安裝指南、FAQ（≥5 個）。語言一致性同技術準確性係重點
