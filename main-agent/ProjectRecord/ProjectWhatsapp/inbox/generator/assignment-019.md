# Assignment 019

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-30T17:31:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 9: Excel Exporter
- **TaskID**: ProjectWhatsapp/Task-9
- **TaskStatus**: pending → in_progress

## 需求
實現 Excel 匯出功能。將 TransactionRecord 列表寫入 .xlsx 文件。

需要建立：
1. `src/exporter/__init__.py`
2. `src/exporter/excel_exporter.py` — 主匯出邏輯
3. `src/exporter/formatters.py` — 欄位格式化

### 具體功能要求

#### excel_exporter.py
- `export_to_excel(records: list[TransactionRecord], output_path: str, sort_by: str = "date") -> None`
- 欄位（表頭）：日期、客戶名稱、維修項目、數量、報價金額（單價）、實收金額、付款方式、付款狀態、備註
- 支援按日期排序（預設）同按客戶名稱排序
- 最後一行自動計算報價總額同實收總額
- 表頭格式：粗體、背景色（淺藍）
- 欄寬自動調整（根據內容長度）
- 金額格式：保留 2 位小數
- 日期格式：YYYY-MM-DD

#### formatters.py
- `format_date(d: date) -> str` — 格式化日期
- `format_amount(amount: Decimal | None) -> str` — 格式化金額（None → ""）
- `format_payment_method(method: str | None) -> str` — 中文化付款方式
- `format_payment_status(status: str) -> str` — 中文化付款狀態

### 付款方式中文化
- payme → "PayMe"
- fps → "轉數快"
- bank_transfer → "銀行轉帳"
- cash → "現金"
- unknown → "未知"

### 付款狀態中文化
- paid → "已付"
- unpaid → "未付"
- partial → "部分付款"

## Context
- TransactionRecord 欄位：transaction_date, customer_name, repair_item, quoted_amount, received_amount, payment_method, payment_status, notes, confidence, needs_review
- 技術棧：Python 3.9+、openpyxl
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-019/`
- **注意**：TransactionRecord 冇 quantity 欄位。如果 notes 包含 "數量: X"，提取 X 作為數量顯示；否則顯示 1

## 驗證標準
- [ ] `export_to_excel` 正確產出 .xlsx 文件
- [ ] 包含正確欄位（9 欄）
- [ ] 支援按日期/客戶名稱排序
- [ ] 最後一行有報價總額同實收總額
- [ ] 表頭有格式（粗體、背景色）
- [ ] 欄寬自動調整
- [ ] 金額格式化（2 位小數）
- [ ] 付款方式/狀態中文化
- [ ] records 為空時產出只有表頭嘅 Excel
- [ ] output_path 目錄唔存在時 raise 明確錯誤
- [ ] Unit tests 覆蓋 Happy Path / Error Path / Edge Case
- [ ] 所有 test pass

## Test Criteria
- **Happy Path**: 3 個 TransactionRecord 匯出後用 openpyxl 讀取驗證有 3 行數據 + 1 行表頭 + 1 行總計；金額欄位值正確；排序正確
- **Error Path**: output_path 目錄唔存在時 raise 明確錯誤（唔係 generic OSError）；records 為空列表時產出只有表頭嘅 Excel（唔 crash）
- **Edge Case**: 客戶名稱含 emoji 時 Excel 正確顯示；金額為 None 時欄位顯示為空（唔係 "None"）；100+ records 時效能 < 3 秒

## 預期輸出
完整可運行嘅代碼文件 + unit tests，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-019/` 目錄：
- `src/exporter/__init__.py`
- `src/exporter/excel_exporter.py`
- `src/exporter/formatters.py`
- `tests/test_exporter/__init__.py`
- `tests/test_exporter/test_excel_exporter.py`
