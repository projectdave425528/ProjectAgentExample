# Assignment 017

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-30T17:06:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 8: Transaction Record Builder — 主整合邏輯
- **TaskID**: ProjectWhatsapp/Task-8
- **TaskStatus**: pending → in_progress

## 需求
實現 RecordBuilder 主邏輯，結合 matcher + extractor + status_resolver，產出完整嘅 TransactionRecord 列表。輸出結構化 JSON 中間結果。

需要建立：
- `src/builder/record_builder.py` — 主整合邏輯

### 具體功能要求

#### record_builder.py
- `build_records(messages: list[ParsedMessage], image_results: list[ImageAnalysisResult]) -> list[TransactionRecord]`
- 流程：
  1. 調用 `match_images_to_messages(messages, image_results)` 取得 MatchResult
  2. 對每個 MatchedPair 調用 `extract_from_matched_pair(pair)` 取得 ExtractionResult
  3. 用 `group_by_time_window(results)` 分組
  4. 對每組用 `resolve_payment_status(quoted_amount, quantity, received_amount)` 判斷狀態
  5. 組裝 TransactionRecord
- 整體信心度計算（綜合 image_result.confidence + extraction.confidence）
- 標記需要人工確認嘅紀錄（confidence < 0.6 threshold）
- 支援將結果序列化為 JSON（`records_to_json(records) -> str`）
- JSON 可以反序列化回 `list[TransactionRecord]`（`json_to_records(json_str) -> list[TransactionRecord]`）

## Context
- 已完成嘅模組（全部喺 test-env/src/builder/）：
  - `matcher.py` — `match_images_to_messages(messages, image_results) -> MatchResult`
  - `extractor.py` — `extract_from_matched_pair(pair) -> ExtractionResult`、`group_by_time_window(results) -> list[list[ExtractionResult]]`
  - `status_resolver.py` — `resolve_payment_status(quoted_amount, quantity, received_amount) -> PaymentStatus`
- Data Models（test-env/src/models/）：
  - `message.py` — ParsedMessage
  - `image_result.py` — ImageAnalysisResult
  - `transaction.py` — TransactionRecord
- 技術棧：Python 3.9+、Pydantic v2
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-017/`

### TransactionRecord 欄位（供參考）
```python
id: str  # UUID auto-generated
transaction_date: date
customer_name: str
repair_item: str | None
quoted_amount: Decimal | None  # 單價
received_amount: Decimal | None  # 實收（from ImageAnalysisResult.amount）
payment_method: Literal["payme", "fps", "bank_transfer", "cash", "unknown"] | None
payment_status: Literal["paid", "unpaid", "partial"]
source_messages: list[int]  # message indices
source_images: list[str]  # image filenames
notes: str
confidence: float  # 0.0 - 1.0
needs_review: bool
```

### ExtractionResult 欄位（供參考）
```python
customer_name: str
repair_item: Optional[str]
quoted_amount: Optional[Decimal]  # 單價
quantity: int  # 預設 1
timestamp: datetime
confidence: float
```

### MatchedPair 欄位（供參考）
```python
message: ParsedMessage
image_result: ImageAnalysisResult  # 有 amount, payment_method, filename
needs_review: bool
```

## 驗證標準
- [ ] `record_builder.py` 實現 `build_records(messages, image_results) -> list[TransactionRecord]`
- [ ] 正確調用 matcher → extractor → status_resolver 流程
- [ ] 產出嘅 TransactionRecord 包含所有必要欄位
- [ ] 支援將結果序列化為 JSON（中間結果保存）
- [ ] JSON 可以反序列化回 list[TransactionRecord]
- [ ] 整體信心度計算（綜合各步驟信心度）
- [ ] 標記需要人工確認嘅紀錄（confidence < 0.6）
- [ ] Unit tests 覆蓋 Happy Path / Error Path / Edge Case
- [ ] 所有 test pass

## Test Criteria（從 specs 複製）
- **Happy Path**: 5 條 message + 3 個 image_result 正確產出對應數量嘅 TransactionRecord；JSON 序列化後可以反序列化回 list[TransactionRecord]
- **Error Path**: messages 同 image_results 都為空時返回空列表唔 crash；matcher 返回全部 unmatched 時仍產出 record（標記 needs_review）
- **Edge Case**: 單個 message 關聯多張圖片時正確處理；所有 record 嘅 confidence < threshold 時全部標記 needs_review；TransactionRecord.id 全局唯一

## 預期輸出
完整可運行嘅代碼文件 + unit tests，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-017/` 目錄：
- `src/builder/record_builder.py`
- `tests/test_builder/test_record_builder.py`
