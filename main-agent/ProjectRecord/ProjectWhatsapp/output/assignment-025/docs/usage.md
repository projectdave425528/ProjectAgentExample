# 使用指南

## CLI 參數

```bash
python -m src.main analyze [OPTIONS]
```

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `--input` | PATH | ✅ | — | 輸入目錄路徑，包含 WhatsApp 對話文件（`.txt`）同付款截圖（`.jpg`/`.png`） |
| `--output` | PATH | ✅ | — | 輸出 Excel 文件路徑（例如 `./output/report.xlsx`） |
| `--mode` | TEXT | ❌ | `ocr` | 分析模式：`ocr`（本地 Tesseract）或 `vision`（AI Vision API，預留） |
| `--config` | PATH | ❌ | `./config.yaml` | 自定義配置文件路徑 |
| `--verbose` | FLAG | ❌ | `False` | 啟用詳細日誌輸出，顯示每個步驟嘅處理細節 |

### 使用範例

基本用法：

```bash
python -m src.main analyze --input ./data --output ./output/report.xlsx
```

指定配置文件 + 詳細日誌：

```bash
python -m src.main analyze --input ./data --output ./output/report.xlsx --config ./my-config.yaml --verbose
```

僅使用文字解析（唔做 OCR）：

```bash
python -m src.main analyze --input ./data --output ./output/report.xlsx --mode text
```

---

## 配置選項

系統支援 `config.yaml` 配置文件，欄位如下：

```yaml
# Tesseract OCR 執行檔路徑
tesseract_path: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# OpenAI API Key（AI Vision 模式用，預留功能）
openai_api_key: ""

# OCR 識別信心度閾值（0.0 - 1.0）
# 低於此值嘅識別結果會標記為 needs_review
confidence_threshold: 0.7

# 時間窗口（小時）
# 同一客戶喺此時間範圍內嘅訊息會被歸為同一筆交易
time_window_hours: 2
```

### 配置優先順序

1. 環境變數（最高優先）
2. `config.yaml` 文件
3. 程式內建預設值

### 環境變數對應

| config.yaml 欄位 | 環境變數 | 說明 |
|-------------------|----------|------|
| `tesseract_path` | `TESSERACT_PATH` | Tesseract 執行檔路徑 |
| `openai_api_key` | `OPENAI_API_KEY` | OpenAI API Key |
| `confidence_threshold` | `CONFIDENCE_THRESHOLD` | 信心度閾值 |
| `time_window_hours` | `TIME_WINDOW_HOURS` | 時間窗口 |

---

## 輸出格式

### Excel 報表欄位定義

匯出嘅 Excel 文件包含以下 9 欄：

| # | 欄位名稱 | 數據類型 | 說明 | 範例 |
|---|----------|----------|------|------|
| 1 | 日期 | 日期 | 交易發生日期 | 2026-05-30 |
| 2 | 客戶名稱 | 文字 | WhatsApp 對話中嘅發送者名稱 | 陳先生 |
| 3 | 維修項目 | 文字 | 從對話內容提取嘅維修描述 | 冷氣機維修 |
| 4 | 數量 | 數字 | 維修項目數量 | 1 |
| 5 | 報價金額 | 金額 | 原始報價金額（格式：X.00） | 500.00 |
| 6 | 實收金額 | 金額 | 實際收到嘅付款金額（格式：X.00） | 500.00 |
| 7 | 付款方式 | 文字 | 付款渠道 | PayMe |
| 8 | 付款狀態 | 文字 | 付款完成狀態 | 已付 |
| 9 | 備註 | 文字 | 額外資訊或需人工覆核標記 | needs_review |

### 報表結構

- **標題列**：第 1 行為欄位標題
- **數據列**：第 2 行起為交易記錄，按日期排序
- **總計列**：最後一行顯示「總計」，包含報價金額同實收金額嘅加總
- **欄寬**：自動調整（最小 10、最大 30 字元寬度）

---

## Tesseract 安裝指南（Windows）

### 步驟 1：下載

前往 [UB Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)，下載最新版 Windows 安裝程式（`.exe`）。

### 步驟 2：安裝

1. 執行下載嘅安裝程式
2. 安裝路徑建議使用預設：`C:\Program Files\Tesseract-OCR`
3. 安裝時勾選需要嘅語言包（建議勾選 `Chinese - Traditional` 同 `Chinese - Simplified`）
4. 完成安裝

### 步驟 3：設定環境變數

1. 開啟「系統內容」→「進階系統設定」→「環境變數」
2. 喺「系統變數」中搵到 `Path`，點擊「編輯」
3. 新增一行：`C:\Program Files\Tesseract-OCR`
4. 確認儲存

或者用 PowerShell（需要管理員權限）：

```powershell
$path = [Environment]::GetEnvironmentVariable("Path", "Machine")
$newPath = $path + ";C:\Program Files\Tesseract-OCR"
[Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
```

### 步驟 4：驗證安裝

開啟新嘅終端機（必須重新開啟先會載入新嘅 PATH），執行：

```bash
tesseract --version
```

預期輸出類似：

```
tesseract v5.x.x
 leptonica-x.xx.x
  ...
```

### 配置文件設定

喺 `config.yaml` 或 `.env` 中指定路徑：

```yaml
# config.yaml
tesseract_path: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

```env
# .env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## AI Vision API 配置

> ⚠️ 此功能為預留功能，尚未實現。以下為未來啟用時嘅配置方式。

### 設置 OPENAI_API_KEY

1. 前往 [OpenAI Platform](https://platform.openai.com/api-keys) 建立 API Key
2. 喺 `.env` 文件中設定：

```env
OPENAI_API_KEY=sk-your-api-key-here
```

或喺 `config.yaml` 中設定：

```yaml
openai_api_key: "sk-your-api-key-here"
```

### 使用 Vision 模式

```bash
python -m src.main analyze --input ./data --output ./output/report.xlsx --mode vision
```

### 注意事項

- Vision 模式會將圖片發送到 OpenAI API 進行分析，請確保網絡連接正常
- 每次 API 調用會產生費用，請留意用量
- 建議先用 OCR 模式處理大部分圖片，只對 OCR 信心度低嘅圖片使用 Vision 模式
- API Key 請妥善保管，唔好提交到版本控制系統

---

## FAQ

### 1. Tesseract 找不到（tesseract is not installed or it's not in your PATH）

**原因**：Tesseract 未安裝或未加入系統 PATH。

**解決方法**：
1. 確認已安裝 Tesseract（參考上方安裝指南）
2. 確認安裝路徑已加入系統 PATH
3. 重新開啟終端機（PATH 更新需要新嘅 session 先生效）
4. 如果唔想改 PATH，可以喺 `config.yaml` 直接指定完整路徑：
   ```yaml
   tesseract_path: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
   ```

### 2. 中文識別亂碼

**原因**：Tesseract 未安裝中文語言包。

**解決方法**：
1. 重新執行 Tesseract 安裝程式，勾選 `Chinese - Traditional`（chi_tra）同 `Chinese - Simplified`（chi_sim）語言包
2. 或者手動下載語言包文件（`.traineddata`），放到 Tesseract 嘅 `tessdata` 目錄：
   ```
   C:\Program Files\Tesseract-OCR\tessdata\chi_tra.traineddata
   C:\Program Files\Tesseract-OCR\tessdata\chi_sim.traineddata
   ```
3. 確認語言包已安裝：
   ```bash
   tesseract --list-langs
   ```
   輸出應包含 `chi_tra` 同 `chi_sim`

### 3. Excel 文件打不開（檔案損壞或格式不正確）

**原因**：可能係文件寫入過程中斷，或 openpyxl 版本問題。

**解決方法**：
1. 確認 openpyxl 版本 ≥ 3.1：
   ```bash
   pip show openpyxl
   ```
2. 如果版本過舊，升級：
   ```bash
   pip install --upgrade openpyxl
   ```
3. 確認輸出路徑嘅目錄存在（程式會自動建立，但權限問題可能導致失敗）
4. 嘗試用其他 Excel 軟件開啟（LibreOffice Calc、Google Sheets）
5. 如果問題持續，刪除舊文件後重新執行

### 4. 圖片格式不支援

**原因**：系統目前支援 `.jpg`、`.jpeg`、`.png` 格式嘅圖片。

**解決方法**：
1. 確認圖片為支援嘅格式（`.jpg`、`.jpeg`、`.png`）
2. 如果圖片為其他格式（`.heic`、`.webp`、`.bmp`），請先轉換為 PNG 或 JPG：
   ```bash
   # 使用 Pillow 轉換（Python）
   python -c "from PIL import Image; Image.open('photo.heic').save('photo.png')"
   ```
3. 確認圖片文件未損壞（可以用圖片檢視器正常開啟）
4. WhatsApp 匯出嘅圖片通常為 JPG 格式，正常情況下唔會有格式問題

### 5. 大文件處理緩慢或記憶體不足

**原因**：大量圖片同時進行 OCR 分析會消耗較多記憶體同時間。

**解決方法**：
1. 將輸入文件分批處理：將大量文件分成多個子目錄，逐個目錄執行
2. 關閉其他佔用記憶體嘅程式
3. 如果只需要文字分析（唔需要 OCR），使用 text 模式：
   ```bash
   python -m src.main analyze --input ./data --output ./output/report.xlsx --mode text
   ```
4. 對於超過 100 張圖片嘅情況，建議分批處理（每批 30-50 張）
5. 使用 `--verbose` 查看處理進度，確認程式仍在運行中

### 6. 配對結果不準確

**原因**：時間窗口設定可能唔適合你嘅對話模式。

**解決方法**：
1. 調整 `config.yaml` 中嘅 `time_window_hours`：
   - 如果客戶回覆較慢，增大時間窗口（例如 4 小時）
   - 如果同一時段有多個客戶，縮小時間窗口（例如 1 小時）
2. 調整 `confidence_threshold`：
   - 降低閾值（例如 0.5）會接受更多 OCR 結果，但可能有誤判
   - 提高閾值（例如 0.9）會更嚴格，但可能漏掉正確結果
3. 檢查輸出報表中標記為 `needs_review` 嘅記錄，人工確認配對是否正確
