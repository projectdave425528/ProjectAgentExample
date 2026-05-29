# Tasks: WhatsApp 帳目分析系統

## Task List

### Task 1: 項目初始化 + Data Models
- **Status**: completed
- **Required**: yes
- **Depends on**: none

**Description**: 建立項目結構、安裝依賴、定義所有 Pydantic data models（ParsedMessage、ImageAnalysisResult、TransactionRecord、AppConfig）。建立 config 載入機制（.env + config.yaml）。

**Input**: Design spec 中嘅 Data Model 定義
**Output**: 完整項目目錄結構 + 所有 Pydantic model 文件 + 配置載入模組

**Expected Outcome**:
- [ ] 項目目錄結構已建立（src/、tests/、docs/）
- [ ] requirements.txt 包含所有核心依賴（pinned versions）
- [ ] src/models/ 下所有 data model 已定義
- [ ] Pydantic model 有正確嘅 type hints 同 validators
- [ ] src/config.py 可以載入 .env 同 config.yaml
- [ ] .env.example 已建立（包含 API Key placeholder）
- [ ] config.yaml 有合理嘅預設值
- [ ] pytest 可以成功 import 所有 models

**Test Criteria**:
- **Happy Path**: 建立 ParsedMessage 實例所有欄位正確賦值同序列化為 JSON；AppConfig 從有效 config.yaml 載入所有欄位值正確；TransactionRecord UUID 自動生成且唯一
- **Error Path**: ParsedMessage 缺少必填欄位時 raise ValidationError；AppConfig 載入唔存在嘅 yaml 時用預設值；ImageAnalysisResult confidence 超出 0-1 範圍時 raise ValidationError
- **Edge Case**: sender 包含 emoji/特殊字符時正確保存；amount 為 Decimal("0.00") 時正確處理；tesseract_path 為 None 時正常運作

**Output Files**:
- `src/__init__.py`, `src/models/__init__.py`, `src/models/message.py`, `src/models/image_result.py`
- `src/models/transaction.py`, `src/models/config.py`, `src/config.py`
- `requirements.txt`, `.env.example`, `config.yaml`, `setup.py`

---

### Task 2: WhatsApp Text Parser — Regex Patterns
- **Status**: completed
- **Required**: yes
- **Depends on**: Task 1

**Description**: 實現 WhatsApp 對話文件嘅 regex patterns，支援多種時間格式（12/24小時制、唔同日期順序）。定義 pattern 常量同 utility functions。

**Input**: WhatsApp .txt 匯出文件嘅各種格式範例
**Output**: Regex pattern 常量 + 時間格式轉換 utility functions

**Expected Outcome**:
- [ ] 定義主訊息 regex pattern：`[YYYY/MM/DD, HH:MM:SS] Sender: Message`
- [ ] 支援 24 小時制同 12 小時制（AM/PM）格式
- [ ] 支援日期順序變體（YYYY/MM/DD、DD/MM/YYYY、MM/DD/YYYY）
- [ ] 支援日期分隔符變體（/、-、.）
- [ ] 定義系統訊息識別 patterns
- [ ] 定義 `<attached:filename>` 提取 pattern
- [ ] 所有 patterns 有對應嘅單元測試，覆蓋率 > 90%

**Test Criteria**:
- **Happy Path**: 標準格式 `[2024/01/15, 14:30:00] John: Hello` 正確匹配並提取 timestamp/sender/content；12小時制 `[1/15/24, 2:30 PM] John: Hi` 正確解析
- **Error Path**: 完全唔符合任何 pattern 嘅行返回 None/不匹配；空字串輸入唔 crash
- **Edge Case**: sender 名稱含冒號（如 `Dr. Wong: 醫生`）時正確分割；日期 `31/02/2024`（無效日期）時 pattern 匹配但後續 datetime 轉換失敗處理

**Output Files**:
- `src/parser/__init__.py`, `src/parser/patterns.py`, `src/parser/utils.py`
- `tests/test_parser/__init__.py`, `tests/test_parser/test_patterns.py`

---

### Task 3: WhatsApp Text Parser — 主解析邏輯
- **Status**: completed
- **Required**: yes
- **Depends on**: Task 2

**Description**: 實現完整嘅 .txt 文件解析器。逐行讀取文件，用 regex 解析每條訊息，處理多行訊息、系統訊息、media attachments。輸出 ParsedMessage 列表。

**Input**: WhatsApp .txt 匯出文件路徑 (str)
**Output**: list[ParsedMessage]

**Expected Outcome**:
- [ ] `text_parser.py` 實現 `parse_chat_file(file_path: str) -> list[ParsedMessage]`
- [ ] 正確處理多行訊息（無時間戳嘅行歸屬前一條訊息）
- [ ] 正確識別並標記系統訊息
- [ ] 正確提取 `<attached:filename>` 到 attachments 列表
- [ ] 處理空文件（返回空列表 + warning log）
- [ ] 處理大文件（>10MB，分段讀取唔會 OOM）
- [ ] 自動偵測時間格式（唔需要用戶指定）
- [ ] 無法解析嘅行記錄 warning 並跳過

**Test Criteria**:
- **Happy Path**: 10 條標準格式訊息嘅 .txt 文件正確解析為 10 個 ParsedMessage；含 attachment 嘅訊息正確填充 attachments 列表
- **Error Path**: 文件路徑唔存在時 raise FileNotFoundError 並有清晰錯誤訊息；文件編碼非 UTF-8 時嘗試其他編碼或報錯
- **Edge Case**: 空文件返回空列表；單行超長訊息（>10000字）正確處理；連續多行無時間戳全部歸屬前一條訊息

**Output Files**:
- `src/parser/text_parser.py`
- `tests/test_parser/test_text_parser.py`, `tests/fixtures/sample_chat.txt`

---

### Task 4: Image Analyzer — Base + OCR 模式
- **Status**: completed
- **Required**: yes
- **Depends on**: Task 1

**Description**: 實現圖片分析器嘅 abstract base class 同 Tesseract OCR 模式。包括圖片讀取、OCR 文字提取、金額識別、付款方式偵測。Base class 定義 interface 方便 mock。

**Input**: 圖片文件路徑 (str) + AppConfig
**Output**: ImageAnalysisResult

**Expected Outcome**:
- [ ] `base.py` 定義 `ImageAnalyzerBase` abstract class（含 analyze 方法 signature）
- [ ] `ocr_analyzer.py` 實現 Tesseract OCR 分析（繼承 base class）
- [ ] 支援 JPG、PNG、WEBP 格式讀取
- [ ] `amount_extractor.py` 從 OCR 文字提取金額（支援 $、HK$、千位分隔符）
- [ ] `payment_detector.py` 識別 PayMe/FPS/銀行轉帳截圖
- [ ] 單張圖片分析失敗時返回 error result（唔 raise exception）
- [ ] 信心度計算邏輯（基於 OCR 結果質量）

**Test Criteria**:
- **Happy Path**: mock Tesseract 返回 "HK$500.00 PayMe" 時正確提取 amount=500.00, payment_method="payme"；mock 返回含 FPS 關鍵字文字時識別為 fps
- **Error Path**: 圖片文件唔存在時返回 ImageAnalysisResult(error="無法讀取文件") 而非 raise exception；Tesseract 未安裝時返回明確 error message
- **Edge Case**: 金額含千位分隔符 "$1,000.50" 正確提取為 1000.50；OCR 返回空字串時 confidence=0.0 且 needs_review=True；WEBP 格式圖片正確讀取

**Output Files**:
- `src/analyzer/__init__.py`, `src/analyzer/base.py`, `src/analyzer/ocr_analyzer.py`
- `src/analyzer/amount_extractor.py`, `src/analyzer/payment_detector.py`
- `tests/test_analyzer/__init__.py`, `tests/test_analyzer/test_ocr_analyzer.py`
- `tests/test_analyzer/test_payment_detector.py`, `tests/test_analyzer/test_amount_extractor.py`

---

### Task 5: Image Analyzer — AI Vision 模式
- **Status**: pending
- **Required**: no
- **Depends on**: Task 4

**Description**: 實現 AI Vision API 分析模式。調用 OpenAI Vision API 分析轉帳截圖，提取金額、付款方式、交易日期等資訊。繼承 base class interface。

**Input**: 圖片文件路徑 (str) + AppConfig（含 API Key）
**Output**: ImageAnalysisResult

**Expected Outcome**:
- [ ] `ai_vision.py` 實現 AI Vision 分析器（繼承 ImageAnalyzerBase）
- [ ] 正確構建 API request（image base64 encoding）
- [ ] 設計有效嘅 prompt 提取交易資訊
- [ ] 解析 API response 到 ImageAnalysisResult
- [ ] API 失敗時 graceful fallback（返回 error result）
- [ ] API Key 從環境變數讀取（唔 hardcode）
- [ ] Rate limiting 處理（retry with backoff）

**Test Criteria**:
- **Happy Path**: mock API 返回 {"amount": 500, "method": "payme"} 時正確映射到 ImageAnalysisResult；confidence 基於 API response 正確計算
- **Error Path**: API 返回 401 Unauthorized 時返回 error result 含 "API Key 無效"；API timeout 時 retry 最多 3 次後返回 error result
- **Edge Case**: API 返回空 response 時 needs_review=True；API Key 為 None 時直接返回 error 唔嘗試調用；圖片 >20MB 時壓縮後再發送

**Output Files**:
- `src/analyzer/ai_vision.py`
- `tests/test_analyzer/test_ai_vision.py`

---

### Task 6: Transaction Record Builder — 配對邏輯
- **Status**: completed
- **Required**: yes
- **Depends on**: Task 3, Task 4

**Description**: 實現圖片同對話嘅配對邏輯。透過 `<attached:filename>` 引用同時間戳，將 ImageAnalysisResult 同對應嘅 ParsedMessage context 配對。

**Input**: list[ParsedMessage] + list[ImageAnalysisResult]
**Output**: list[MatchedPair]（含未配對列表）

**Expected Outcome**:
- [ ] `matcher.py` 實現 `match_images_to_messages(messages, image_results) -> MatchResult`
- [ ] 透過 attachment filename 精確配對
- [ ] 配對失敗時記錄 warning（唔中斷）
- [ ] 返回未配對嘅圖片列表（供後續處理/人工確認）
- [ ] MatchResult 包含 matched_pairs + unmatched_images + unmatched_attachments

**Test Criteria**:
- **Happy Path**: 3 條含 attachment 嘅 message + 3 個對應 image_result 正確配對為 3 個 MatchedPair；配對後 MatchedPair 包含正確嘅 message context
- **Error Path**: image_results 為空列表時返回空 matched_pairs + 所有 attachments 列入 unmatched；messages 為空列表時返回空結果唔 crash
- **Edge Case**: 同一 filename 出現喺多條 message 時只配對第一次出現嘅；image_result 有 error 時仍然配對但標記 needs_review；filename 大小寫唔一致時 case-insensitive 配對

**Output Files**:
- `src/builder/__init__.py`, `src/builder/matcher.py`
- `tests/test_builder/__init__.py`, `tests/test_builder/test_matcher.py`

---

### Task 7: Transaction Record Builder — 交易資訊提取
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 6

**Description**: 從配對好嘅對話 context 中提取交易資訊：客戶名稱、維修項目、報價金額。用關鍵字匹配策略處理廣東話/中文/英文混合內容。同時實現付款狀態判斷邏輯。

**Input**: list[MatchedPair] + list[ParsedMessage]（context window）
**Output**: 提取嘅交易欄位值（customer_name, repair_item, quoted_amount, payment_status）

**Expected Outcome**:
- [ ] `extractor.py` 實現交易資訊提取
- [ ] 客戶名稱從 sender 欄位提取
- [ ] 維修項目用關鍵字匹配（換屏、換電池、維修、整機等）
- [ ] 數量提取：支援「3部」「x2」「×3」「2台」「兩部」等格式，預設為 1
- [ ] 報價金額用 regex 從對話提取（$xxx、xxx蚊、xxx元）— 為單價
- [ ] 支援廣東話金額表達（「三百」「五百蚊」等）
- [ ] `status_resolver.py` 判斷付款狀態（比較 報價×數量 vs 實收）
- [ ] 處理一個客戶多次交易（按時間窗口分組）

**Test Criteria**:
- **Happy Path**: 對話含 "換屏 $500" 時正確提取 repair_item="換屏", quoted_amount=500, quantity=1；對話含 "換屏 x3 $500" 時 quantity=3；sender="陳大文" 時 customer_name="陳大文"；報價500×2=1000 實收1000時 status="paid"
- **Error Path**: 對話完全無金額相關內容時 quoted_amount=None 且唔 crash；sender 為空字串時 customer_name 設為 "Unknown"
- **Edge Case**: 廣東話 "三百蚊" 正確轉換為 300；廣東話 "兩部" 正確轉換為 quantity=2；同一客戶 2 小時內有 2 筆唔同金額交易時分為 2 個 record；報價500×2=1000 實收700時 status="partial"

**Output Files**:
- `src/builder/extractor.py`, `src/builder/status_resolver.py`
- `tests/test_builder/test_extractor.py`, `tests/test_builder/test_status_resolver.py`

---

### Task 8: Transaction Record Builder — 主整合邏輯
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 7

**Description**: 實現 RecordBuilder 主邏輯，結合 matcher + extractor + status_resolver，產出完整嘅 TransactionRecord 列表。輸出結構化 JSON 中間結果。

**Input**: list[ParsedMessage] + list[ImageAnalysisResult]
**Output**: list[TransactionRecord] + JSON 中間結果文件

**Expected Outcome**:
- [ ] `record_builder.py` 實現 `build_records(messages, image_results) -> list[TransactionRecord]`
- [ ] 正確調用 matcher → extractor → status_resolver 流程
- [ ] 產出嘅 TransactionRecord 包含所有必要欄位
- [ ] 支援將結果序列化為 JSON（中間結果保存）
- [ ] 整體信心度計算（綜合各步驟信心度）
- [ ] 標記需要人工確認嘅紀錄（confidence < threshold）

**Test Criteria**:
- **Happy Path**: 5 條 message + 3 個 image_result 正確產出對應數量嘅 TransactionRecord；JSON 序列化後可以反序列化回 list[TransactionRecord]
- **Error Path**: messages 同 image_results 都為空時返回空列表唔 crash；matcher 返回全部 unmatched 時仍產出 record（標記 needs_review）
- **Edge Case**: 單個 message 關聯多張圖片時正確處理；所有 record 嘅 confidence < threshold 時全部標記 needs_review；TransactionRecord.id 全局唯一

**Output Files**:
- `src/builder/record_builder.py`
- `tests/test_builder/test_record_builder.py`

---

### Task 9: Excel Exporter
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 8

**Description**: 實現 Excel 匯出功能。將 TransactionRecord 列表寫入 .xlsx 文件，包含所有欄位、排序、格式化、自動計算總額。

**Input**: list[TransactionRecord] + output_path (str) + sort_by (str)
**Output**: .xlsx 文件

**Expected Outcome**:
- [ ] `excel_exporter.py` 實現 `export_to_excel(records, output_path, sort_by="date")`
- [ ] 包含欄位：日期、客戶名稱、維修項目、數量、報價金額（單價）、實收金額、付款方式、付款狀態、備註
- [ ] 支援按日期排序（預設）同按客戶名稱排序
- [ ] 最後一行自動計算報價總額同實收總額
- [ ] 欄位格式化（日期格式、金額格式、欄寬自動調整）
- [ ] 表頭有格式（粗體、背景色）
- [ ] `formatters.py` 處理欄位顯示格式

**Test Criteria**:
- **Happy Path**: 3 個 TransactionRecord 匯出後用 openpyxl 讀取驗證有 3 行數據 + 1 行表頭 + 1 行總計；金額欄位值正確；排序正確
- **Error Path**: output_path 目錄唔存在時 raise 明確錯誤（唔係 generic OSError）；records 為空列表時產出只有表頭嘅 Excel（唔 crash）
- **Edge Case**: 客戶名稱含 emoji 時 Excel 正確顯示；金額為 None 時欄位顯示為空（唔係 "None"）；100+ records 時效能 < 3 秒

**Output Files**:
- `src/exporter/__init__.py`, `src/exporter/excel_exporter.py`, `src/exporter/formatters.py`
- `tests/test_exporter/__init__.py`, `tests/test_exporter/test_excel_exporter.py`

---

### Task 10: CLI 入口 + 主流程串接
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 9

**Description**: 實現 CLI 入口點，用 Click 框架。串接所有模組成完整 pipeline。提供進度提示、錯誤訊息中文化、中間結果保存。

**Input**: CLI 參數（--input, --output, --mode, --config, --verbose）
**Output**: .xlsx 報表文件 + 中間結果 JSON

**Expected Outcome**:
- [ ] `main.py` 用 Click 實現 CLI
- [ ] 命令：`python -m src.main analyze --input <folder> --output <file> --mode <ocr|ai_vision>`
- [ ] 自動偵測輸入資料夾中嘅 .txt 同圖片文件
- [ ] 顯示處理進度（正在解析文字... 正在分析圖片 3/10...）
- [ ] 錯誤訊息全部中文
- [ ] 中間結果保存到 output/intermediate/
- [ ] `--verbose` flag 顯示詳細日誌
- [ ] `--config` flag 指定配置文件路徑

**Test Criteria**:
- **Happy Path**: 用 Click CliRunner 調用 analyze 命令，提供有效 input folder，exit code = 0 且 output 文件存在
- **Error Path**: --input 指向唔存在嘅路徑時 exit code = 1 且錯誤訊息為中文；--mode 為無效值時顯示 usage help
- **Edge Case**: input folder 有 .txt 但無圖片時仍正常運行（只做文字分析）；input folder 有圖片但無 .txt 時顯示警告並終止；--output 路徑含中文字時正確處理

**Output Files**:
- `src/main.py`
- `tests/test_main.py`

---

### Task 11: 端到端整合測試
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 10

**Description**: 建立完整嘅端到端測試。用 sample data 跑完整 pipeline，驗證最終 Excel 輸出正確。包括正常流程同 edge cases。

**Input**: tests/fixtures/ 入面嘅 sample data
**Output**: 測試報告 + 覆蓋率報告

**Expected Outcome**:
- [ ] 建立完整嘅 test fixtures（sample_chat.txt + mock images）
- [ ] 端到端測試：輸入 → 解析 → 分析 → 整合 → 匯出
- [ ] 驗證 Excel 輸出嘅欄位值正確
- [ ] Edge case 測試：空文件、損壞圖片、無交易內容
- [ ] 所有測試 pass
- [ ] 整體覆蓋率 > 80%

**Test Criteria**:
- **Happy Path**: sample_chat.txt（含 5 筆交易）+ 5 張 mock 圖片 → Excel 輸出含 5 行正確數據
- **Error Path**: 損壞圖片混入正常圖片時，正常圖片仍正確處理，損壞圖片被跳過
- **Edge Case**: 空 .txt 文件 → 顯示「未偵測到交易紀錄」；所有圖片都唔係轉帳截圖時 → 所有 record 標記 needs_review

**Output Files**:
- `tests/test_e2e.py`, `tests/conftest.py`
- `tests/fixtures/sample_chat.txt`, `tests/fixtures/sample_images/`
- `tests/fixtures/expected_output/expected.json`

---

### Task 12: 文檔 + README
- **Status**: pending
- **Required**: yes
- **Depends on**: Task 10

**Description**: 撰寫用戶文檔同 README。包括安裝指南（含 Tesseract 安裝）、使用說明、配置說明、常見問題。

**Input**: 完成嘅代碼 + CLI 介面
**Output**: README.md + docs/usage.md

**Expected Outcome**:
- [ ] README.md 包含：項目簡介、功能列表、安裝步驟、快速開始
- [ ] docs/usage.md 包含：詳細使用說明、配置選項、輸出格式說明
- [ ] Tesseract 安裝指南（Windows）
- [ ] AI Vision API 配置指南
- [ ] 常見問題 FAQ
- [ ] 文檔語言：中文

**Test Criteria**:
- **Happy Path**: README.md 嘅安裝步驟可以喺全新 Python 環境成功執行；usage.md 嘅命令範例可以正確運行
- **Error Path**: N/A（文檔任務）
- **Edge Case**: 確認所有文件路徑引用同實際目錄結構一致；確認所有依賴版本同 requirements.txt 一致

**Output Files**:
- `README.md`
- `docs/usage.md`

---

## Task 依賴圖

```
Task 1 (項目初始化 + Data Models)
├── Task 2 (Regex Patterns)
│   └── Task 3 (Text Parser 主邏輯) ──┐
├── Task 4 (Image Analyzer OCR) ──────┤
│   └── Task 5 (AI Vision, optional)  │
└──────────────────────────────────────┘
        │
        ▼
    Task 6 (配對邏輯)
        │
        ▼
    Task 7 (交易資訊提取)
        │
        ▼
    Task 8 (主整合邏輯)
        │
        ▼
    Task 9 (Excel Exporter)
        │
        ▼
    Task 10 (CLI + 串接)
    ├── Task 11 (E2E 測試)
    └── Task 12 (文檔)
```

---

## 優先級摘要

| 優先級 | Tasks | 說明 |
|--------|-------|------|
| P0 (必須) | 1, 2, 3, 4, 6, 7, 8, 9, 10 | 核心功能 |
| P1 (重要) | 11, 12 | 質量保證同用戶體驗 |
| P2 (可選) | 5 | AI Vision 模式（增強功能） |
