# Assignment 015

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-30T11:01:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 7: Transaction Record Builder — 交易資訊提取
- **TaskID**: ProjectWhatsapp/Task-7
- **TaskStatus**: pending → in_progress

## 需求
實現交易資訊提取模組。從配對好嘅對話 context 中提取：客戶名稱、維修項目、數量、報價金額。同時實現付款狀態判斷邏輯（比較 報價×數量 vs 實收金額）。

需要建立兩個模組：
1. `src/builder/extractor.py` — 交易資訊提取
2. `src/builder/status_resolver.py` — 付款狀態判斷

### 具體功能要求

#### extractor.py
- 客戶名稱從 MatchedPair.message.sender 提取
- 維修項目用關鍵字匹配（換屏、換電池、維修、整機、換mon、換芒、貼膜 等）
- 數量提取：支援「3部」「x2」「×3」「2台」「兩部」「三部」等格式，預設為 1
- 報價金額用 regex 從對話提取（$xxx、xxx蚊、xxx元、HK$xxx）— 為單價
- 支援廣東話金額表達（「三百」「五百蚊」「一千」等）
- 處理一個客戶多次交易（按時間窗口分組，預設 2 小時）

#### status_resolver.py
- 比較 quoted_amount × quantity vs received_amount（來自 ImageAnalysisResult.amount）
- 完全匹配 → "paid"
- 部分匹配（received > 0 但 < total）→ "partial"
- 無收款記錄 → "unpaid"
- 容差：±1%（避免 floating point 問題）

## Context
- 配對邏輯已完成：`test-env/src/builder/matcher.py`（MatchedPair、MatchResult）
- Data Models：
  - `test-env/src/models/message.py` — ParsedMessage（有 sender、content、timestamp、attachments）
  - `test-env/src/models/image_result.py` — ImageAnalysisResult（有 amount、payment_method）
  - `test-env/src/models/transaction.py` — TransactionRecord（有 quoted_amount、received_amount、payment_status、quantity 欄位需要確認）
- 技術棧：Python 3.9+、Pydantic v2
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-015/`
- **注意**：TransactionRecord 目前冇 quantity 欄位，extractor 需要自行管理 quantity 並計算 total（quoted_amount × quantity）

### 現有 TransactionRecord 欄位（供參考）
```python
id: str  # UUID
transaction_date: date
customer_name: str
repair_item: str | None
quoted_amount: Decimal | None  # 單價
received_amount: Decimal | None  # 實收
payment_method: Literal["payme", "fps", "bank_transfer", "cash", "unknown"] | None
payment_status: Literal["paid", "unpaid", "partial"]
source_messages: list[int]
source_images: list[str]
notes: str
confidence: float
needs_review: bool
```

### MatchedPair 結構（供參考）
```python
class MatchedPair(BaseModel):
    message: ParsedMessage  # 有 sender, content, timestamp, attachments
    image_result: ImageAnalysisResult  # 有 amount, payment_method
    needs_review: bool
```

## 驗證標準
- [ ] `extractor.py` 實現交易資訊提取
- [ ] 客戶名稱從 sender 欄位提取
- [ ] 維修項目用關鍵字匹配（換屏、換電池、維修、整機等）
- [ ] 數量提取：支援「3部」「x2」「×3」「2台」「兩部」等格式，預設為 1
- [ ] 報價金額用 regex 從對話提取（$xxx、xxx蚊、xxx元）— 為單價
- [ ] 支援廣東話金額表達（「三百」「五百蚊」等）
- [ ] `status_resolver.py` 判斷付款狀態（比較 報價×數量 vs 實收）
- [ ] 處理一個客戶多次交易（按時間窗口分組）
- [ ] Unit tests 覆蓋 Happy Path / Error Path / Edge Case
- [ ] 所有 test pass

## Test Criteria（從 specs 複製）
- **Happy Path**: 對話含 "換屏 $500" 時正確提取 repair_item="換屏", quoted_amount=500, quantity=1；對話含 "換屏 x3 $500" 時 quantity=3；sender="陳大文" 時 customer_name="陳大文"；報價500×2=1000 實收1000時 status="paid"
- **Error Path**: 對話完全無金額相關內容時 quoted_amount=None 且唔 crash；sender 為空字串時 customer_name 設為 "Unknown"
- **Edge Case**: 廣東話 "三百蚊" 正確轉換為 300；廣東話 "兩部" 正確轉換為 quantity=2；同一客戶 2 小時內有 2 筆唔同金額交易時分為 2 個 record；報價500×2=1000 實收700時 status="partial"

## 預期輸出
完整可運行嘅代碼文件 + unit tests，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-015/` 目錄：
- `src/builder/extractor.py`
- `src/builder/status_resolver.py`
- `tests/test_builder/test_extractor.py`
- `tests/test_builder/test_status_resolver.py`
