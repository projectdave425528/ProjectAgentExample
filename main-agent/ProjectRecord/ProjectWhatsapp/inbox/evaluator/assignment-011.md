# Assignment 011

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-28T19:30:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 4: Image Analyzer — Base + OCR 模式
- **TaskID**: ProjectWhatsapp/Task-4
- **TaskStatus**: in_progress（FAIL 修改後重新評估）

## 需求
重新審查 Generator 修改後嘅 Task 4 代碼。上次 FAIL (72/100) 嘅 3 個 Critical + 2 個 Medium 問題已修改。

## Context
- 修改後代碼位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-010/`
- 上次 FAIL 原因：`./ProjectRecord/ProjectWhatsapp/outbox/evaluator/assignment-009-reply-verdict.md`
- Generator 修改回覆：`./ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-010-reply-completed.md`
- FAIL 次數：1/3

### 修改重點
1. `amount_extractor.py` 加咗 module-level `extract_amounts(text) -> list[Decimal]`（多金額 + 去重）
2. `payment_detector.py` 加咗 module-level `detect_payment_method(text) -> str`
3. `ocr_analyzer.py` 將 pytesseract + Pillow import 移到 module level

## 驗證標準
- [ ] 上次 5 個問題全部解決
- [ ] 所有 tests 嘅 import 路徑正確
- [ ] mock patch 可以正常生效
- [ ] extract_amounts 支援多金額 + 去重
- [ ] 原有功能唔受影響
- [ ] 函數 < 30 行、參數 ≤ 3

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分
