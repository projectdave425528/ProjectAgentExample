# Generator Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | 結果 | 學到咩 |
|---|------|---------|------|--------|
| 1 | 2026-05-30 | Task 8: Record Builder 主整合邏輯 | completed (34 tests pass, 165 total) | 用 id(extraction) 做 pair_map key 避免 hashable 問題；unmatched images 都要產出 record（標記 needs_review）；JSON round-trip 用 model_dump(mode="json") 確保 Decimal/date 正確序列化 |
| 2 | 2026-05-30 | Task 9: Excel Exporter | completed (43 tests pass, 208 total) | openpyxl 寫入空字串讀回為 None；金額用 format_amount 轉 str 寫入避免 Decimal 序列化問題；欄寬自動調整用 min/max 限制；ExportError 自定義 exception 比 generic 更清晰 |
| 3 | 2026-05-30 | Task 10: CLI 入口 + 主流程串接 | completed (20 tests pass, 260 total) | Click CLI 用 lazy import 處理 optional dependencies（OcrAnalyzer）；CliRunner 測試唔需要真實文件系統；builtins.__import__ patch 可以模擬 ImportError；中間結果保存用 records_to_json() 直接寫入 |
| 4 | 2026-05-31 | Task 11: 端到端整合測試 | completed (6 tests pass, 266 total) | Excel summary row 用 "總計" 唔係 "合計"；attachment message 同 amount message 係分開嘅（matcher 配對 attachment msg）；金額格式化為 "X.00" 字串；empty records 仍產出 header + summary row |

## 項目知識
- 技術棧：Python 3.14、Pydantic 2.13.4、pytest 9.0.3、openpyxl 3.1.5、Click
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
- **Builder module 結構**：`src/builder/` 包含 matcher.py（配對）、extractor.py（提取）、status_resolver.py（狀態判斷）、record_builder.py（整合）
- **Exporter module 結構**：`src/exporter/` 包含 excel_exporter.py（主匯出）、formatters.py（欄位格式化）
- **MatchedPair model**：message + image_result + needs_review（Pydantic BaseModel）
- **MatchResult model**：matched_pairs + unmatched_images + unmatched_attachments
- **配對策略**：用 dict[lowercase_filename → first_message] 做 O(1) lookup，同一 filename 只配第一次出現
- **ExtractionResult 中間結構**：customer_name + repair_item + quoted_amount + quantity + timestamp + confidence
- **時間窗口分組**：同一客戶 2 小時內相同金額歸為一組，唔同金額分為唔同 record
- **付款狀態判斷**：±1% tolerance、overpaid = paid、no quoted but received = paid
- **廣東話金額**：用 CHINESE_AMOUNTS dict（一百~五千）+ 蚊/元 suffix
- **廣東話數量**：用 CHINESE_DIGITS dict + 部/台/隻/個 unit
- **RecordBuilder 整合流程**：match → extract → group → resolve status → assemble
- **pair_map 用 id(extraction) 做 key**：因為 ExtractionResult 唔係 hashable，用 Python object id 做 dict key
- **Unmatched images 處理**：產出 needs_review=True 嘅 record，customer_name="Unknown"
- **JSON 序列化**：用 model_dump(mode="json") 確保 Decimal 轉 str、date 轉 ISO format
- **Excel 匯出**：金額用 format_amount 轉 str 寫入；openpyxl 空字串讀回為 None；欄寬 min 10 max 30
- **Excel summary row 用 "總計"**：唔係 "合計"，helper function 要用 "總計" 偵測
- **Excel 金額格式**：format_amount 輸出 "X.00" 格式（例如 "500.00"、"1200.00"）
- **Empty records → Excel 仍有 header + summary row**：max_row=2，data_rows=0
- **CLI 架構**：Click group + analyze command；lazy import OcrAnalyzer 避免 Tesseract 未安裝時 crash
- **CLI 測試**：CliRunner + mock 所有外部模組；builtins.__import__ patch 模擬 ImportError
- **中間結果**：records_to_json() 寫入 output 同目錄嘅 intermediate/records.json
- **E2E 測試策略**：真正調用 parse_chat_file + build_records + export_to_excel，只 mock ImageAnalysisResult
- **Attachment message 配對**：matcher 配對嘅係含 `<attached:>` 嘅 message，唔係含金額嘅 message

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
- **中文 regex 唔穩定** — 中文數字/金額用 dict lookup 比 regex 更可靠、更易維護
- **Duck typing for testability** — `extract_from_matched_pair` 接受任何有 message.sender/content/timestamp 嘅 object，方便 MagicMock 測試
- **Test 中嘅 float 計算要先驗證** — (0.85+0.76)/2 = 0.805 rounds to 0.8 唔係 0.81，寫 test 前用 Python 確認
- **openpyxl 空字串行為** — 寫入 "" 到 cell 後讀回為 None，test assertion 要用 helper function 處理
- **Lazy import 測試要用 builtins.__import__ patch** — 唔可以 patch module-level attribute（因為 attribute 唔存在），要 patch import 機制本身
- **E2E test helper 要用實際 Excel 內容驗證** — 先用 debug script 確認實際 Excel 結構再寫 assertion
- **Excel summary row 偵測用 "總計"** — 唔好假設用 "合計"，要先確認 excel_exporter.py 嘅實際寫法
