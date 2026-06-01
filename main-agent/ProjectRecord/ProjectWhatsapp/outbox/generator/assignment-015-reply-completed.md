# Assignment Reply: 015

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-30T16:19:00+08:00
- **AssignmentStatus**: completed
- **TaskRef**: Task 7: Transaction Record Builder — 交易資訊提取
- **TaskID**: ProjectWhatsapp/Task-7
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] `extractor.py` 實現交易資訊提取
- [x] 客戶名稱從 sender 欄位提取
- [x] 維修項目用關鍵字匹配（換屏、換電池、維修、整機等）
- [x] 數量提取：支援「3部」「x2」「×3」「2台」「兩部」等格式，預設為 1
- [x] 報價金額用 regex 從對話提取（$xxx、xxx蚊、xxx元）— 為單價
- [x] 支援廣東話金額表達（「三百」「五百蚊」等）
- [x] `status_resolver.py` 判斷付款狀態（比較 報價×數量 vs 實收）
- [x] 處理一個客戶多次交易（按時間窗口分組）
- [x] Unit tests 覆蓋 Happy Path / Error Path / Edge Case
- [x] 所有 test pass

## 結果

### 生成文件
| # | 文件路徑 | 用途 |
|---|----------|------|
| 1 | `src/builder/extractor.py` | 交易資訊提取模組 |
| 2 | `src/builder/status_resolver.py` | 付款狀態判斷模組 |
| 3 | `tests/test_builder/test_extractor.py` | extractor 單元測試（46 tests） |
| 4 | `tests/test_builder/test_status_resolver.py` | status_resolver 單元測試（23 tests） |
| 5 | `src/__init__.py` | Package init |
| 6 | `src/builder/__init__.py` | Package init |
| 7 | `tests/__init__.py` | Package init |
| 8 | `tests/test_builder/__init__.py` | Package init |

### 測試結果
- **執行命令**: `python -m pytest tests/ -v`
- **結果**: 69 passed in 1.58s
- **失敗 tests**: 0

### 設計決策

1. **ExtractionResult 中間結構** — 因為 TransactionRecord 冇 quantity 欄位，建立 ExtractionResult BaseModel 包含 quantity + timestamp，方便後續 record_builder 整合時計算 total。

2. **時間窗口分組邏輯** — `group_by_time_window()` 按 customer_name + timestamp + quoted_amount 三個維度分組。同一客戶 2 小時內相同金額嘅交易歸為一組，唔同金額分為唔同 record。

3. **付款狀態容差** — ±1% tolerance 用 Decimal 計算避免 floating point 問題。Overpaid 視為 "paid"。

4. **廣東話支援** — 用 dict lookup 處理中文數字（一到十）同金額表達（一百到五千），覆蓋常見維修報價範圍。

### 模組 API 摘要

**extractor.py**:
- `extract_customer_name(sender: str) -> str`
- `extract_repair_item(content: str) -> Optional[str]`
- `extract_quantity(content: str) -> int`
- `extract_quoted_amount(content: str) -> Optional[Decimal]`
- `extract_from_matched_pair(pair) -> ExtractionResult`
- `group_by_time_window(results, window_hours=2) -> list[list[ExtractionResult]]`

**status_resolver.py**:
- `resolve_payment_status(quoted_amount, quantity, received_amount) -> PaymentStatus`

## 備註
- 所有函數 < 30 行、參數 ≤ 3、Loop ≤ 3 層
- `extract_from_matched_pair` 接受 duck-typed pair（有 message.sender/content/timestamp 即可），方便 mock 測試
- 後續 Task 8 (record_builder) 可以直接 import ExtractionResult + resolve_payment_status 整合

## Memory 已更新
✅

## Usage 估算
- **Context 使用率**: 40%
- **估算 Token 數**: ~15,000 input / ~8,000 output
- **接近限額警告**: ✅
