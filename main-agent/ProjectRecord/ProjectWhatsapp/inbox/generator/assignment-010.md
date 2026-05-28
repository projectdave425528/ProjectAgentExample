# Assignment 010

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-28T19:00:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **TaskStatus**: in_progress（FAIL 重做）

## 需求
修改 Task 4 代碼，解決 Evaluator 指出嘅問題。源代碼品質好，問題集中喺 test 同 source 嘅 interface 唔一致。

## Context
- 上次代碼：`./ProjectRecord/ProjectWhatsapp/output/assignment-008/`
- Evaluator FAIL 原因（Assignment 009）：
  1. **Critical** — `test_amount_extractor.py` import `extract_amounts` from `src.analyzer.amount_extractor`，但該函數唔存在
  2. **Critical** — `test_payment_detector.py` import `detect_payment_method` from `src.analyzer.payment_detector`，但該函數唔存在
  3. **Critical** — `test_ocr_analyzer.py` mock `src.analyzer.ocr_analyzer.pytesseract` 同 `Image`，但實際係 lazy import（function 入面），module-level patch 唔生效
  4. **Medium** — `extract_amounts` 唔支援多金額提取（test 期望返回多個金額）
  5. **Medium** — `extract_amounts` 唔支援去重（test 期望 "$500 同 500蚊" 只返回一個 500）
- FAIL 次數：1/3

## Evaluator 建議修改方案（方案 A，推薦）
1. 喺 `amount_extractor.py` 加 module-level `extract_amounts(text) -> list[Decimal]` function（支援多金額 + 去重）
2. 喺 `payment_detector.py` 加 module-level `detect_payment_method(text) -> str` function
3. 將 `ocr_analyzer.py` 嘅 pytesseract + Pillow import 移到 module level（唔好 lazy import），令 test mock 可以正常 patch

## 驗證標準
- [ ] `test_amount_extractor.py` 可以正確 import `extract_amounts` from `src.analyzer.amount_extractor`
- [ ] `test_payment_detector.py` 可以正確 import `detect_payment_method` from `src.analyzer.payment_detector`
- [ ] `test_ocr_analyzer.py` mock 可以正確 patch pytesseract 同 Image
- [ ] `extract_amounts` 支援多金額提取
- [ ] `extract_amounts` 支援去重
- [ ] 所有 tests pass
- [ ] 原有功能唔受影響

## 預期輸出
修改後嘅代碼文件，放喺 `./ProjectRecord/ProjectWhatsapp/output/assignment-010/`（同 assignment-008 相同結構）
