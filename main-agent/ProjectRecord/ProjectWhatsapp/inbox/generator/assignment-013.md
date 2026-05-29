# Assignment 013

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-30T10:01:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 6: Transaction Record Builder — 配對邏輯
- **TaskID**: ProjectWhatsapp/Task-6
- **TaskStatus**: pending → in_progress

## 需求
實現圖片同對話嘅配對邏輯。透過 `<attached:filename>` 引用同時間戳，將 ImageAnalysisResult 同對應嘅 ParsedMessage context 配對。

具體要求：
1. 建立 `src/builder/__init__.py` 同 `src/builder/matcher.py`
2. 建立 `tests/test_builder/__init__.py` 同 `tests/test_builder/test_matcher.py`
3. 實現 `match_images_to_messages(messages, image_results) -> MatchResult`
4. 透過 attachment filename 精確配對（case-insensitive）
5. 配對失敗時記錄 warning（唔中斷）
6. 返回未配對嘅圖片列表同未配對嘅 attachments
7. MatchResult 包含 matched_pairs + unmatched_images + unmatched_attachments
8. 必須同時提供 unit test

## Context
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-013/`
- 現有代碼環境：`ProjectRecord/ProjectWhatsapp/test-env/`
- 技術棧：Python 3.9+、Pydantic v2、pytest
- ParsedMessage model（已存在）：
  ```python
  class ParsedMessage(BaseModel):
      timestamp: datetime
      sender: str
      content: str
      is_system_message: bool = False
      attachments: list[str] = []  # 附件文件名列表
      raw_text: str
  ```
- ImageAnalysisResult model（已存在）：
  ```python
  class ImageAnalysisResult(BaseModel):
      filename: str
      image_date: date | None = None
      analysis_mode: Literal["ocr", "ai_vision"]
      payment_method: Literal["payme", "fps", "bank_transfer", "unknown"] | None = None
      amount: Decimal | None = None
      transaction_date: date | None = None
      transaction_id: str | None = None
      confidence: float
      raw_text: str | None = None
      needs_review: bool = False
      error: str | None = None
  ```
- 需要定義新嘅 MatchedPair 同 MatchResult model（可以放喺 matcher.py 或獨立 model 文件）

## 驗證標準
- [ ] `matcher.py` 實現 `match_images_to_messages(messages, image_results) -> MatchResult`
- [ ] 透過 attachment filename 精確配對
- [ ] 配對失敗時記錄 warning（唔中斷）
- [ ] 返回未配對嘅圖片列表（供後續處理/人工確認）
- [ ] MatchResult 包含 matched_pairs + unmatched_images + unmatched_attachments
- [ ] Case-insensitive filename 配對
- [ ] 同一 filename 出現喺多條 message 時只配對第一次出現嘅
- [ ] image_result 有 error 時仍然配對但標記 needs_review
- [ ] Unit test 覆蓋 Happy Path / Error Path / Edge Case

## Test Criteria（從 specs 複製）
- **Happy Path**: 3 條含 attachment 嘅 message + 3 個對應 image_result 正確配對為 3 個 MatchedPair；配對後 MatchedPair 包含正確嘅 message context
- **Error Path**: image_results 為空列表時返回空 matched_pairs + 所有 attachments 列入 unmatched；messages 為空列表時返回空結果唔 crash
- **Edge Case**: 同一 filename 出現喺多條 message 時只配對第一次出現嘅；image_result 有 error 時仍然配對但標記 needs_review；filename 大小寫唔一致時 case-insensitive 配對

## 預期輸出
完整可運行嘅代碼文件，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-013/` 目錄：
- `src/builder/__init__.py`
- `src/builder/matcher.py`
- `tests/test_builder/__init__.py`
- `tests/test_builder/test_matcher.py`
