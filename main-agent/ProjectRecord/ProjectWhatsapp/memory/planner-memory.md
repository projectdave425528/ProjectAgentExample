# Planner Memory — ProjectWhatsapp

## 最近任務
| # | 日期 | 任務摘要 | 結果 | 學到咩 |
|---|------|---------|------|--------|
| 1 | 2026-05-28 | 重寫全部 Specs（requirements/design/tasks） | completed | 每個 Task 必須有 Test Criteria（H+E+Edge）；template 格式要嚴格遵守；Input/Output 定義要明確 |

## 重要教訓（永久）
（空 — 下次任務後由 Agent 自行填入）

## 項目知識
- 技術棧：Python 3.9+、Pydantic v2、Click、openpyxl、pytesseract、OpenAI Vision API
- 架構：Pipeline（TextParser → ImageAnalyzer → RecordBuilder → ExcelExporter）
- 12 個 Tasks，P0 有 9 個，P1 有 2 個，P2 有 1 個
- 每個模組透過 Pydantic data model 通訊，可獨立 unit test
- Base class + interface 設計方便 mock 外部依賴（Tesseract、OpenAI API）

## 常見問題
- WhatsApp 匯出格式有多種變體（時間格式、日期順序），需要支援所有已知格式
- 廣東話金額表達（「三百蚊」）需要特殊處理
- OCR 中文準確度有限，需要 confidence threshold + needs_review 機制
- Tesseract 喺 Windows 安裝較複雜，需要提供詳細指南
