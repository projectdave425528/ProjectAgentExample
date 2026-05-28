# Assignment 009

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-28T18:30:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 4 代碼：Image Analyzer Base Class + OCR 模式 + Amount Extractor + Payment Detector + Unit Tests。

## Context
- 代碼位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-008/`
- 原始需求：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 4 section）
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Generator 回覆：`./ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-008-reply-completed.md`
- 技術棧：Python 3.9+、pytest、pytesseract、Pillow

### 代碼文件清單
```
output/assignment-008/
├── src/
│   └── analyzer/
│       ├── __init__.py
│       ├── base.py              (ImageAnalyzerBase abstract class)
│       ├── ocr_analyzer.py      (OcrAnalyzer - Tesseract + Pillow)
│       ├── amount_extractor.py  (AmountExtractor - $, HK$, 蚊, 元)
│       └── payment_detector.py  (PaymentDetector - PayMe/FPS/銀行)
└── tests/
    └── test_analyzer/
        ├── __init__.py
        ├── test_ocr_analyzer.py
        ├── test_amount_extractor.py
        └── test_payment_detector.py
```

## 驗證標準
- [ ] `base.py` 定義 `ImageAnalyzerBase` abstract class
- [ ] `ocr_analyzer.py` 繼承 base class，實現 Tesseract OCR 分析
- [ ] 支援 JPG、PNG、WEBP 格式
- [ ] `amount_extractor.py` 從 OCR 文字提取金額（$、HK$、千位分隔符、蚊、元）
- [ ] `payment_detector.py` 識別 PayMe/FPS/銀行轉帳
- [ ] 單張圖片分析失敗返回 error result（唔 raise exception）
- [ ] 信心度計算邏輯合理
- [ ] Unit test mock Tesseract + Pillow，覆蓋 Happy Path + Error Path + Edge Case
- [ ] 函數 < 30 行、參數 ≤ 3

## Test Criteria（從 Planner Specs）
- **Happy Path**: mock Tesseract 返回 "HK$500.00 PayMe" → amount=500.00, payment_method="payme"
- **Error Path**: 圖片唔存在 → error result（唔 raise）；Tesseract 未安裝 → 明確 error
- **Edge Case**: "$1,000.50" → 1000.50；OCR 空字串 → confidence=0.0, needs_review=True

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
