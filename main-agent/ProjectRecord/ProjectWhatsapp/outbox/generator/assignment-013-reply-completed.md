# Assignment Reply: 013

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-30T02:45:05+08:00
- **AssignmentStatus**: completed
- **TaskRef**: Task 6: Transaction Record Builder — 配對邏輯
- **TaskID**: ProjectWhatsapp/Task-6
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] `matcher.py` 實現 `match_images_to_messages(messages, image_results) -> MatchResult`
- [x] 透過 attachment filename 精確配對
- [x] 配對失敗時記錄 warning（唔中斷）
- [x] 返回未配對嘅圖片列表（供後續處理/人工確認）
- [x] MatchResult 包含 matched_pairs + unmatched_images + unmatched_attachments
- [x] Case-insensitive filename 配對
- [x] 同一 filename 出現喺多條 message 時只配對第一次出現嘅
- [x] image_result 有 error 時仍然配對但標記 needs_review
- [x] Unit test 覆蓋 Happy Path / Error Path / Edge Case

## 結果

### 產出文件
| # | 文件 | 說明 |
|---|------|------|
| 1 | `output/assignment-013/src/builder/__init__.py` | Module init，export MatchedPair, MatchResult, match_images_to_messages |
| 2 | `output/assignment-013/src/builder/matcher.py` | 配對邏輯主模組（4 個函數，全部 <30 行） |
| 3 | `output/assignment-013/tests/test_builder/__init__.py` | Test module init |
| 4 | `output/assignment-013/tests/test_builder/test_matcher.py` | 17 個 unit tests |

### 設計決策
- `MatchedPair` 用 Pydantic BaseModel，包含 message + image_result + needs_review
- `needs_review` 由 `image_result.error is not None or image_result.needs_review` 決定
- `_build_attachment_index` 建立 lowercase filename → first message 嘅 dict（O(1) lookup）
- Unmatched attachments 保留原始大小寫（方便用戶識別）
- 所有 warning 用 `logging.warning`，唔中斷流程

### 測試結果
- **新 tests**：17/17 passed
- **全量 tests**：62/62 passed（無 regression）
- **執行時間**：0.78s

### Test 覆蓋
| 類型 | 數量 | 覆蓋場景 |
|------|------|----------|
| Happy Path | 4 | 全配對、部分配對、正確 message context、無 attachment 訊息忽略 |
| Error Path | 5 | 空 images、空 messages、雙空、無匹配、warning log 驗證 |
| Edge Case | 8 | Case-insensitive（雙向）、重複 filename 只配第一個、error image needs_review、多 attachment 單 message、原始大小寫保留、Pydantic 序列化 |

## 備註
- 代碼已複製到 test-env 驗證通過
- Task 7（交易資訊提取）可以直接使用 MatchedPair model

## Memory 已更新
✅

## Usage 估算
- **Context 使用率**: 40%
- **估算 Token 數**: ~12,000 input / ~5,000 output
- **接近限額警告**: ✅
