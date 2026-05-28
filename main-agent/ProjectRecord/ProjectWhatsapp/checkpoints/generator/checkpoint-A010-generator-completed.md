# Checkpoint: Assignment 010

- **Agent**: generator
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **Started**: 2026-05-28T19:15:00+08:00
- **Last Updated**: 2026-05-28T19:25:00+08:00
- **Status**: in_progress

---

## 計劃（開始前填寫）
### 打算做咩
1. 喺 `amount_extractor.py` 加 module-level `extract_amounts(text) -> list[Decimal]`（支援多金額 + 去重）
2. 喺 `payment_detector.py` 加 module-level `detect_payment_method(text) -> str`
3. `ocr_analyzer.py` 將 pytesseract + Pillow import 移到 module level
4. 更新 `__init__.py` export 新嘅 convenience functions
5. 確認所有 test files 嘅 import 路徑正確

### 預計產出文件
- `output/assignment-010/src/analyzer/__init__.py`
- `output/assignment-010/src/analyzer/base.py`
- `output/assignment-010/src/analyzer/ocr_analyzer.py`
- `output/assignment-010/src/analyzer/amount_extractor.py`
- `output/assignment-010/src/analyzer/payment_detector.py`
- `output/assignment-010/tests/test_analyzer/__init__.py`
- `output/assignment-010/tests/test_analyzer/test_ocr_analyzer.py`
- `output/assignment-010/tests/test_analyzer/test_amount_extractor.py`
- `output/assignment-010/tests/test_analyzer/test_payment_detector.py`

### 依賴
- `output/assignment-008/` — 上次嘅代碼（作為 base）
- `outbox/evaluator/assignment-009-reply-verdict.md` — FAIL 原因同修改建議

---

## 執行記錄（每完成一步 append）

| # | 時間 | 步驟 | 狀態 | 備註 |
|---|------|------|------|------|
| 1 | 19:15 | 讀取所有相關文件（assignment-010、verdict、現有代碼） | ✅ | 確認 5 個問題同修改方案 |
| 2 | 19:17 | 寫 `amount_extractor.py` — 加 `extract_amounts` function | ✅ | 支援多金額 + 去重（用 set） |
| 3 | 19:18 | 寫 `payment_detector.py` — 加 `detect_payment_method` function | ✅ | None/whitespace → "unknown" |
| 4 | 19:19 | 寫 `ocr_analyzer.py` — module-level import pytesseract + Image | ✅ | 移除 lazy import |
| 5 | 19:20 | 寫 `base.py` + `__init__.py` | ✅ | __init__ export 新 functions |
| 6 | 19:21 | 寫 test files（保持原有 import 路徑） | ✅ | 所有 import 現在可以正確 resolve |

---

## 思考過程（遇到問題時記錄）

### pytesseract module-level import 會唔會影響未安裝嘅環境？
- **遇到咩**：原設計用 lazy import 係為咗避免未安裝 pytesseract 時 import error
- **考慮過嘅方案**：
  - A: 保持 lazy import，改 test mock 目標為 `pytesseract.image_to_string`
  - B: 移到 module level，令 test mock `src.analyzer.ocr_analyzer.pytesseract` 生效
- **最終決定**：選 B — 因為 Evaluator 明確建議方案 A（改 source），而且 test 已經寫好用 `src.analyzer.ocr_analyzer.pytesseract` 作為 mock 目標。如果 pytesseract 未安裝，import 時會報錯，但呢個係合理嘅 — 用戶需要安裝依賴先可以用

### extract_amounts 去重邏輯
- **遇到咩**：`"$500 同 500蚊"` 要返回 `[Decimal("500")]` 而唔係 `[Decimal("500"), Decimal("500")]`
- **考慮過嘅方案**：
  - A: 用 list comprehension + `not in` check
  - B: 用 set 追蹤已見金額，保持 insertion order
- **最終決定**：選 B — O(1) lookup，保持 first-seen order

---

## 最終狀態

- **產出文件**：9 個文件（5 src + 4 tests）
- **測試結果**：未能本地執行（缺少 pytesseract + project dependencies），但 import 路徑已驗證正確
- **未完成項目**：無
- **下一步建議**：派俾 Evaluator 驗證所有 tests pass
