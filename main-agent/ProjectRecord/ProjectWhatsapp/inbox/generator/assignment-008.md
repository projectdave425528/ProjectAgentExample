# Assignment 008

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-28T15:00:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **TaskStatus**: pending → in_progress

## 需求
實現圖片分析器嘅 abstract base class 同 Tesseract OCR 模式。包括圖片讀取、OCR 文字提取、金額識別、付款方式偵測。Base class 定義 interface 方便 mock。

必須同時提供 unit test（pytest），mock Tesseract 同 Pillow。

## Context
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Tasks Spec：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 4）
- Task 1 代碼（models）：`./ProjectRecord/ProjectWhatsapp/output/assignment-002/src/models/`
- 技術棧：Python 3.9+、pytest、pytesseract、Pillow
- 代碼輸出位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-008/`

### 依賴嘅已完成代碼
- `src/models/image_result.py` — ImageAnalysisResult model
- `src/models/config.py` — AppConfig model

### 設計要求
1. `base.py` — Abstract base class `ImageAnalyzerBase`，定義 `analyze(image_path: str, config: AppConfig) -> ImageAnalysisResult`
2. `ocr_analyzer.py` — 繼承 base class，用 pytesseract + Pillow 實現 OCR
3. `amount_extractor.py` — 從 OCR 文字提取金額（$500、HK$1,000.50、500蚊 等）
4. `payment_detector.py` — 從 OCR 文字識別付款方式（PayMe/FPS/銀行轉帳）

### 金額格式支援
- `$500`、`$500.00`
- `HK$500`、`HK$1,000.50`
- `500蚊`、`500元`
- 千位分隔符：`$1,000`、`$10,000.50`

### 付款方式關鍵字
- PayMe：「PayMe」「payme」「Pay Me」
- FPS：「FPS」「轉數快」「Faster Payment」
- 銀行轉帳：「銀行」「bank transfer」「匯款」「轉帳」

## 驗證標準
- [ ] `base.py` 定義 `ImageAnalyzerBase` abstract class
- [ ] `ocr_analyzer.py` 實現 Tesseract OCR 分析（繼承 base class）
- [ ] 支援 JPG、PNG、WEBP 格式讀取
- [ ] `amount_extractor.py` 從 OCR 文字提取金額
- [ ] `payment_detector.py` 識別 PayMe/FPS/銀行轉帳截圖
- [ ] 單張圖片分析失敗時返回 error result（唔 raise exception）
- [ ] 信心度計算邏輯

## Test Criteria
- **Happy Path**: mock Tesseract 返回 "HK$500.00 PayMe" 時正確提取 amount=500.00, payment_method="payme"；mock 返回含 FPS 關鍵字文字時識別為 fps
- **Error Path**: 圖片文件唔存在時返回 ImageAnalysisResult(error="無法讀取文件") 而非 raise exception；Tesseract 未安裝時返回明確 error message
- **Edge Case**: 金額含千位分隔符 "$1,000.50" 正確提取為 1000.50；OCR 返回空字串時 confidence=0.0 且 needs_review=True；WEBP 格式圖片正確讀取

## 預期輸出
```
output/assignment-008/
├── src/
│   └── analyzer/
│       ├── __init__.py
│       ├── base.py
│       ├── ocr_analyzer.py
│       ├── amount_extractor.py
│       └── payment_detector.py
└── tests/
    └── test_analyzer/
        ├── __init__.py
        ├── test_ocr_analyzer.py
        ├── test_amount_extractor.py
        └── test_payment_detector.py
```
