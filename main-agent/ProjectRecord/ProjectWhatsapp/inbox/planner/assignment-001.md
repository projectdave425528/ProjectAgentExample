# Assignment 001

- **From**: main-agent
- **To**: planner
- **Timestamp**: 2026-05-28T10:00:00+08:00
- **Type**: plan-request
- **TaskRef**: N/A（全 Specs 重寫）
- **TaskID**: ProjectWhatsapp/Specs-Rewrite
- **TaskStatus**: pending → in_progress

## 需求
用戶要求重寫 ProjectWhatsapp 嘅所有 Specs（requirements.md、design.md、tasks.md）。

項目係一個 **WhatsApp 帳目分析系統**：
- Python 桌面工具，專為手機維修員設計
- 讀取 WhatsApp 匯出嘅對話紀錄（.txt）同圖片
- 自動分析內容，整合成結構化嘅客戶交易紀錄
- 匯出 Excel 報表

用戶改咗 Agent 嘅條件（Planner 嘅 steering 已更新），所以需要重新按照最新嘅 template 格式同規則重寫所有 Specs。

## Context
- 現有 Specs 位置：`./ProjectRecord/ProjectWhatsapp/specs/`
- Template 位置：`./ProjectRecord/templates/specs/`
- 現有 requirements.md、design.md、tasks.md 已有完整內容（可參考但需重寫）
- Planner 嘅新規則要求：每個 Task 必須可獨立 Unit Test、必須有 Test Criteria（Happy Path + Error Path + Edge Case）
- 輸出必須嚴格遵守 template 格式

## 驗證標準
- [ ] requirements.md 按 requirements-template.md 格式重寫
- [ ] design.md 按 design-template.md 格式重寫
- [ ] tasks.md 按 tasks-template.md 格式重寫，每個 Task 有 Test Criteria
- [ ] 所有 Specs 內容完整覆蓋原有功能需求
- [ ] Tasks 之間依賴關係清晰
- [ ] 每個 Task 有明確嘅 Input/Output/Edge Cases

## 預期輸出
重寫後嘅三份 Specs 文件，寫入 `./ProjectRecord/ProjectWhatsapp/specs/`：
- requirements.md
- design.md
- tasks.md
