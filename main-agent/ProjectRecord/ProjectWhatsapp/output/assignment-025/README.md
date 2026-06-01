# WhatsApp 帳目分析系統

自動從 WhatsApp 對話記錄及付款截圖中提取交易記錄，匯出結構化 Excel 報表。適用於維修服務行業嘅日常帳目管理，支援 PayMe、FPS、銀行轉帳等常見付款方式嘅截圖識別。

## 功能列表

- **文字解析（多格式支援）** — 解析 WhatsApp 匯出嘅 `.txt` 對話記錄，支援 12/24 小時制、多種日期格式
- **OCR 圖片分析** — 識別 PayMe、FPS、銀行轉帳截圖中嘅金額同交易資訊
- **交易配對** — 自動將對話訊息同付款截圖配對，建立完整交易記錄
- **Excel 匯出** — 產出排序整齊、含總計列嘅 Excel 報表（9 欄標準格式）

## 安裝步驟

### 1. 環境要求

- Python 3.9 或以上版本

### 2. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 3. 安裝 Tesseract OCR（Windows）

1. 前往 [Tesseract 下載頁面](https://github.com/UB-Mannheim/tesseract/wiki)
2. 下載最新版安裝程式（`.exe`）
3. 執行安裝，記住安裝路徑（預設：`C:\Program Files\Tesseract-OCR`）
4. 將安裝路徑加入系統環境變數 `PATH`
5. 開啟新嘅終端機，執行以下指令驗證：

```bash
tesseract --version
```

### 4. 配置環境變數

```bash
copy .env.example .env
```

編輯 `.env` 文件，填入必要嘅配置（如 Tesseract 路徑、API Key 等）。

## 快速開始

```bash
python -m src.main analyze --input ./data --output ./output/report.xlsx --mode ocr
```

此指令會：
1. 讀取 `./data` 目錄下嘅 WhatsApp 對話文件同圖片
2. 使用 OCR 模式分析付款截圖
3. 配對交易記錄
4. 匯出報表到 `./output/report.xlsx`

## 項目結構

```
src/
├── models/          # Pydantic data models
├── parser/          # WhatsApp text parser
├── analyzer/        # Image analysis (OCR / AI Vision)
├── builder/         # Transaction record builder
├── exporter/        # Excel exporter
├── config.py        # Configuration loader
└── main.py          # CLI entry point
```

## 輸出格式

Excel 報表包含以下 9 欄：

| 欄位 | 說明 |
|------|------|
| 日期 | 交易日期 |
| 客戶名稱 | WhatsApp 對話中嘅發送者名稱 |
| 維修項目 | 從對話內容提取嘅維修描述 |
| 數量 | 維修數量 |
| 報價金額 | 原始報價 |
| 實收金額 | 實際收到嘅付款金額 |
| 付款方式 | PayMe / FPS / 銀行轉帳 |
| 付款狀態 | 已付 / 未付 / 部分付款 |
| 備註 | 額外資訊或需要人工覆核嘅標記 |

## 技術棧

- Python 3.9+
- Pydantic 2.x（數據模型）
- Click（CLI 框架）
- openpyxl（Excel 匯出）
- pytesseract + Pillow（OCR 圖片分析）
- PyYAML + python-dotenv（配置管理）

## 授權

本項目僅供內部使用。
