# Assignment 021

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-30T17:56:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 10: CLI 入口 + 主流程串接
- **TaskID**: ProjectWhatsapp/Task-10
- **TaskStatus**: pending → in_progress

## 需求
實現 CLI 入口點，用 Click 框架。串接所有模組成完整 pipeline。

需要建立：
- `src/main.py` — CLI 入口

### 具體功能要求

#### CLI 命令
```
python -m src.main analyze --input <folder> --output <file> --mode <ocr|ai_vision> [--config <path>] [--verbose]
```

#### 參數
- `--input` (required): 輸入資料夾路徑（包含 .txt 同圖片文件）
- `--output` (required): 輸出 .xlsx 文件路徑
- `--mode` (required): 分析模式（ocr 或 ai_vision），預設 ocr
- `--config` (optional): 配置文件路徑
- `--verbose` (optional): 顯示詳細日誌

#### 主流程
1. 驗證 --input 路徑存在
2. 自動偵測 .txt 文件同圖片文件（jpg/png/webp）
3. 如果有 .txt → 調用 `parse_chat_file()` 解析
4. 如果有圖片 → 調用 image analyzer（根據 --mode）
5. 調用 `build_records()` 整合
6. 調用 `export_to_excel()` 匯出
7. 保存中間結果 JSON 到 output 同目錄嘅 intermediate/ 子目錄
8. 顯示處理進度（正在解析文字... 正在分析圖片 3/10...）
9. 錯誤訊息全部中文

#### 錯誤處理
- --input 唔存在 → exit code 1 + 中文錯誤訊息
- --input 有圖片但無 .txt → 警告並終止
- --input 有 .txt 但無圖片 → 正常運行（只做文字分析，跳過圖片步驟）
- --mode 無效 → Click 自動顯示 usage help

## Context
- 已完成嘅模組：
  - `src/parser/text_parser.py` — `parse_chat_file(file_path) -> list[ParsedMessage]`
  - `src/analyzer/ocr_analyzer.py` — OCR 分析器
  - `src/builder/record_builder.py` — `build_records(messages, image_results) -> list[TransactionRecord]`
  - `src/exporter/excel_exporter.py` — `export_to_excel(records, output_path, sort_by)`
  - `src/config.py` — AppConfig
- 技術棧：Python 3.9+、Click
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-021/`
- **注意**：Image Analyzer 需要 Tesseract 安裝，CLI 應該 graceful handle Tesseract 未安裝嘅情況（顯示中文錯誤提示）
- **注意**：AI Vision 模式（Task 5）未實現，如果 --mode ai_vision 顯示「AI Vision 模式尚未實現」並 exit

## 驗證標準
- [ ] `main.py` 用 Click 實現 CLI
- [ ] 命令 `analyze` 有 --input, --output, --mode, --config, --verbose 參數
- [ ] 自動偵測 .txt 同圖片文件
- [ ] 顯示處理進度
- [ ] 錯誤訊息全部中文
- [ ] 中間結果保存到 intermediate/
- [ ] --verbose 顯示詳細日誌
- [ ] Unit tests 用 Click CliRunner 測試
- [ ] 所有 test pass

## Test Criteria
- **Happy Path**: 用 Click CliRunner 調用 analyze 命令，提供有效 input folder（含 .txt），exit code = 0 且 output 文件存在
- **Error Path**: --input 指向唔存在嘅路徑時 exit code = 1 且錯誤訊息為中文；--mode 為無效值時顯示 usage help
- **Edge Case**: input folder 有 .txt 但無圖片時仍正常運行（只做文字分析）；input folder 有圖片但無 .txt 時顯示警告並終止

## 預期輸出
完整可運行嘅代碼文件 + unit tests，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-021/` 目錄：
- `src/main.py`
- `tests/test_main.py`
