# Assignment Reply: 017

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-30T17:19:03+08:00
- **AssignmentStatus**: completed
- **TaskRef**: Task 8: Transaction Record Builder — 主整合邏輯
- **TaskID**: ProjectWhatsapp/Task-8
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] build_records(messages, image_results) → list[TransactionRecord]
- [x] 流程：match → extract → group → resolve status → assemble
- [x] 整體信心度 = round((image_confidence + extraction_confidence) / 2, 2)
- [x] needs_review = confidence < 0.6 or MatchedPair.needs_review
- [x] records_to_json(records) → str
- [x] json_to_records(json_str) → list[TransactionRecord]
- [x] Happy Path: 5 messages + 3 images 正確產出 3 個 TransactionRecord；JSON round-trip 正確
- [x] Error Path: 空 messages + 空 images 返回空列表；全部 unmatched 仍產出 record（標記 needs_review）
- [x] Edge Case: 所有 confidence < threshold 全部標記 needs_review；TransactionRecord.id 全局唯一
- [x] quantity > 1 時 notes 加 "數量: {quantity}"
- [x] Unit Test 34 個全部 PASS
- [x] 全套 165 tests PASS（無 regression）

## 結果

### 產出文件
| # | 文件路徑 | 用途 |
|---|----------|------|
| 1 | `output/assignment-017/src/builder/record_builder.py` | 主整合邏輯 |
| 2 | `output/assignment-017/tests/test_builder/test_record_builder.py` | 34 個 unit + integration tests |

### 實現摘要
- `build_records()`: 主入口，調用 matcher → extractor → group_by_time_window → resolve_payment_status → 組裝 TransactionRecord
- `records_to_json()`: 用 `model_dump(mode="json")` + `json.dumps` 序列化
- `json_to_records()`: 用 `json.loads` + `TransactionRecord(**item)` 反序列化
- Unmatched images 產出 needs_review=True 嘅 record（customer_name="Unknown"）
- 用 `id(extraction)` 做 pair_map key 避免 Pydantic model hashable 問題

### 測試覆蓋
| 類型 | 數量 | 說明 |
|------|------|------|
| Helper Unit Tests | 13 | _calculate_confidence, _determine_needs_review, _build_notes, _sum_quantity |
| JSON Serialization | 5 | round-trip, preserve ID, empty list, valid JSON |
| Happy Path Integration | 6 | single/multiple messages, 5+3 scenario, confidence, quantity, partial payment |
| Error Path | 4 | empty inputs, unmatched images, no matching filenames |
| Edge Cases | 5 | unique IDs, low confidence, pair flag, JSON after build, no quoted amount |

### 技術決策
1. **pair_map 用 id(extraction)** — ExtractionResult 係 Pydantic BaseModel，唔適合做 dict key（可能有相同值嘅 instance），用 Python object id 確保唯一性
2. **Unmatched images 產出 record** — 即使冇 message context，都產出 record 方便人工 review
3. **函數拆分** — 每個 private helper < 15 行，主函數 build_records 只有 flow control

## 備註
N/A

## Memory 已更新
✅

## Usage 估算
- **Context 使用率**: 40%
- **估算 Token 數**: ~12,000 input / ~6,000 output
- **接近限額警告**: ✅
