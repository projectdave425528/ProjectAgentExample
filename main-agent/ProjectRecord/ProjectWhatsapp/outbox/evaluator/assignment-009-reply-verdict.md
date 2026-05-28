# Assignment Reply: 009

- **From**: evaluator
- **To**: main-agent
- **Timestamp**: 2026-05-28T18:45:00+08:00
- **AssignmentStatus**: verdict-fail
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **TaskStatus**: in_progress（FAIL，需要修改）

## 驗證標準
- [x] `base.py` 定義 `ImageAnalyzerBase` abstract class
- [x] `ocr_analyzer.py` 繼承 base class，實現 Tesseract OCR 分析
- [x] 支援 JPG、PNG、WEBP 格式
- [x] `amount_extractor.py` 從 OCR 文字提取金額（$、HK$、千位分隔符、蚊、元）
- [x] `payment_detector.py` 識別 PayMe/FPS/銀行轉帳
- [x] 單張圖片分析失敗返回 error result（唔 raise exception）
- [x] 信心度計算邏輯合理
- [ ] Unit test mock Tesseract + Pillow，覆蓋 Happy Path + Error Path + Edge Case ← FAIL
- [x] 函數 < 30 行、參數 ≤ 3

## 結果

### 評分：72/100

| 類別 | 得分 | 權重 | 加權分 |
|------|------|------|--------|
| 功能性 | 90 | 30% | 27.0 |
| 代碼品質 | 88 | 25% | 22.0 |
| 安全性 | 85 | 20% | 17.0 |
| 可測試性 | 30 | 15% | 4.5 |
| 可維護性 | 85 | 10% | 8.5 |

**總分：79.0 → 調整為 72**（因為 tests 全部無法執行屬 Critical Test 問題，扣 7 分）

### 優點
1. **base.py 設計正確** — 用 ABC + @abstractmethod，interface 清晰，方便 Task 5 擴展
2. **OcrAnalyzer 永遠唔 raise** — 所有 error path 都返回 error result，符合需求
3. **AmountExtractor 支援所有格式** — $、HK$、千位分隔符、蚊、元，pattern 排序合理（specific → general）
4. **PaymentDetector keyword matching 完整** — PayMe/FPS/銀行轉帳，priority order 正確
5. **Confidence 計算邏輯合理** — base 0.3 + amount 0.35 + payment 0.35 = max 1.0
6. **Lazy import pytesseract/Pillow** — 避免未安裝時 import error，設計考慮周到
7. **函數行數同參數數都符合標準** — 所有函數 < 30 行、參數 ≤ 3

### 必須修改（Critical）

| # | 問題 | 位置 | 嚴重程度 | 修改建議 |
|---|------|------|----------|----------|
| 1 | test_amount_extractor.py import 路徑錯誤 | `test_amount_extractor.py:6` | Critical | `extract_amounts` 唔存在於 `src.analyzer.amount_extractor`。應改為 `from src.analyzer.ocr_analyzer import extract_amounts`，或者喺 `amount_extractor.py` 加一個 module-level `extract_amounts` function |
| 2 | test_payment_detector.py import 路徑錯誤 | `test_payment_detector.py:4` | Critical | `detect_payment_method` 唔存在於 `src.analyzer.payment_detector`。應改為 `from src.analyzer.ocr_analyzer import detect_payment_method`，或者喺 `payment_detector.py` 加一個 module-level `detect_payment_method` function |
| 3 | test_ocr_analyzer.py mock 目標錯誤 | `test_ocr_analyzer.py` 全部 test | Critical | `pytesseract` 同 `Image` 係 lazy import（喺 `_extract_text` function 入面 import），module-level patch `src.analyzer.ocr_analyzer.pytesseract` 唔會生效。需要改為 patch `pytesseract.image_to_string` 同 `PIL.Image.open`，或者將 import 移到 module level |
| 4 | extract_amounts 唔支援多金額提取 | `ocr_analyzer.py:21-23` | Medium | Test 期望 `extract_amounts("報價 $500 實收 HK$450.00")` 返回兩個金額，但實際只返回第一個。需要改 `AmountExtractor` 支援 `extract_all` 或改 `extract_amounts` wrapper |
| 5 | extract_amounts 唔支援去重 | `ocr_analyzer.py:21-23` | Medium | Test `test_no_duplicate_amounts` 期望 `"$500 同 500蚊"` 只返回一個 500，但目前冇去重邏輯 |

### 修改優先順序
1. **Critical（必須修改）**：問題 1-3 — Test import/mock 錯誤導致所有 tests 無法執行
2. **Medium（建議修改）**：問題 4-5 — Test 期望同實際行為唔一致

### 建議修改方案

**方案 A（推薦）— 改 source code 加 convenience functions：**
1. 喺 `amount_extractor.py` 底部加：
   ```python
   _extractor = AmountExtractor()
   def extract_amounts(text: str) -> list[Decimal]:
       if not text or not text.strip():
           return []
       results = []
       seen = set()
       for pattern in _AMOUNT_PATTERNS:
           for match in pattern.finditer(text):
               amount = _extractor._parse_amount(match.group(1))
               if amount and amount not in seen:
                   results.append(amount)
                   seen.add(amount)
       return results
   ```
2. 喺 `payment_detector.py` 底部加：
   ```python
   _detector = PaymentDetector()
   def detect_payment_method(text: str) -> str:
       result = _detector.detect(text)
       return result if result is not None else "unknown"
   ```
3. 將 `ocr_analyzer.py` 嘅 `_extract_text` 入面嘅 import 移到 module level，或者改 test mock 目標為 `pytesseract.image_to_string` 同 `PIL.Image.open`

**方案 B — 改 test import 路徑：**
1. `test_amount_extractor.py` 改為 `from src.analyzer.ocr_analyzer import extract_amounts`
2. `test_payment_detector.py` 改為 `from src.analyzer.ocr_analyzer import detect_payment_method`
3. 但仍需解決 extract_amounts 唔支援多金額/去重嘅問題

## 備註
- 源代碼本身品質好，設計合理，問題集中喺 test 同 source 嘅 interface 唔一致
- Generator reply 提到「修正咗 import 問題」但修正唔完整 — convenience wrappers 放喺 ocr_analyzer.py 但 tests 仍然 import from 原始模組
- 建議用方案 A，因為每個模組有自己嘅 public API 係更好嘅設計

## Memory 已更新
✅

## Usage 估算
- **Context 使用率**: 45%
- **估算 Token 數**: ~12,000 input / ~4,000 output
- **接近限額警告**: ✅
