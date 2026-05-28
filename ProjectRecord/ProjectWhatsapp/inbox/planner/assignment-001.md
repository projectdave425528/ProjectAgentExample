# Assignment 001

- **From**: main-agent
- **To**: planner
- **Timestamp**: 2026-05-28T10:00:00+08:00
- **Type**: plan-request
- **TaskRef**: Task 1: WhatsApp 帳目分析系統
- **TaskID**: ProjectWhatsapp/Task-1
- **TaskStatus**: pending

## 需求
根據用戶需求，產出 requirements.md、design.md、tasks.md。

用戶係手機維修員，需要一個系統處理 WhatsApp 匯出嘅對話紀錄（.txt + 圖片），自動分析並整合成客戶交易紀錄，最終匯出 Excel。

### 四個核心模組：
1. **WhatsApp 文字解讀器**  解析 .txt 匯出文件，提取時間戳、發送者、訊息內容
2. **圖片分析器**  OCR/AI Vision 分析轉帳截圖，提取金額、日期、交易資訊
3. **交易紀錄整合器**  配對對話同圖片，整合成結構化客戶交易文檔
4. **Excel 匯出器**  將交易紀錄匯出為 .xlsx 格式

### 技術背景：
- WhatsApp 匯出格式：.txt（每行 [時間戳] 發送者: 內容）+ 圖片（IMG-YYYYMMDD-WANNNN.jpg）
- 圖片引用：<attached: IMG-YYYYMMDD-WANNNN.jpg>
- 對話語言：廣東話 / 中文混合
- 圖片類型：轉帳截圖（PayMe/FPS）、手機損壞相片、報價單
- 建議技術棧：Python

### Excel 輸出欄位（建議）：
- 日期、客戶名稱、維修項目、報價金額、實收金額、付款方式、付款狀態、備註

## Context
- 當前 Project: ProjectWhatsapp
- 用戶係手機維修員，帳目混亂需要系統化
- 需要支援中文 OCR（轉帳截圖）
- 圖片分析建議支援多方案（AI Vision API + Tesseract fallback）

## 預期輸出
- [ ] requirements.md  功能需求 + 非功能需求 + 用戶故事
- [ ] design.md  系統架構 + 模組設計 + 數據流 + 技術選型
- [ ] tasks.md  拆解為可執行任務（每個 task 有 acceptance criteria）

## 預期格式
請將產出寫入 ProjectRecord/ProjectWhatsapp/outbox/planner/assignment-001-reply-completed.md
