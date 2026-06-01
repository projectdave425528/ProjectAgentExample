# Assignment 020

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-30T18:40:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 9: Excel Exporter
- **TaskID**: ProjectWhatsapp/Task-9
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 9 代碼（excel_exporter.py + formatters.py）。只做 Code Review，唔使跑 test — 已確認 240/240 pass。

## Context
- 代碼位置：
  - `ProjectRecord/ProjectWhatsapp/test-env/src/exporter/excel_exporter.py`
  - `ProjectRecord/ProjectWhatsapp/test-env/src/exporter/formatters.py`
- 已確認 Test 結果：240 passed（含 43 個 exporter tests）

## 評估重點
1. 代碼質量：函數 < 30 行？參數 ≤ 3？type hints + docstrings？
2. 功能完整性：排序、總計行、表頭格式、欄寬調整
3. Formatters 正確性：金額格式、付款方式/狀態中文化
4. 錯誤處理：ExportError、None 金額處理

## 驗證標準
- [ ] export_to_excel 正確產出 .xlsx
- [ ] 9 欄表頭正確
- [ ] 排序邏輯正確（date / customer_name）
- [ ] 總計行正確計算
- [ ] 表頭格式（粗體 + 背景色）
- [ ] formatters 所有函數正確
- [ ] ExportError 處理目錄唔存在
- [ ] 函數 < 30 行、參數 ≤ 3

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 簡短問題清單
