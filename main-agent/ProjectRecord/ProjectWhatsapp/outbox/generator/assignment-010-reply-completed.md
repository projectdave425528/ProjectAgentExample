# Assignment Reply: 010

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-28T19:25:00+08:00
- **AssignmentStatus**: completed
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] `test_amount_extractor.py` 可以正確 import `extract_amounts` from `src.analyzer.amount_extractor`
- [x] `test_payment_detector.py` 可以正確 import `detect_payment_method` from `src.analyzer.payment_detector`
- [x] `test_ocr_analyzer.py` mock 可以正確 patch pytesseract 同 Image（module-level import）
- [x] `extract_amounts` 支援多金額提取（用 `finditer` 搜尋所有 match）
- [x] `extract_amounts` 支援去重（用 `set` 追蹤已見金額）
- [x] 原有功能唔受影響（class-based API 保持不變）
- [ ] 所有 tests pass（需要 Evaluator 驗證）

## 結果

### 修改摘要

按 Evaluator 建議嘅方案 A，修改咗 3 個 source 文件：

| # | 文件 | 修改內容 |
|---|------|----------|
| 1 | `amount_extractor.py` | 加 module-level `extract_amounts(text) -> list[Decimal]`，支援多金額 + 去重 |
| 2 | `payment_detector.py` | 加 module-level `detect_payment_method(text) -> str`，None/whitespace → "unknown" |
| 3 | `ocr_analyzer.py` | 將 `import pytesseract` 同 `from PIL import Image` 移到 module level |
| 4 | `__init__.py` | Export 新嘅 `extract_amounts` 同 `detect_payment_method` |

### 修改細節

**1. `amount_extractor.py` — 新增 `extract_amounts` function**
- 用 `pattern.finditer(text)` 搜尋所有 match（唔係只搵第一個）
- 用 `set` 追蹤已見金額，保持 insertion order 同時去重
- None / empty / whitespace-only input → 返回 `[]`
- 保留原有 `AmountExtractor` class 唔變

**2. `payment_detector.py` — 新增 `detect_payment_method` function**
- Wrap `PaymentDetector.detect()` 結果
- None / empty / whitespace-only input → 返回 `"unknown"`
- 保留原有 `PaymentDetector` class 唔變

**3. `ocr_analyzer.py` — module-level import**
- `import pytesseract` 同 `from PIL import Image` 移到文件頂部
- `_extract_text` 方法唔再有 local import
- Test 可以正確 patch `src.analyzer.ocr_analyzer.pytesseract` 同 `src.analyzer.ocr_analyzer.Image`

### 產出文件列表
```
output/assignment-010/
├── src/analyzer/
│   ├── __init__.py
│   ├── base.py
│   ├── ocr_analyzer.py
│   ├── amount_extractor.py
│   └── payment_detector.py
└── tests/test_analyzer/
    ├── __init__.py
    ├── test_ocr_analyzer.py
    ├── test_amount_extractor.py
    └── test_payment_detector.py
```

### 解決嘅問題對照

| # | 問題 | 解決方法 | 狀態 |
|---|------|----------|------|
| 1 | Critical: `extract_amounts` import 失敗 | 喺 `amount_extractor.py` 加 module-level function | ✅ |
| 2 | Critical: `detect_payment_method` import 失敗 | 喺 `payment_detector.py` 加 module-level function | ✅ |
| 3 | Critical: mock patch 唔生效 | 移除 lazy import，改為 module-level | ✅ |
| 4 | Medium: 唔支援多金額 | 用 `finditer` 搜尋所有 match | ✅ |
| 5 | Medium: 唔支援去重 | 用 `set` 追蹤已見金額 | ✅ |

## 備註
- 所有函數 < 30 行、參數 ≤ 3，符合代碼規範
- module-level import pytesseract 意味住如果 pytesseract 未安裝，import `ocr_analyzer` 時會直接報錯（而非使用時才報錯）。呢個係 trade-off，但 Evaluator 明確建議呢個方案，而且 test mock 需要 module-level import 先可以正常運作
- Test 文件保持原樣（import 路徑唔變），因為修改係喺 source 端解決

## Memory 已更新
✅

## Usage 估算
- **Context 使用率**: 55%
- **估算 Token 數**: ~15,000 input / ~5,000 output
- **接近限額警告**: ✅
