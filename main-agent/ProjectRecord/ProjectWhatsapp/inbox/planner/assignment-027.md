# Assignment 027

- **From**: main-agent
- **To**: planner
- **Timestamp**: 2026-06-05T13:20:00+08:00
- **Type**: plan-request

## 需求

用戶想了解：**可唔可以用 CodeGraph（已有嘅 code graph / 代碼知識圖譜）嘅數據，設計一個自動化測試系統？**

背景：
1. 用戶已有一個 WhatsApp 對話分析系統（Python + pytest），CodeGraph 已索引咗 139 個文件、2145 nodes、3813 edges
2. 用戶之前討論過 Data-Driven / Keyword-Driven / State-Aware 自動化測試方向
3. CodeGraph 提供：symbol search、callers/callees 關係、impact analysis、file tree
4. 用戶想知道能否利用呢啲資訊自動生成 test cases、發現未測試嘅 code paths、偵測 regression 風險

## Context

- 當前 Project：ProjectWhatsapp
- 技術棧：Python、pytest、Playwright（考慮中）
- CodeGraph 提供嘅工具：codegraph_explore、codegraph_search、codegraph_callers、codegraph_callees、codegraph_impact、codegraph_files
- 已有嘅 code 結構：parser（text_parser, patterns）、analyzer（ocr_analyzer, amount_extractor, payment_detector）、builder（record_builder）、exporter（excel_exporter）、matcher

## 預期輸出

請產出一份規劃文件（放入 `./ProjectRecord/ProjectWhatsapp/UserDocument/codegraph-auto-testing-plan.md`），內容包括：

1. **可行性分析**：CodeGraph 嘅數據能做到咩程度嘅自動化測試
2. **設計方案**：點樣利用 callers/callees + impact graph 自動生成 test coverage 報告、發現未測試路徑
3. **實作建議**：建議嘅工具鏈 + 架構圖
4. **限制同風險**：呢個方法嘅 limitations
5. **同其他方法嘅對比**：vs 傳統 coverage tool（pytest-cov）、vs 純 data-driven testing

注意：呢份係研究 / 規劃文件，唔係要寫 code。用英文撰寫。
