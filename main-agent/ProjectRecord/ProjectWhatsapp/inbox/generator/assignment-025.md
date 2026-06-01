# Assignment 025

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-31T10:36:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 12: 文檔 + README
- **TaskID**: ProjectWhatsapp/Task-12
- **TaskStatus**: pending → in_progress

## 需求
撰寫用戶文檔同 README。包括安裝指南（含 Tesseract 安裝）、使用說明、配置說明、常見問題。文檔語言：中文。

需要建立：
- `README.md` — 項目簡介 + 安裝 + 快速開始
- `docs/usage.md` — 詳細使用說明

### README.md 內容要求
1. **項目簡介** — WhatsApp 帳目分析系統，自動從 WhatsApp 對話 + 付款截圖提取交易記錄
2. **功能列表** — 文字解析、OCR 圖片分析、交易配對、Excel 匯出
3. **安裝步驟**：
   - Python 3.9+ 要求
   - `pip install -r requirements.txt`
   - Tesseract OCR 安裝（Windows）
   - `.env` 配置
4. **快速開始** — 一個完整嘅使用範例：
   ```
   python -m src.main analyze --input ./data --output ./output/report.xlsx --mode ocr
   ```
5. **項目結構** — 列出 src/ 目錄結構

### docs/usage.md 內容要求
1. **詳細使用說明** — 所有 CLI 參數解釋
2. **配置選項** — config.yaml 所有欄位說明
3. **輸出格式說明** — Excel 欄位定義
4. **Tesseract 安裝指南（Windows）** — 下載連結 + 環境變數設置
5. **AI Vision API 配置指南** — API Key 設置（雖然未實現，但預留文檔）
6. **常見問題 FAQ** — 至少 5 個 Q&A

### 注意事項
- 文檔語言全部中文
- 確認所有文件路徑引用同實際目錄結構一致
- 確認所有依賴版本同 requirements.txt 一致
- CLI 命令範例要可以真正運行

## Context
- 技術棧：Python 3.9+、Click、openpyxl、pytesseract、Pydantic v2
- CLI 命令：`python -m src.main analyze --input <folder> --output <file> --mode <ocr|ai_vision> [--config <path>] [--verbose]`
- 代碼輸出位置：`ProjectRecord/ProjectWhatsapp/output/assignment-025/`

## 驗證標準
- [ ] README.md 包含：項目簡介、功能列表、安裝步驟、快速開始
- [ ] docs/usage.md 包含：詳細使用說明、配置選項、輸出格式說明
- [ ] Tesseract 安裝指南（Windows）
- [ ] AI Vision API 配置指南
- [ ] 常見問題 FAQ（至少 5 個）
- [ ] 文檔語言：中文
- [ ] 所有文件路徑引用同實際目錄結構一致

## 預期輸出
完整文檔文件，放喺 `ProjectRecord/ProjectWhatsapp/output/assignment-025/` 目錄：
- `README.md`
- `docs/usage.md`
