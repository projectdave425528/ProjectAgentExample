# Requirements: WhatsApp 帳目分析系統

## 概述

WhatsApp 帳目分析系統係一個 Python 桌面工具，專為手機維修員設計。系統讀取 WhatsApp 匯出嘅對話紀錄（.txt）同圖片，自動分析內容，整合成結構化嘅客戶交易紀錄，最後匯出 Excel 報表。

**目標用戶**：手機維修員（非技術人員）
**核心問題**：帳目混亂，難以追蹤客戶交易、收款狀態
**解決方案**：自動化分析 WhatsApp 對話 + 轉帳截圖 → 結構化交易紀錄 → Excel 報表

---

## User Stories

### US-1: 匯入 WhatsApp 對話紀錄
**As a** 手機維修員
**I want to** 將 WhatsApp 匯出嘅 .txt 文件匯入系統
**So that** 系統可以自動解析對話內容，提取交易相關資訊

**Acceptance Criteria:**
- [ ] 支援拖放或選擇 .txt 文件匯入
- [ ] 正確解析 `[YYYY/MM/DD, HH:MM:SS] Sender: Message` 格式
- [ ] 處理多行訊息（訊息跨多行時正確歸屬同一條訊息）
- [ ] 識別並跳過系統訊息（加入群組、更改群組名稱等）
- [ ] 識別 `<attached:filename>` 媒體引用並記錄
- [ ] 支援 12 小時制（AM/PM）同 24 小時制時間格式
- [ ] 支援唔同日期順序（DD/MM/YYYY、MM/DD/YYYY、YYYY/MM/DD）

### US-2: 分析轉帳截圖
**As a** 手機維修員
**I want to** 系統自動分析 WhatsApp 匯出嘅轉帳截圖
**So that** 我唔使手動記錄每筆轉帳金額

**Acceptance Criteria:**
- [ ] 支援 JPG、PNG、WEBP 圖片格式
- [ ] 識別 PayMe 轉帳截圖並提取金額
- [ ] 識別 FPS 轉帳截圖並提取金額
- [ ] 識別銀行轉帳截圖並提取金額同交易編號
- [ ] 將圖片透過 `<attached:...>` 時間戳同對話 context 配對
- [ ] 提供免費本地 OCR 模式（Tesseract）
- [ ] 提供付費雲端 AI Vision 模式（更準確）
- [ ] 用戶可以選擇使用邊種模式

### US-3: 自動整合交易紀錄
**As a** 手機維修員
**I want to** 系統自動將對話分析同圖片分析結果整合成交易紀錄
**So that** 我可以清楚睇到每個客戶嘅交易狀態

**Acceptance Criteria:**
- [ ] 自動提取客戶名稱（從 WhatsApp 發送者名稱）
- [ ] 自動提取維修項目（從對話內容）
- [ ] 自動提取報價金額（從對話內容）
- [ ] 自動提取實收金額（從轉帳截圖或對話確認）
- [ ] 自動識別付款方式（PayMe/FPS/銀行轉帳/現金）
- [ ] 自動標記付款狀態（已收/未收）
- [ ] 處理一個客戶多次交易嘅情況
- [ ] 產出結構化 JSON 交易紀錄

### US-4: 匯出 Excel 報表
**As a** 手機維修員
**I want to** 將所有交易紀錄匯出為 Excel 文件
**So that** 我可以用熟悉嘅工具查閱同管理帳目

**Acceptance Criteria:**
- [ ] 匯出 .xlsx 格式文件
- [ ] 包含欄位：日期、客戶名稱、維修項目、報價金額、實收金額、付款方式、付款狀態、備註
- [ ] 支援按日期排序
- [ ] 支援按客戶名稱排序
- [ ] 自動計算總額（報價總額、實收總額）
- [ ] 用戶可以選擇匯出路徑

### US-5: 簡單易用嘅操作流程
**As a** 非技術人員
**I want to** 用最少步驟完成整個分析流程
**So that** 我唔使學複雜嘅操作

**Acceptance Criteria:**
- [ ] 提供 CLI 介面，步驟清晰
- [ ] 錯誤訊息用中文顯示
- [ ] 處理過程有進度提示
- [ ] 唔需要手動配置複雜設定

---

## System Behaviors (EARS Notation)

### SB-1: 文字解析行為
**When** 系統收到 WhatsApp .txt 匯出文件
**the system shall** 逐行讀取並用 regex 解析每條訊息嘅時間戳、發送者、內容。

**When** 一行文字唔符合訊息開頭格式（無時間戳）
**the system shall** 將該行附加到前一條訊息嘅內容（多行訊息處理）。

**When** 訊息內容包含 `<attached:filename>`
**the system shall** 記錄媒體引用並嘗試配對對應嘅圖片文件。

**When** 系統訊息被偵測到（如「加入了群組」「更改了群組名稱」）
**the system shall** 標記為系統訊息並排除於交易分析之外。

### SB-2: 圖片分析行為
**When** 系統收到圖片文件且用戶選擇 OCR 模式
**the system shall** 使用 Tesseract OCR 提取文字並解析金額資訊。

**When** 系統收到圖片文件且用戶選擇 AI Vision 模式
**the system shall** 調用 AI Vision API 分析圖片並提取交易資訊。

**When** 圖片無法識別為轉帳截圖
**the system shall** 標記為「無法識別」並記錄到日誌，唔影響其他處理。

**When** OCR/AI Vision 提取嘅金額信心度低於閾值
**the system shall** 標記為「需人工確認」。

### SB-3: 交易整合行為
**When** 文字分析同圖片分析完成
**the system shall** 根據時間戳同 context 配對，整合成交易紀錄。

**When** 同一客戶有多筆交易
**the system shall** 為每筆交易建立獨立紀錄，並以客戶名稱關聯。

**When** 偵測到報價但未偵測到對應付款
**the system shall** 將該交易標記為「未收」。

### SB-4: Excel 匯出行為
**When** 用戶觸發匯出
**the system shall** 將所有交易紀錄寫入 .xlsx 文件，包含所有必要欄位同自動計算。

---

## Functional Requirements

| ID | 模組 | 需求描述 | 優先級 |
|----|------|----------|--------|
| FR-01 | Text Parser | 解析 WhatsApp .txt 匯出格式 | P0 |
| FR-02 | Text Parser | 支援多種時間格式（12/24小時制） | P0 |
| FR-03 | Text Parser | 處理多行訊息 | P0 |
| FR-04 | Text Parser | 識別系統訊息並排除 | P1 |
| FR-05 | Text Parser | 識別 `<attached:...>` 媒體引用 | P0 |
| FR-06 | Text Parser | 支援唔同日期順序格式 | P1 |
| FR-07 | Image Analyzer | 支援 JPG/PNG/WEBP 格式 | P0 |
| FR-08 | Image Analyzer | Tesseract OCR 本地分析模式 | P0 |
| FR-09 | Image Analyzer | AI Vision API 雲端分析模式 | P1 |
| FR-10 | Image Analyzer | 提取轉帳金額 | P0 |
| FR-11 | Image Analyzer | 提取交易日期 | P1 |
| FR-12 | Image Analyzer | 提取交易編號 | P2 |
| FR-13 | Image Analyzer | 圖片同對話 context 配對 | P0 |
| FR-14 | Image Analyzer | 識別付款方式（PayMe/FPS/銀行轉帳） | P0 |
| FR-15 | Record Builder | 結合文字 + 圖片分析結果 | P0 |
| FR-16 | Record Builder | 自動提取客戶名稱 | P0 |
| FR-17 | Record Builder | 自動提取維修項目 | P1 |
| FR-18 | Record Builder | 自動提取報價金額 | P0 |
| FR-19 | Record Builder | 自動提取實收金額 | P0 |
| FR-20 | Record Builder | 識別付款方式 | P0 |
| FR-21 | Record Builder | 標記付款狀態 | P0 |
| FR-22 | Record Builder | 處理一客戶多交易 | P1 |
| FR-23 | Record Builder | 產出結構化 JSON | P0 |
| FR-24 | Excel Exporter | 匯出 .xlsx 格式 | P0 |
| FR-25 | Excel Exporter | 包含所有必要欄位 | P0 |
| FR-26 | Excel Exporter | 按日期排序 | P1 |
| FR-27 | Excel Exporter | 按客戶排序 | P1 |
| FR-28 | Excel Exporter | 自動計算總額 | P1 |

---

## Non-Functional Requirements

| ID | 類別 | 需求描述 | 指標 |
|----|------|----------|------|
| NFR-01 | 效能 | 處理 1000 條訊息嘅 .txt 文件應在 5 秒內完成 | < 5s |
| NFR-02 | 效能 | 單張圖片 OCR 分析應在 10 秒內完成 | < 10s |
| NFR-03 | 可用性 | 錯誤訊息必須用中文顯示 | 100% 中文 |
| NFR-04 | 可用性 | CLI 操作步驟不超過 5 步 | ≤ 5 步 |
| NFR-05 | 可靠性 | 單張圖片分析失敗唔影響整體流程 | 容錯隔離 |
| NFR-06 | 可靠性 | 文字解析錯誤率 < 1%（標準格式） | < 1% |
| NFR-07 | 相容性 | 支援 Windows 10+ 運行 | Win10+ |
| NFR-08 | 相容性 | 支援 Python 3.9+ | Py3.9+ |
| NFR-09 | 安全性 | AI Vision API Key 唔可以 hardcode | 環境變數/配置文件 |
| NFR-10 | 可維護性 | 模組間低耦合，可獨立測試 | 模組化設計 |
| NFR-11 | 國際化 | 支援廣東話/中文/英文混合內容分析 | 多語言 |

---

## Edge Cases

| # | 場景 | 預期處理 |
|---|------|----------|
| 1 | .txt 文件為空 | 顯示錯誤訊息「文件為空，請確認匯出正確」 |
| 2 | 圖片文件損壞或無法讀取 | 跳過該圖片，記錄警告，繼續處理其他 |
| 3 | 對話中無任何交易相關內容 | 顯示「未偵測到交易紀錄」 |
| 4 | 同一時間戳有多張圖片 | 逐一分析，分別配對 |
| 5 | 金額格式異常（如 $1,000.5、HK$500） | 支援常見金額格式，含千位分隔符同貨幣符號 |
| 6 | 客戶名稱含 emoji 或特殊字符 | 保留原始名稱，Excel 匯出時正確顯示 |
| 7 | 超大文件（>10MB .txt） | 分段讀取，避免記憶體溢出 |
| 8 | 圖片唔係轉帳截圖（如維修照片） | OCR/AI 識別後標記為「非轉帳圖片」，跳過 |
| 9 | 對話語言混合（廣東話+英文+普通話） | 支援多語言混合分析 |
| 10 | WhatsApp 匯出格式版本差異 | 支援已知嘅格式變體，未知格式記錄警告 |
| 11 | 報價同實收金額唔一致 | 兩者都記錄，備註標記差異 |
| 12 | 群組對話（多人） | 正確區分每個發送者，分別建立交易紀錄 |

---

## Constraints

| # | 約束 | 原因 |
|---|------|------|
| 1 | 程式語言必須用 Python | 用戶指定 |
| 2 | 必須支援離線運行（OCR 模式） | 用戶可能無穩定網絡 |
| 3 | 目標用戶為非技術人員 | 介面必須簡單直觀 |
| 4 | 對話語言為廣東話/中文混合英文 | NLP 分析需支援多語言 |
| 5 | 付款方式限定：PayMe、FPS、銀行轉帳、現金 | 香港常用付款方式 |
| 6 | 圖片命名格式：IMG-YYYYMMDD-WANNNN.jpg | WhatsApp 標準匯出命名 |
| 7 | 免費方案必須可用（Tesseract OCR） | 用戶可能唔想付費 |

---

## Out of Scope

| # | 項目 | 原因 |
|---|------|------|
| 1 | GUI 圖形介面 | 第一版用 CLI，後續可擴展 |
| 2 | 即時 WhatsApp 連接 | 只處理匯出文件，唔做即時通訊 |
| 3 | 自動發送收款提醒 | 超出帳目分析範圍 |
| 4 | 多幣種支援 | 只處理 HKD |
| 5 | 雲端儲存/同步 | 本地工具，唔涉及雲端 |
| 6 | 客戶管理 CRM 功能 | 只做帳目分析，唔做客戶關係管理 |
| 7 | 發票生成 | 超出範圍 |
| 8 | 語音訊息分析 | 只處理文字同圖片 |
| 9 | 影片分析 | 只處理靜態圖片 |
