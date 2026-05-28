# Requirements: WhatsApp 帳目分析系統

## 概述
Python 桌面工具，專為手機維修員設計，讀取 WhatsApp 匯出嘅對話紀錄（.txt）同圖片，自動分析內容並整合成結構化客戶交易紀錄，最後匯出 Excel 報表。

## User Stories

### US-001: 匯入 WhatsApp 對話紀錄
- **As a** 手機維修員
- **I want** 將 WhatsApp 匯出嘅 .txt 文件匯入系統
- **So that** 系統可以自動解析對話內容，提取交易相關資訊

#### Acceptance Criteria
- [ ] 支援拖放或選擇 .txt 文件匯入
- [ ] 正確解析 `[YYYY/MM/DD, HH:MM:SS] Sender: Message` 格式
- [ ] 處理多行訊息（訊息跨多行時正確歸屬同一條訊息）
- [ ] 識別並跳過系統訊息（加入群組、更改群組名稱等）
- [ ] 識別 `<attached:filename>` 媒體引用並記錄
- [ ] 支援 12 小時制（AM/PM）同 24 小時制時間格式
- [ ] 支援唔同日期順序（DD/MM/YYYY、MM/DD/YYYY、YYYY/MM/DD）

### US-002: 分析轉帳截圖
- **As a** 手機維修員
- **I want** 系統自動分析 WhatsApp 匯出嘅轉帳截圖
- **So that** 我唔使手動記錄每筆轉帳金額

#### Acceptance Criteria
- [ ] 支援 JPG、PNG、WEBP 圖片格式
- [ ] 識別 PayMe 轉帳截圖並提取金額
- [ ] 識別 FPS 轉帳截圖並提取金額
- [ ] 識別銀行轉帳截圖並提取金額同交易編號
- [ ] 將圖片透過 `<attached:...>` 時間戳同對話 context 配對
- [ ] 提供免費本地 OCR 模式（Tesseract）
- [ ] 提供付費雲端 AI Vision 模式（更準確）
- [ ] 用戶可以選擇使用邊種模式

### US-003: 自動整合交易紀錄
- **As a** 手機維修員
- **I want** 系統自動將對話分析同圖片分析結果整合成交易紀錄
- **So that** 我可以清楚睇到每個客戶嘅交易狀態

#### Acceptance Criteria
- [ ] 自動提取客戶名稱（從 WhatsApp 發送者名稱）
- [ ] 自動提取維修項目（從對話內容）
- [ ] 自動提取報價金額（從對話內容）
- [ ] 自動提取實收金額（從轉帳截圖或對話確認）
- [ ] 自動識別付款方式（PayMe/FPS/銀行轉帳/現金）
- [ ] 自動標記付款狀態（已收/未收/部分）
- [ ] 處理一個客戶多次交易嘅情況
- [ ] 產出結構化 JSON 交易紀錄

### US-004: 匯出 Excel 報表
- **As a** 手機維修員
- **I want** 將所有交易紀錄匯出為 Excel 文件
- **So that** 我可以用熟悉嘅工具查閱同管理帳目

#### Acceptance Criteria
- [ ] 匯出 .xlsx 格式文件
- [ ] 包含欄位：日期、客戶名稱、維修項目、報價金額、實收金額、付款方式、付款狀態、備註
- [ ] 支援按日期排序
- [ ] 支援按客戶名稱排序
- [ ] 自動計算總額（報價總額、實收總額）
- [ ] 用戶可以選擇匯出路徑

### US-005: 簡單易用嘅操作流程
- **As a** 非技術人員
- **I want** 用最少步驟完成整個分析流程
- **So that** 我唔使學複雜嘅操作

#### Acceptance Criteria
- [ ] 提供 CLI 介面，步驟清晰
- [ ] 錯誤訊息用中文顯示
- [ ] 處理過程有進度提示
- [ ] 唔需要手動配置複雜設定

---

## System Behaviors (EARS Notation)

### 文字解析

WHEN 系統收到 WhatsApp .txt 匯出文件
THE SYSTEM SHALL 逐行讀取並用 regex 解析每條訊息嘅時間戳、發送者、內容

WHEN 一行文字唔符合訊息開頭格式（無時間戳）
THE SYSTEM SHALL 將該行附加到前一條訊息嘅內容（多行訊息處理）

WHEN 訊息內容包含 `<attached:filename>`
THE SYSTEM SHALL 記錄媒體引用並嘗試配對對應嘅圖片文件

WHEN 系統訊息被偵測到（如「加入了群組」「更改了群組名稱」）
THE SYSTEM SHALL 標記為系統訊息並排除於交易分析之外

### 圖片分析

WHEN 系統收到圖片文件且用戶選擇 OCR 模式
THE SYSTEM SHALL 使用 Tesseract OCR 提取文字並解析金額資訊

WHEN 系統收到圖片文件且用戶選擇 AI Vision 模式
THE SYSTEM SHALL 調用 AI Vision API 分析圖片並提取交易資訊

WHEN 圖片無法識別為轉帳截圖
THE SYSTEM SHALL 標記為「無法識別」並記錄到日誌，唔影響其他處理

WHEN OCR/AI Vision 提取嘅金額信心度低於閾值（0.7）
THE SYSTEM SHALL 標記為「需人工確認」

### 交易整合

WHEN 文字分析同圖片分析完成
THE SYSTEM SHALL 根據時間戳同 attachment filename 配對，整合成交易紀錄

WHEN 同一客戶有多筆交易
THE SYSTEM SHALL 為每筆交易建立獨立紀錄，並以客戶名稱關聯

WHEN 偵測到報價但未偵測到對應付款
THE SYSTEM SHALL 將該交易標記為「未收」

### Excel 匯出

WHEN 用戶觸發匯出
THE SYSTEM SHALL 將所有交易紀錄寫入 .xlsx 文件，包含所有必要欄位同自動計算

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | 解析 WhatsApp .txt 匯出格式 | Must | 支援標準匯出格式 |
| FR-002 | 支援多種時間格式（12/24小時制） | Must | |
| FR-003 | 處理多行訊息 | Must | 無時間戳行歸屬前一條 |
| FR-004 | 識別系統訊息並排除 | Should | |
| FR-005 | 識別 `<attached:...>` 媒體引用 | Must | |
| FR-006 | 支援唔同日期順序格式 | Should | DD/MM、MM/DD、YYYY/MM/DD |
| FR-007 | 支援 JPG/PNG/WEBP 圖片格式 | Must | |
| FR-008 | Tesseract OCR 本地分析模式 | Must | 免費離線 |
| FR-009 | AI Vision API 雲端分析模式 | Could | 付費更準確 |
| FR-010 | 提取轉帳金額 | Must | 支援 $、HK$、千位分隔符 |
| FR-011 | 提取交易日期 | Should | |
| FR-012 | 提取交易編號 | Could | |
| FR-013 | 圖片同對話 context 配對 | Must | 透過 attachment filename |
| FR-014 | 識別付款方式（PayMe/FPS/銀行轉帳） | Must | |
| FR-015 | 結合文字 + 圖片分析結果 | Must | |
| FR-016 | 自動提取客戶名稱 | Must | 從 sender 欄位 |
| FR-017 | 自動提取維修項目 | Should | 關鍵字匹配 |
| FR-018 | 自動提取報價金額 | Must | 從對話 regex |
| FR-019 | 自動提取實收金額 | Must | 從截圖或對話 |
| FR-020 | 識別付款方式 | Must | |
| FR-021 | 標記付款狀態 | Must | paid/unpaid/partial |
| FR-022 | 處理一客戶多交易 | Should | 時間窗口分組 |
| FR-023 | 產出結構化 JSON | Must | 中間結果 |
| FR-024 | 匯出 .xlsx 格式 | Must | |
| FR-025 | Excel 包含所有必要欄位 | Must | |
| FR-026 | 按日期排序 | Should | |
| FR-027 | 按客戶排序 | Should | |
| FR-028 | 自動計算總額 | Should | 報價 + 實收 |

---

## Non-Functional Requirements

| ID | Type | Requirement | Criteria |
|----|------|-------------|----------|
| NFR-001 | Performance | 處理 1000 條訊息嘅 .txt 文件 | < 5 秒 |
| NFR-002 | Performance | 單張圖片 OCR 分析 | < 10 秒 |
| NFR-003 | Usability | 錯誤訊息必須用中文顯示 | 100% 中文 |
| NFR-004 | Usability | CLI 操作步驟 | ≤ 5 步 |
| NFR-005 | Reliability | 單張圖片分析失敗唔影響整體流程 | 容錯隔離 |
| NFR-006 | Reliability | 文字解析錯誤率（標準格式） | < 1% |
| NFR-007 | Compatibility | 支援 Windows 10+ 運行 | Win10+ |
| NFR-008 | Compatibility | 支援 Python 3.9+ | Py3.9+ |
| NFR-009 | Security | AI Vision API Key 唔可以 hardcode | 環境變數/.env |
| NFR-010 | Maintainability | 模組間低耦合，可獨立測試 | 模組化 + interface |
| NFR-011 | i18n | 支援廣東話/中文/英文混合內容分析 | 多語言 |

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
|----------|-------------------|
| .txt 文件為空 | 顯示錯誤訊息「文件為空，請確認匯出正確」，終止 |
| .txt 文件唔存在 | 顯示錯誤訊息「文件唔存在」，終止 |
| 圖片文件損壞或無法讀取 | 跳過該圖片，記錄警告，繼續處理其他 |
| 對話中無任何交易相關內容 | 顯示「未偵測到交易紀錄」 |
| 同一時間戳有多張圖片 | 逐一分析，分別配對 |
| 金額格式異常（$1,000.5、HK$500） | 支援常見金額格式，含千位分隔符同貨幣符號 |
| 客戶名稱含 emoji 或特殊字符 | 保留原始名稱，Excel 匯出時正確顯示 |
| 超大文件（>10MB .txt） | 分段讀取，避免記憶體溢出 |
| 圖片唔係轉帳截圖（如維修照片） | 標記為「非轉帳圖片」，跳過 |
| 對話語言混合（廣東話+英文+普通話） | 支援多語言混合分析 |
| WhatsApp 匯出格式版本差異 | 支援已知格式變體，未知格式記錄警告 |
| 報價同實收金額唔一致 | 兩者都記錄，備註標記差異 |
| 群組對話（多人） | 正確區分每個發送者，分別建立交易紀錄 |
| AI Vision API 失敗 | 回退到 OCR 模式（如可用），否則標記 error |
| Tesseract 未安裝 | 顯示清晰安裝指引，終止 |

---

## Constraints
- 程式語言必須用 Python（用戶指定）
- 必須支援離線運行（OCR 模式）
- 目標用戶為非技術人員，介面必須簡單直觀
- 對話語言為廣東話/中文混合英文
- 付款方式限定：PayMe、FPS、銀行轉帳、現金（香港常用）
- 圖片命名格式：IMG-YYYYMMDD-WANNNN.jpg（WhatsApp 標準匯出命名）
- 免費方案必須可用（Tesseract OCR）
- 只處理 HKD 幣種

---

## Out of Scope
- GUI 圖形介面（第一版用 CLI）
- 即時 WhatsApp 連接（只處理匯出文件）
- 自動發送收款提醒
- 多幣種支援
- 雲端儲存/同步
- 客戶管理 CRM 功能
- 發票生成
- 語音訊息分析
- 影片分析
