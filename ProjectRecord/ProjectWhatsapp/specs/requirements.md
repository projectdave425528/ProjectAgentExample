# Requirements: WhatsApp 帳目分析系統

## 概述

為手機維修員設計嘅帳目分析工具，自動解析 WhatsApp 匯出嘅對話記錄同圖片（轉帳截圖），提取交易資訊，整合成結構化紀錄並匯出 Excel 報表。目標用戶係非技術人員，系統需要簡單易用、容錯能力強。

---

## User Stories

### US-001: 匯入 WhatsApp 對話
**As a** 手機維修員  
**I want to** 將 WhatsApp 匯出嘅 .txt 文件匯入系統  
**So that** 系統可以自動解析對話內容，唔使我逐條手動抄

### US-002: 自動識別交易相關訊息
**As a** 手機維修員  
**I want to** 系統自動識別邊啲訊息同收費/付款有關  
**So that** 我唔使逐條訊息睇，只需要確認結果

### US-003: 分析轉帳截圖
**As a** 手機維修員  
**I want to** 系統自動分析轉帳截圖入面嘅金額同付款方式  
**So that** 我唔使逐張圖片人手核對

### US-004: 配對對話同圖片
**As a** 手機維修員  
**I want to** 系統自動將對話入面提到嘅圖片同實際圖片配對  
**So that** 每筆交易都有完整嘅文字 + 圖片證據

### US-005: 匯出 Excel 報表
**As a** 手機維修員  
**I want to** 一鍵匯出所有客戶嘅交易紀錄做 Excel  
**So that** 我可以用 Excel 做帳、追數、報稅

### US-006: 處理多個客戶對話
**As a** 手機維修員  
**I want to** 一次過處理多個客戶嘅 WhatsApp 匯出  
**So that** 我可以批量整理所有客戶嘅帳目

### US-007: 選擇圖片分析方案
**As a** 手機維修員  
**I want to** 可以選擇用免費 OCR 定 AI Vision API 分析圖片  
**So that** 我可以根據預算同準確度需求做選擇

---

## System Behaviors (EARS Notation)

### SB-001: 時間戳解析
**When** 系統讀取 .txt 文件  
**the system shall** 用 regex 解析每行嘅時間戳，支援以下格式：
- `[YYYY/MM/DD, HH:MM:SS]`
- `[DD/MM/YYYY, HH:MM:SS]`
- `[YYYY-MM-DD, HH:MM:SS]`
- `[DD/MM/YYYY, h:mm:ss am/pm]`

### SB-002: 圖片引用偵測
**When** 訊息內容包含 `<attached: filename>`  
**the system shall** 記錄該圖片引用，並嘗試喺指定目錄搵到對應文件

### SB-003: 交易金額識別
**When** 訊息包含金額模式（如 `$XXX`、`HKD XXX`、`XXX蚊`、`XXX元`）  
**the system shall** 提取金額數值並標記為潛在交易金額

### SB-004: 付款方式識別
**When** 訊息包含付款關鍵字（PayMe、FPS、轉數快、銀行轉帳、現金、cash）  
**the system shall** 標記對應嘅付款方式

### SB-005: OCR 失敗回退
**If** Tesseract OCR 無法識別圖片內容  
**the system shall** 標記該圖片為「需人工確認」並繼續處理其他圖片

### SB-006: AI Vision API 失敗回退
**If** AI Vision API 調用失敗（網絡錯誤、API key 無效、額度用盡）  
**the system shall** 回退到 Tesseract OCR 並通知用戶

---

## Functional Requirements

### FR-001: WhatsApp .txt 文件解析
系統必須能夠讀取 WhatsApp 匯出嘅 .txt 文件，解析出：
- 時間戳（datetime）
- 發送者名稱
- 訊息內容
- 圖片附件引用

### FR-002: 多時間戳格式支援
系統必須支援至少 4 種常見嘅 WhatsApp 時間戳格式（見 SB-001），並能自動偵測使用中嘅格式。

### FR-003: 圖片 OCR 分析
系統必須能夠用 Tesseract OCR 分析轉帳截圖，提取：
- 交易金額
- 交易日期
- 付款方式/平台

### FR-004: AI Vision 圖片分析
系統必須支援用 AI Vision API（Claude/GPT）分析圖片，提取同 FR-003 相同嘅資訊，準確度更高。

### FR-005: 對話-圖片配對
系統必須能夠根據 `<attached: filename>` 標記，將對話訊息同對應圖片配對。

### FR-006: 交易紀錄整合
系統必須結合文字分析同圖片分析結果，產出結構化交易紀錄（JSON），包含：
- 日期
- 客戶名稱
- 維修項目
- 報價金額
- 實收金額
- 付款方式
- 付款狀態
- 備註

### FR-007: Excel 匯出
系統必須能夠將所有交易紀錄匯出為 .xlsx 文件，欄位同 FR-006 一致。

### FR-008: 批量處理
系統必須支援一次處理多個客戶嘅 WhatsApp 匯出文件夾。

### FR-009: 中間結果保存
系統必須將中間結果（解析後嘅 JSON）保存到文件，方便用戶檢查同修正。

---

## Non-Functional Requirements

### NFR-001: 易用性
系統以 CLI 工具形式提供，命令簡單直觀，附帶清晰嘅使用說明。目標用戶唔需要懂 Python。

### NFR-002: 性能
處理 50 個客戶對話（每個約 500 條訊息 + 10 張圖片）應在 5 分鐘內完成（使用 OCR 模式）。

### NFR-003: 準確度
- OCR 模式：金額識別準確率 ≥ 70%
- AI Vision 模式：金額識別準確率 ≥ 95%

### NFR-004: 容錯性
單個文件解析失敗唔應該影響其他文件嘅處理。系統應記錄所有錯誤並繼續。

### NFR-005: 可維護性
代碼模組化，每個模組獨立可測試。

### NFR-006: 數據安全
所有數據只喺本地處理同儲存（除咗 AI Vision API 調用）。唔會上傳到第三方伺服器。

---

## Edge Cases & Error Handling

| # | 場景 | 處理方式 |
|---|------|---------|
| EC-001 | .txt 文件編碼唔係 UTF-8 | 嘗試 UTF-8-BOM、GBK、Big5，失敗則報錯 |
| EC-002 | 時間戳格式完全無法識別 | 跳過該行，記錄 warning |
| EC-003 | 圖片文件唔存在（.txt 有引用但文件缺失） | 標記為「圖片缺失」，繼續處理 |
| EC-004 | 圖片唔係轉帳截圖（例如維修前後對比圖） | OCR/AI 回傳「非交易圖片」，跳過 |
| EC-005 | 同一對話有多筆交易 | 每筆交易獨立一條紀錄 |
| EC-006 | 金額有矛盾（文字寫 $500，圖片顯示 $450） | 兩個金額都記錄，標記「需確認」 |
| EC-007 | 多行訊息（訊息跨行） | 合併到上一條訊息 |
| EC-008 | 系統訊息（加入群組、更改號碼等） | 識別並跳過 |
| EC-009 | 空白 .txt 文件 | 跳過，記錄 warning |
| EC-010 | AI Vision API rate limit | 加入 retry with exponential backoff，最多 3 次 |

---

## Constraints

1. **語言**：Python 3.9+
2. **運行環境**：Windows（手機維修員常用）、macOS
3. **依賴最小化**：核心功能只依賴常見 Python 套件
4. **離線優先**：OCR 模式必須完全離線運行
5. **無需安裝數據庫**：所有數據用文件（JSON/Excel）儲存
6. **單機運行**：唔需要網絡（除 AI Vision API 模式）

---

## Out of Scope

1. WhatsApp 自動匯出（用戶需要手動匯出對話）
2. 即時通訊整合（唔會連接 WhatsApp API）
3. 多語言支援（只支援中文/廣東話/英文混合）
4. Web UI 或 GUI（第一版只做 CLI）
5. 自動記帳到會計軟件
6. 客戶管理功能（CRM）
7. 自動發送收款提醒
8. 歷史數據遷移
