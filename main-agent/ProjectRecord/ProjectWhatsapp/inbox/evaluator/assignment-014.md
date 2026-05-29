# Assignment 014

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-30T10:07:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 6: Transaction Record Builder — 配對邏輯
- **TaskID**: ProjectWhatsapp/Task-6
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 6 配對邏輯代碼。執行 unit test 並驗證結果。

## Context
- 代碼位置：`ProjectRecord/ProjectWhatsapp/output/assignment-013/`
  - `src/builder/__init__.py`
  - `src/builder/matcher.py`
  - `tests/test_builder/__init__.py`
  - `tests/test_builder/test_matcher.py`
- 合併測試環境：`ProjectRecord/ProjectWhatsapp/test-env/`
- Generator 回覆：`ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-013-reply-completed.md`
- Task 定義：`ProjectRecord/ProjectWhatsapp/specs/tasks.md` → Task 6

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
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] 代碼有 type hints 同 docstrings
- [ ] 所有 tests pass

## Test Criteria（從 specs 複製）
- **Happy Path**: 3 條含 attachment 嘅 message + 3 個對應 image_result 正確配對為 3 個 MatchedPair；配對後 MatchedPair 包含正確嘅 message context
- **Error Path**: image_results 為空列表時返回空 matched_pairs + 所有 attachments 列入 unmatched；messages 為空列表時返回空結果唔 crash
- **Edge Case**: 同一 filename 出現喺多條 message 時只配對第一次出現嘅；image_result 有 error 時仍然配對但標記 needs_review；filename 大小寫唔一致時 case-insensitive 配對

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
