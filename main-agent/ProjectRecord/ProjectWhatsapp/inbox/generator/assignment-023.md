# Assignment 023

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-31T10:01:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 11: 端到端整合測試
- **TaskID**: ProjectWhatsapp/Task-11
- **TaskStatus**: pending → in_progress

## 需求
建立完整嘅端到端測試。用 sample data 跑完整 pipeline，驗證最終 Excel 輸出正確。

需要建立：
- `tests/test_e2e.py` — E2E 測試
- `tests/conftest.py` — 共用 fixtures
- `tests/fixtures/sample_chat.txt` — 測試用 WhatsApp 對話文件
- `tests/fixtures/expected_output/expected.json` — 預期輸出

### 具體功能要求

#### test_e2e.py
- 端到端測試：輸入 .txt → 解析 → 分析（mock OCR）→ 整合 → 匯出 Excel
- 驗證 Excel 輸出嘅欄位值正確
- Edge case 測試：空文件、無交易內容

#### sample_chat.txt
建立一個包含 5 筆交易嘅 WhatsApp 對話文件，格式：
```
[2024/01/15, 10:00:00] 陳大文: 換屏 $500
[2024/01/15, 10:01:00] 陳大文: <attached: img001.jpg>
[2024/01/15, 11:00:00] 李小明: 換電池 x2 $300
[2024/01/15, 11:01:00] 李小明: <attached: img002.jpg>
[2024/01/15, 14:00:00] 王美麗: 維修 $800
[2024/01/15, 14:01:00] 王美麗: <attached: img003.jpg>
[2024/01/15, 15:00:00] 張三: 貼膜 三百蚊
[2024/01/15, 15:01:00] 張三: <attached: img004.jpg>
[2024/01/15, 16:00:00] 趙四: 整機 $1,200
[2024/01/15, 16:01:00] 趙四: <attached: img005.jpg>
```

#### conftest.py
- 共用 fixtures：sample_chat_path、mock_image_results、tmp_output_path
- mock_image_results 返回 5 個 ImageAnalysisResult（對應 img001-005.jpg）

#### expected.json
- 5 筆交易嘅預期 TransactionRecord（JSON 格式）

### 測試場景

1. **Happy Path**: sample_chat.txt（5 筆交易）+ 5 個 mock image results → Excel 輸出含 5 行正確數據
2. **Error Path**: 損壞圖片混入正常圖片時，正常圖片仍正確處理（mock 一個 error result）
3. **Edge Case - 空文件**: 空 .txt → build_records 返回空列表 → Excel 只有表頭
4. **Edge Case - 無交易**: .txt 有訊息但冇金額/維修關鍵字 → records 有 needs_review flag

### 注意事項
- **唔好真正調用 OCR** — 用 mock ImageAnalysisResult 代替
- 用 `parse_chat_file` 真正解析 sample_chat.txt（測試真實 parser）
- 用 `build_records` 真正整合（測試真實 builder）
- 用 `export_to_excel` 真正匯出（測試真實 exporter）
- 用 `openpyxl` 讀取 Excel 驗證內容

### Import 路徑
```python
from src.parser.text_parser import parse_chat_file
from src.builder.record_builder import build_records
from src.exporter.excel_exporter import export_to_excel
from src.models.image_result import ImageAnalysisResult
```

## Context
- 所有模組已完成（test-env/src/）
- 技術棧：Python 3.9+、pytest、openpyxl
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-023/`

## 驗證標準
- [ ] 建立完整 test fixtures（sample_chat.txt + mock images）
- [ ] 端到端測試：輸入 → 解析 → 分析 → 整合 → 匯出
- [ ] 驗證 Excel 輸出嘅欄位值正確
- [ ] Edge case 測試：空文件、無交易內容
- [ ] 所有測試 pass
- [ ] 整體覆蓋率 > 80%（如果可以量度）

## Test Criteria
- **Happy Path**: sample_chat.txt（含 5 筆交易）+ 5 個 mock image results → Excel 輸出含 5 行正確數據
- **Error Path**: 損壞圖片混入正常圖片時，正常圖片仍正確處理，損壞圖片被跳過
- **Edge Case**: 空 .txt 文件 → 顯示「未偵測到交易紀錄」；所有圖片都唔係轉帳截圖時 → 所有 record 標記 needs_review

## 預期輸出
完整可運行嘅代碼文件，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-023/` 目錄：
- `tests/test_e2e.py`
- `tests/conftest.py`
- `tests/fixtures/sample_chat.txt`
- `tests/fixtures/expected_output/expected.json`
