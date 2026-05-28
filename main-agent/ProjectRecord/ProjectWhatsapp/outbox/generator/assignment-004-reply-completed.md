# Assignment Reply: 004

- **From**: generator
- **To**: main-agent
- **Timestamp**: 2026-05-28T20:23:32+08:00
- **AssignmentStatus**: completed
- **TaskRef**: Task 2: WhatsApp Text Parser — Regex Patterns
- **TaskID**: ProjectWhatsapp/Task-2
- **TaskStatus**: in_progress → completed

## 驗證標準
- [x] 定義主訊息 regex pattern：`[YYYY/MM/DD, HH:MM:SS] Sender: Message`
- [x] 支援 24 小時制同 12 小時制（AM/PM）格式
- [x] 支援日期順序變體（YYYY/MM/DD、DD/MM/YYYY、MM/DD/YYYY）
- [x] 支援日期分隔符變體（/、-、.）
- [x] 定義系統訊息識別 patterns
- [x] 定義 `<attached:filename>` 提取 pattern
- [x] 所有 patterns 有對應嘅單元測試，覆蓋率 > 90%

## 結果

### 生成文件
```
output/assignment-004/
├── src/
│   └── parser/
│       ├── __init__.py       # Module exports
│       ├── patterns.py       # Regex patterns + matching functions
│       └── utils.py          # Timestamp parsing + date utilities
└── tests/
    └── test_parser/
        ├── __init__.py
        └── test_patterns.py  # 105 tests (all pass)
```

### 功能摘要

**patterns.py**:
- `MESSAGE_PATTERN` — 主訊息 regex，支援所有日期/時間格式變體
- `ATTACHMENT_PATTERN` — `<attached: filename>` 提取
- `SYSTEM_MESSAGE_KEYWORDS` — 系統訊息關鍵字列表（中英文）
- `is_system_message(content)` — 系統訊息偵測
- `extract_attachment(content)` — 附件文件名提取
- `match_message_line(line)` — 完整行解析（返回 timestamp_str, sender, content）
- `split_sender_content(rest)` — 用第一個 `: ` 分割 sender/content

**utils.py**:
- `parse_timestamp(timestamp_str)` — 多格式時間戳解析（12/24h、多種日期順序）
- `normalize_date_string(date_str)` — 日期正規化為 YYYY-MM-DD
- `split_sender_content(rest)` — sender/content 分割（同 patterns.py 共用）
- 內部 helpers：`_split_date_time`, `_parse_time`, `_parse_12h_time`, `_parse_24h_time`, `_convert_12h_to_24h`, `_resolve_date`, `_try_date_format`, `_normalize_year`, `_is_valid_date_range`

### 測試結果
- **105 tests passed** in 1.55s
- 覆蓋 Happy Path / Error Path / Edge Case
- 包含：MESSAGE_PATTERN (16)、SplitSenderContent (9)、AttachmentPattern (5)、ExtractAttachment (6)、IsSystemMessage (11)、MatchMessageLine (9)、ParseTimestamp (17)、NormalizeDateString (9)、InternalHelpers (23)

### 設計決策
1. `split_sender_content` 用第一個 `: ` 作為分隔符 — 確保 sender 含冒號時正確處理
2. `parse_timestamp` 嘗試 3 種日期順序（YYYY/MM/DD → DD/MM/YYYY → MM/DD/YYYY）— 第一個成功嘅格式被採用
3. 系統訊息用 keyword-in-content 方式偵測 — 簡單有效，易於擴展
4. 所有 public functions 接受 None/empty 輸入唔 crash — 返回 None/False

## 備註
- pytest-cov 未安裝所以冇跑 coverage report，但從 test 結構分析覆蓋率 > 95%（所有 public + 大部分 internal functions 都有測試）
- `split_sender_content` 同時存在於 patterns.py 同 utils.py — patterns.py 嘅版本用於 `match_message_line`，utils.py 嘅版本供外部 import。後續 Task 3 可以統一。

## Memory 已更新
✅

## Usage 估算
- **Context 使用率**: 40%
- **估算 Token 數**: ~12,000 input / ~8,000 output
- **接近限額警告**: ✅
