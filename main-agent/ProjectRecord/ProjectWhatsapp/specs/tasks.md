# Tasks: WhatsApp 帳目分析系統

---

## Task 1: 項目初始化 + Data Models

- **Status**: pending
- **Required**: yes
- **Depends on**: (none)
- **Description**: 建立項目結構、安裝依賴、定義所有 Pydantic data models。包括 ParsedMessage、ImageAnalysisResult、TransactionRecord、AppConfig。建立 config 載入機制（.env + config.yaml）。
- **Expected Outcome**:
  - [ ] 項目目錄結構已建立（src/、tests/、docs/）
  - [ ] requirements.txt 包含所有核心依賴（pydantic、openpyxl、click、pillow、pytesseract、python-dotenv、pyyaml、openai）
  - [ ] src/models/ 下所有 data model 已定義（message.py、image_result.py、transaction.py、config.py）
  - [ ] Pydantic model 有正確嘅 type hints 同 validators
  - [ ] src/config.py 可以載入 .env 同 config.yaml
  - [ ] .env.example 已建立（包含 API Key placeholder）
  - [ ] config.yaml 有合理嘅預設值
  - [ ] pytest 可以成功 import 所有 models
- **Output Files**:
  - `src/__init__.py`
  - `src/models/__init__.py`
  - `src/models/message.py`
  - `src/models/image_result.py`
  - `src/models/transaction.py`
  - `src/models/config.py`
  - `src/config.py`
  - `requirements.txt`
  - `.env.example`
  - `config.yaml`
  - `setup.py`

---

## Task 2: WhatsApp Text Parser — Regex Patterns

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 1
- **Description**: 實現 WhatsApp 對話文件嘅 regex patterns，支援多種時間格式（12/24小時制、唔同日期順序）。定義 pattern 常量同 utility functions。
- **Expected Outcome**:
  - [ ] 定義主訊息 regex pattern：`[YYYY/MM/DD, HH:MM:SS] Sender: Message`
  - [ ] 支援 24 小時制格式
  - [ ] 支援 12 小時制格式（AM/PM）
  - [ ] 支援日期順序變體（YYYY/MM/DD、DD/MM/YYYY、MM/DD/YYYY）
  - [ ] 支援日期分隔符變體（/、-、.）
  - [ ] 定義系統訊息識別 patterns
  - [ ] 定義 `<attached:filename>` 提取 pattern
  - [ ] 所有 patterns 有對應嘅單元測試
  - [ ] 測試覆蓋率 > 90%
- **Output Files**:
  - `src/parser/__init__.py`
  - `src/parser/patterns.py`
  - `src/parser/utils.py`
  - `tests/test_parser/__init__.py`
  - `tests/test_parser/test_patterns.py`

---

## Task 3: WhatsApp Text Parser — 主解析邏輯

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 2
- **Description**: 實現完整嘅 .txt 文件解析器。逐行讀取文件，用 regex 解析每條訊息，處理多行訊息、系統訊息、media attachments。輸出 ParsedMessage 列表。
- **Expected Outcome**:
  - [ ] `text_parser.py` 實現 `parse_chat_file(file_path) -> list[ParsedMessage]`
  - [ ] 正確處理多行訊息（無時間戳嘅行歸屬前一條訊息）
  - [ ] 正確識別並標記系統訊息
  - [ ] 正確提取 `<attached:filename>` 到 attachments 列表
  - [ ] 處理空文件（返回空列表 + warning）
  - [ ] 處理大文件（分段讀取，唔會 OOM）
  - [ ] 自動偵測時間格式（唔需要用戶指定）
  - [ ] 有完整嘅單元測試 + sample_chat.txt fixture
  - [ ] 錯誤處理：無法解析嘅行記錄 warning 並跳過
- **Output Files**:
  - `src/parser/text_parser.py`
  - `tests/test_parser/test_text_parser.py`
  - `tests/fixtures/sample_chat.txt`

---

## Task 4: Image Analyzer — Base + OCR 模式

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 1
- **Description**: 實現圖片分析器嘅 base class 同 Tesseract OCR 模式。包括圖片讀取、OCR 文字提取、金額識別、付款方式偵測。
- **Expected Outcome**:
  - [ ] `base.py` 定義 `ImageAnalyzerBase` abstract class
  - [ ] `ocr_analyzer.py` 實現 Tesseract OCR 分析
  - [ ] 支援 JPG、PNG、WEBP 格式讀取
  - [ ] `amount_extractor.py` 可以從 OCR 文字提取金額（支援 $、HK$、千位分隔符）
  - [ ] `payment_detector.py` 可以識別 PayMe/FPS/銀行轉帳截圖
  - [ ] 單張圖片分析失敗時返回 error result（唔 raise exception）
  - [ ] 信心度計算邏輯（基於 OCR 結果質量）
  - [ ] 有單元測試（mock Tesseract 輸出）
- **Output Files**:
  - `src/analyzer/__init__.py`
  - `src/analyzer/base.py`
  - `src/analyzer/ocr_analyzer.py`
  - `src/analyzer/amount_extractor.py`
  - `src/analyzer/payment_detector.py`
  - `tests/test_analyzer/__init__.py`
  - `tests/test_analyzer/test_ocr_analyzer.py`
  - `tests/test_analyzer/test_payment_detector.py`

---

## Task 5: Image Analyzer — AI Vision 模式

- **Status**: pending
- **Required**: no
- **Depends on**: Task 4
- **Description**: 實現 AI Vision API 分析模式。調用 OpenAI Vision API 分析轉帳截圖，提取金額、付款方式、交易日期等資訊。
- **Expected Outcome**:
  - [ ] `ai_vision.py` 實現 AI Vision 分析器（繼承 base class）
  - [ ] 正確構建 API request（image base64 encoding）
  - [ ] 設計有效嘅 prompt 提取交易資訊
  - [ ] 解析 API response 到 ImageAnalysisResult
  - [ ] API 失敗時 graceful fallback（返回 error result）
  - [ ] API Key 從環境變數讀取（唔 hardcode）
  - [ ] Rate limiting 處理
  - [ ] 有單元測試（mock API response）
- **Output Files**:
  - `src/analyzer/ai_vision.py`
  - `tests/test_analyzer/test_ai_vision.py`

---

## Task 6: Transaction Record Builder — 配對邏輯

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 3, Task 4
- **Description**: 實現圖片同對話嘅配對邏輯。透過 `<attached:filename>` 引用同時間戳，將 ImageAnalysisResult 同對應嘅 ParsedMessage context 配對。
- **Expected Outcome**:
  - [ ] `matcher.py` 實現 `match_images_to_messages(messages, image_results) -> list[MatchedPair]`
  - [ ] 透過 attachment filename 精確配對
  - [ ] 配對失敗時記錄 warning（唔中斷）
  - [ ] 返回未配對嘅圖片列表（供後續處理）
  - [ ] 有單元測試
- **Output Files**:
  - `src/builder/__init__.py`
  - `src/builder/matcher.py`
  - `tests/test_builder/__init__.py`
  - `tests/test_builder/test_matcher.py`

---

## Task 7: Transaction Record Builder — 交易資訊提取

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 6
- **Description**: 從配對好嘅對話 context 中提取交易資訊：客戶名稱、維修項目、報價金額。用關鍵字匹配策略處理廣東話/中文/英文混合內容。
- **Expected Outcome**:
  - [ ] `extractor.py` 實現交易資訊提取
  - [ ] 客戶名稱從 sender 欄位提取
  - [ ] 維修項目用關鍵字匹配（換屏、換電池、維修、整機等）
  - [ ] 報價金額用 regex 從對話提取（$xxx、xxx蚊、xxx元）
  - [ ] 支援廣東話金額表達（「三百」「五百蚊」等）
  - [ ] `status_resolver.py` 判斷付款狀態（比較報價 vs 實收）
  - [ ] 處理一個客戶多次交易（按時間窗口分組）
  - [ ] 有單元測試
- **Output Files**:
  - `src/builder/extractor.py`
  - `src/builder/status_resolver.py`
  - `tests/test_builder/test_extractor.py`
  - `tests/test_builder/test_status_resolver.py`

---

## Task 8: Transaction Record Builder — 主整合邏輯

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 7
- **Description**: 實現 RecordBuilder 主邏輯，結合 matcher + extractor + status_resolver，產出完整嘅 TransactionRecord 列表。輸出結構化 JSON。
- **Expected Outcome**:
  - [ ] `record_builder.py` 實現 `build_records(messages, image_results) -> list[TransactionRecord]`
  - [ ] 正確調用 matcher → extractor → status_resolver 流程
  - [ ] 產出嘅 TransactionRecord 包含所有必要欄位
  - [ ] 支援將結果序列化為 JSON（中間結果保存）
  - [ ] 整體信心度計算（綜合各步驟信心度）
  - [ ] 標記需要人工確認嘅紀錄
  - [ ] 有整合測試
- **Output Files**:
  - `src/builder/record_builder.py`
  - `tests/test_builder/test_record_builder.py`

---

## Task 9: Excel Exporter

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 8
- **Description**: 實現 Excel 匯出功能。將 TransactionRecord 列表寫入 .xlsx 文件，包含所有欄位、排序、格式化、自動計算總額。
- **Expected Outcome**:
  - [ ] `excel_exporter.py` 實現 `export_to_excel(records, output_path, sort_by)`
  - [ ] 包含所有欄位：日期、客戶名稱、維修項目、報價金額、實收金額、付款方式、付款狀態、備註
  - [ ] 支援按日期排序（預設）
  - [ ] 支援按客戶名稱排序
  - [ ] 最後一行自動計算報價總額同實收總額
  - [ ] 欄位格式化（日期格式、金額格式、欄寬自動調整）
  - [ ] 表頭有格式（粗體、背景色）
  - [ ] `formatters.py` 處理欄位顯示格式
  - [ ] 有單元測試（驗證輸出 Excel 內容）
- **Output Files**:
  - `src/exporter/__init__.py`
  - `src/exporter/excel_exporter.py`
  - `src/exporter/formatters.py`
  - `tests/test_exporter/__init__.py`
  - `tests/test_exporter/test_excel_exporter.py`

---

## Task 10: CLI 入口 + 主流程串接

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 9
- **Description**: 實現 CLI 入口點，用 Click 框架。串接所有模組成完整 pipeline。提供進度提示、錯誤訊息中文化、中間結果保存。
- **Expected Outcome**:
  - [ ] `main.py` 用 Click 實現 CLI
  - [ ] 命令：`python -m src.main analyze --input <folder> --output <file> --mode <ocr|ai_vision>`
  - [ ] 自動偵測輸入資料夾中嘅 .txt 同圖片文件
  - [ ] 顯示處理進度（正在解析文字... 正在分析圖片 3/10...）
  - [ ] 錯誤訊息全部中文
  - [ ] 中間結果保存到 output/intermediate/
  - [ ] 最終輸出 .xlsx 路徑顯示
  - [ ] `--verbose` flag 顯示詳細日誌
  - [ ] `--config` flag 指定配置文件路徑
  - [ ] 有基本嘅 CLI 測試
- **Output Files**:
  - `src/main.py`
  - `tests/test_main.py`

---

## Task 11: 端到端整合測試

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 10
- **Description**: 建立完整嘅端到端測試。用 sample data 跑完整 pipeline，驗證最終 Excel 輸出正確。包括正常流程同 edge cases。
- **Expected Outcome**:
  - [ ] 建立完整嘅 test fixtures（sample_chat.txt + sample images）
  - [ ] 端到端測試：輸入 → 解析 → 分析 → 整合 → 匯出
  - [ ] 驗證 Excel 輸出嘅欄位值正確
  - [ ] Edge case 測試：空文件、損壞圖片、無交易內容
  - [ ] 測試報告顯示覆蓋率
  - [ ] 所有測試 pass
- **Output Files**:
  - `tests/test_e2e.py`
  - `tests/fixtures/sample_chat.txt`（更新）
  - `tests/fixtures/sample_images/` (mock images)
  - `tests/fixtures/expected_output/expected.json`
  - `tests/conftest.py`

---

## Task 12: 文檔 + README

- **Status**: pending
- **Required**: yes
- **Depends on**: Task 10
- **Description**: 撰寫用戶文檔同 README。包括安裝指南（含 Tesseract 安裝）、使用說明、配置說明、常見問題。
- **Expected Outcome**:
  - [ ] README.md 包含：項目簡介、功能列表、安裝步驟、快速開始
  - [ ] docs/usage.md 包含：詳細使用說明、配置選項、輸出格式說明
  - [ ] Tesseract 安裝指南（Windows）
  - [ ] AI Vision API 配置指南
  - [ ] 常見問題 FAQ
  - [ ] 文檔語言：中文
- **Output Files**:
  - `README.md`
  - `docs/usage.md`

---

## Task 依賴圖

```
Task 1 (項目初始化)
├── Task 2 (Regex Patterns)
│   └── Task 3 (Text Parser 主邏輯)
│       └── Task 6 (配對邏輯) ─┐
├── Task 4 (Image Analyzer OCR)  │
│   ├── Task 5 (AI Vision)      │
│   └── Task 6 (配對邏輯) ──────┘
│       └── Task 7 (交易資訊提取)
│           └── Task 8 (整合邏輯)
│               └── Task 9 (Excel Exporter)
│                   └── Task 10 (CLI + 串接)
│                       ├── Task 11 (E2E 測試)
│                       └── Task 12 (文檔)
```

---

## 優先級摘要

| 優先級 | Tasks | 說明 |
|--------|-------|------|
| P0 (必須) | 1, 2, 3, 4, 6, 7, 8, 9, 10 | 核心功能，缺一不可 |
| P1 (重要) | 11, 12 | 質量保證同用戶體驗 |
| P2 (可選) | 5 | AI Vision 模式（增強功能） |
