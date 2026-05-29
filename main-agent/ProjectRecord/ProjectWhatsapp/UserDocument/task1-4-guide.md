# Task 1-4 使用指南

> 本文件解釋 Task 1-4 各自嘅用途、點跑 Unit Test、同預期結果。

---

## 項目結構總覽

```
output/
├── assignment-002/    ← Task 1: Data Models + Config
├── assignment-004/    ← Task 2: Regex Patterns
├── assignment-006/    ← Task 3: Text Parser 主邏輯
└── assignment-010/    ← Task 4: Image Analyzer (OCR)
```

---

## Task 1: 項目初始化 + Data Models

### 用途
定義整個系統嘅核心數據結構（Pydantic v2 models）同配置載入機制。所有後續 Task 都依賴呢啲 models。

### 包含咩
| 文件 | 用途 |
|------|------|
| `src/models/message.py` | `ParsedMessage` — WhatsApp 訊息結構 |
| `src/models/image_result.py` | `ImageAnalysisResult` — 圖片分析結果 |
| `src/models/transaction.py` | `TransactionRecord` — 交易紀錄 |
| `src/models/config.py` | `AppConfig` — 應用配置 |
| `src/config.py` | Config loader（.env + config.yaml） |
| `requirements.txt` | 所有依賴（pinned versions） |
| `.env.example` | 環境變數範例 |
| `config.yaml` | 預設配置 |

### 點跑 Unit Test

```bash
# 進入 Task 1 output 目錄
cd ProjectRecord/ProjectWhatsapp/output/assignment-002

# 安裝依賴
pip install -r requirements.txt

# 跑 tests
pytest tests/ -v
```

### 預期結果

```
tests/test_models.py::TestParsedMessageHappyPath::test_create_with_all_fields PASSED
tests/test_models.py::TestParsedMessageHappyPath::test_serialize_to_json PASSED
tests/test_models.py::TestParsedMessageHappyPath::test_defaults_applied PASSED
tests/test_models.py::TestParsedMessageErrorPath::test_missing_timestamp_raises_error PASSED
tests/test_models.py::TestParsedMessageErrorPath::test_empty_sender_raises_error PASSED
tests/test_models.py::TestParsedMessageEdgeCases::test_sender_with_emoji PASSED
tests/test_models.py::TestImageAnalysisResultErrorPath::test_confidence_above_1_raises_error PASSED
tests/test_models.py::TestTransactionRecordHappyPath::test_uuid_auto_generated PASSED
tests/test_models.py::TestTransactionRecordHappyPath::test_uuid_unique PASSED
tests/test_models.py::TestAppConfigHappyPath::test_defaults PASSED
tests/test_config.py::TestLoadConfigHappyPath::test_load_from_valid_yaml PASSED
tests/test_config.py::TestLoadConfigHappyPath::test_env_overrides_yaml PASSED
...

54 passed in 0.93s
```

### 核心概念

**ParsedMessage** — 一條 WhatsApp 訊息：
```python
from src.models.message import ParsedMessage
from datetime import datetime

msg = ParsedMessage(
    timestamp=datetime(2024, 1, 15, 14, 30, 0),
    sender="陳大文",
    content="換屏幾錢？",
    is_system_message=False,
    attachments=[],
    raw_text="[2024/01/15, 14:30:00] 陳大文: 換屏幾錢？"
)
```

**ImageAnalysisResult** — 一張圖片嘅分析結果：
```python
from src.models.image_result import ImageAnalysisResult
from decimal import Decimal

result = ImageAnalysisResult(
    filename="payment_receipt.jpg",
    analysis_mode="ocr",
    payment_method="payme",
    amount=Decimal("500.00"),
    confidence=0.95,
    raw_text="HK$500.00 PayMe 轉帳成功"
)
```

**AppConfig** — 配置載入（優先順序：env vars > yaml > defaults）：
```python
from src.config import load_config

config = load_config("config.yaml")
# config.analysis_mode == "ocr"
# config.confidence_threshold == 0.7
```

---

## Task 2: WhatsApp Text Parser — Regex Patterns

### 用途
定義所有用嚟解析 WhatsApp 匯出文件嘅 regex patterns 同 utility functions。支援多種時間格式、日期順序、分隔符。

### 包含咩
| 文件 | 用途 |
|------|------|
| `src/parser/patterns.py` | MESSAGE_PATTERN、ATTACHMENT_PATTERN、系統訊息偵測 |
| `src/parser/utils.py` | `parse_timestamp()`、`normalize_date_string()`、時間格式轉換 |

### 點跑 Unit Test

```bash
cd ProjectRecord/ProjectWhatsapp/output/assignment-004
pytest tests/ -v
```

### 預期結果

```
tests/test_parser/test_patterns.py::TestMessagePattern::test_standard_24h_format PASSED
tests/test_parser/test_patterns.py::TestMessagePattern::test_12h_format_pm PASSED
tests/test_parser/test_patterns.py::TestMessagePattern::test_dd_mm_yyyy_format PASSED
tests/test_parser/test_patterns.py::TestMessagePattern::test_dash_separator PASSED
tests/test_parser/test_patterns.py::TestSplitSenderContent::test_sender_with_colon PASSED
tests/test_parser/test_patterns.py::TestAttachmentPattern::test_standard_attachment PASSED
tests/test_parser/test_patterns.py::TestIsSystemMessage::test_joined_group_chinese PASSED
tests/test_parser/test_patterns.py::TestParseTimestamp::test_standard_24h PASSED
tests/test_parser/test_patterns.py::TestParseTimestamp::test_12h_pm PASSED
tests/test_parser/test_patterns.py::TestParseTimestamp::test_invalid_date_feb_31 PASSED
...

105 passed in 1.55s
```

### 核心概念

**解析一行 WhatsApp 訊息：**
```python
from src.parser.patterns import match_message_line

# 正常訊息
result = match_message_line("[2024/01/15, 14:30:00] 陳大文: 你好")
# result = ("2024/01/15, 14:30:00", "陳大文", "你好")

# 非訊息行（多行訊息嘅延續）
result = match_message_line("如果係 Pro Max 就 $680")
# result = None
```

**解析時間戳（支援多種格式）：**
```python
from src.parser.utils import parse_timestamp

# 24 小時制
parse_timestamp("2024/01/15, 14:30:00")
# → datetime(2024, 1, 15, 14, 30, 0)

# 12 小時制
parse_timestamp("1/15/24, 2:30 PM")
# → datetime(2024, 1, 15, 14, 30, 0)

# 唔同分隔符
parse_timestamp("2024-01-15, 14:30:00")
# → datetime(2024, 1, 15, 14, 30, 0)

# 無效日期
parse_timestamp("2024/02/31, 14:30:00")
# → None
```

**偵測系統訊息：**
```python
from src.parser.patterns import is_system_message

is_system_message("陳大文 加入了群組")  # True
is_system_message("你好嗎？")           # False
```

**提取附件：**
```python
from src.parser.patterns import extract_attachment

extract_attachment("<attached: payment_receipt.jpg>")
# → "payment_receipt.jpg"

extract_attachment("普通訊息")
# → None
```

---

## Task 3: WhatsApp Text Parser — 主解析邏輯

### 用途
將完整嘅 WhatsApp .txt 匯出文件解析成 `ParsedMessage` 列表。處理多行訊息、系統訊息、附件。

### 包含咩
| 文件 | 用途 |
|------|------|
| `src/parser/text_parser.py` | `parse_chat_file()` — 主解析函數 |
| `tests/fixtures/sample_chat.txt` | 測試用嘅 WhatsApp 對話範例 |

### 點跑 Unit Test

```bash
cd ProjectRecord/ProjectWhatsapp/output/assignment-006
pytest tests/ -v
```

**注意：** Task 3 依賴 Task 1 同 Task 2 嘅代碼。如果要獨立跑，需要確保 `src/models/` 同 `src/parser/patterns.py` + `utils.py` 都存在。Generator 已喺 `_test_env/` 目錄準備咗完整環境。

### 預期結果

```
tests/test_parser/test_text_parser.py::TestHappyPath::test_parse_sample_chat_message_count PASSED
tests/test_parser/test_text_parser.py::TestHappyPath::test_parse_sample_chat_first_message_is_system PASSED
tests/test_parser/test_text_parser.py::TestHappyPath::test_parse_sample_chat_multiline_message PASSED
tests/test_parser/test_text_parser.py::TestHappyPath::test_parse_sample_chat_attachment PASSED
tests/test_parser/test_text_parser.py::TestErrorPath::test_file_not_found_raises PASSED
tests/test_parser/test_text_parser.py::TestErrorPath::test_latin1_encoding_fallback PASSED
tests/test_parser/test_text_parser.py::TestEdgeCases::test_empty_file_returns_empty_list PASSED
tests/test_parser/test_text_parser.py::TestEdgeCases::test_long_message_content PASSED
tests/test_parser/test_text_parser.py::TestEdgeCases::test_consecutive_continuation_lines PASSED
...

28 passed
```

### 核心概念

**解析完整對話文件：**
```python
from src.parser.text_parser import parse_chat_file

messages = parse_chat_file("path/to/chat.txt")
# 返回 list[ParsedMessage]

# 每個 message 包含：
# - timestamp: datetime
# - sender: str
# - content: str（多行訊息會合併）
# - is_system_message: bool
# - attachments: list[str]
# - raw_text: str
```

**用 sample_chat.txt 嘅預期結果：**

```python
messages = parse_chat_file("tests/fixtures/sample_chat.txt")

len(messages)  # 12

# 第 1 條：系統訊息（加密通知）
messages[0].is_system_message  # True
messages[0].sender  # "Messages and calls are end-to-end encrypted..."

# 第 2 條：普通訊息
messages[1].sender  # "陳大文"
messages[1].content  # "早晨，想問下換屏幾錢？"

# 第 3 條：多行訊息（3 行合併）
messages[2].sender  # "維修師傅"
"iPhone 15 換屏 $500" in messages[2].content  # True
"Pro Max" in messages[2].content  # True
"保護貼" in messages[2].content  # True

# 第 9 條：含附件
messages[8].attachments  # ["payment_receipt.jpg"]

# 第 12 條：系統訊息（改描述）
messages[11].is_system_message  # True
```

**錯誤處理：**
```python
# 文件唔存在 → FileNotFoundError
parse_chat_file("/nonexistent/file.txt")
# raises FileNotFoundError: "Chat file not found: /nonexistent/file.txt"

# 空文件 → 返回空列表 + warning log
parse_chat_file("empty.txt")
# → []（同時 log warning "Empty chat file"）
```

---

## Task 4: Image Analyzer — Base + OCR 模式

### 用途
分析轉帳截圖，提取金額同付款方式。用 Tesseract OCR 讀取圖片文字，再用 regex 提取金額同 keyword matching 識別付款方式。

### 包含咩
| 文件 | 用途 |
|------|------|
| `src/analyzer/base.py` | `ImageAnalyzerBase` — Abstract base class（interface） |
| `src/analyzer/ocr_analyzer.py` | `OcrAnalyzer` — Tesseract OCR 實現 |
| `src/analyzer/amount_extractor.py` | `extract_amounts()` — 金額提取 |
| `src/analyzer/payment_detector.py` | `detect_payment_method()` — 付款方式識別 |

### 點跑 Unit Test

```bash
cd ProjectRecord/ProjectWhatsapp/output/assignment-010
pytest tests/ -v
```

**注意：** 所有 tests 都 mock 咗 Tesseract 同 Pillow，唔需要真正安裝 Tesseract 就可以跑 tests。

### 預期結果

```
tests/test_analyzer/test_amount_extractor.py::TestExtractAmounts::test_simple_dollar_amount PASSED
tests/test_analyzer/test_amount_extractor.py::TestExtractAmounts::test_hk_dollar_with_thousands PASSED
tests/test_analyzer/test_amount_extractor.py::TestExtractAmounts::test_chinese_suffix_mun PASSED
tests/test_analyzer/test_amount_extractor.py::TestExtractAmounts::test_multiple_amounts PASSED
tests/test_analyzer/test_amount_extractor.py::TestExtractAmounts::test_no_duplicate_amounts PASSED
tests/test_analyzer/test_payment_detector.py::TestDetectPaymentMethod::test_payme_detected PASSED
tests/test_analyzer/test_payment_detector.py::TestDetectPaymentMethod::test_fps_detected PASSED
tests/test_analyzer/test_payment_detector.py::TestDetectPaymentMethod::test_bank_transfer_detected PASSED
tests/test_analyzer/test_ocr_analyzer.py::TestOcrAnalyzerHappyPath::test_extract_payme_amount PASSED
tests/test_analyzer/test_ocr_analyzer.py::TestOcrAnalyzerErrorPath::test_file_not_found PASSED
tests/test_analyzer/test_ocr_analyzer.py::TestOcrAnalyzerEdgeCases::test_empty_ocr_text PASSED
...

All tests passed
```

### 核心概念

**提取金額（支援多種格式）：**
```python
from src.analyzer.amount_extractor import extract_amounts
from decimal import Decimal

extract_amounts("HK$500.00 PayMe")
# → [Decimal("500.00")]

extract_amounts("$1,000.50")
# → [Decimal("1000.50")]

extract_amounts("收咗500蚊")
# → [Decimal("500")]

extract_amounts("報價 $500 實收 HK$450.00")
# → [Decimal("500"), Decimal("450.00")]  ← 支援多金額

extract_amounts("$500 同 500蚊")
# → [Decimal("500")]  ← 自動去重

extract_amounts("")
# → []
```

**識別付款方式：**
```python
from src.analyzer.payment_detector import detect_payment_method

detect_payment_method("PayMe 轉帳成功")
# → "payme"

detect_payment_method("轉數快 FPS 已收")
# → "fps"

detect_payment_method("銀行轉帳 已完成")
# → "bank_transfer"

detect_payment_method("你好")
# → "unknown"
```

**完整 OCR 分析流程（需要 Tesseract 安裝）：**
```python
from src.analyzer.ocr_analyzer import OcrAnalyzer
from src.models.config import AppConfig

analyzer = OcrAnalyzer()
config = AppConfig()

result = analyzer.analyze("payment_screenshot.jpg", config)
# result.amount → Decimal("500.00") 或 None
# result.payment_method → "payme" / "fps" / "bank_transfer" / None
# result.confidence → 0.0 - 1.0
# result.needs_review → True（如果 confidence < 0.5）
# result.error → None（成功）或 "無法讀取文件"（失敗）
```

**信心度計算邏輯：**
```
OCR 返回空字串 → confidence = 0.0
有文字但無金額無付款方式 → confidence = 0.3
有文字 + 有金額 → confidence = 0.65
有文字 + 有付款方式 → confidence = 0.65
有文字 + 有金額 + 有付款方式 → confidence = 1.0
```

**錯誤處理（永遠唔 raise exception）：**
```python
# 文件唔存在
result = analyzer.analyze("/nonexistent.jpg", config)
result.error  # "無法讀取文件"
result.confidence  # 0.0
result.needs_review  # True

# 唔支援嘅格式
result = analyzer.analyze("file.bmp", config)
result.error  # "唔支援嘅圖片格式: .bmp"

# Tesseract 未安裝
result = analyzer.analyze("test.jpg", config)
result.error  # "Tesseract OCR 執行失敗"
```

---

## 整體 Pipeline 流程

```
Task 1 (Data Models)
  ↓ 提供 ParsedMessage、ImageAnalysisResult、AppConfig
Task 2 (Regex Patterns)
  ↓ 提供 match_message_line()、parse_timestamp()
Task 3 (Text Parser)
  ↓ parse_chat_file() → list[ParsedMessage]
Task 4 (Image Analyzer)
  ↓ OcrAnalyzer.analyze() → ImageAnalysisResult

  ↓↓ 兩者嘅結果會喺 Task 6-8 整合成 TransactionRecord
```

---

## 跑所有 Tests 嘅快速方法

如果你想一次過驗證所有 Task：

```bash
# 方法 1：逐個 Task 跑
cd output/assignment-002 && pytest tests/ -v && cd ../..
cd output/assignment-004 && pytest tests/ -v && cd ../..
cd output/assignment-006 && pytest tests/ -v && cd ../..
cd output/assignment-010 && pytest tests/ -v && cd ../..

# 方法 2：合併到一個項目目錄後跑（需要手動合併）
# 將所有 src/ 同 tests/ 合併到同一個目錄，然後：
pytest tests/ -v --tb=short
```

### 依賴安裝

```bash
pip install pydantic==2.5.0 openpyxl==3.1.2 click==8.1.7 pillow==10.1.0 pytesseract==0.3.10 python-dotenv==1.0.0 pyyaml==6.0.1 pytest==7.4.3
```

**注意：** 跑 tests 唔需要安裝 Tesseract OCR（所有 OCR tests 都用 mock）。只有實際使用 `OcrAnalyzer` 分析真實圖片時先需要安裝。
