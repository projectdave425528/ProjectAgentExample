# Assignment 006

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-28T14:00:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 3: WhatsApp Text Parser — 主解析邏輯
- **TaskID**: ProjectWhatsapp/Task-3
- **TaskStatus**: pending → in_progress

## 需求
實現完整嘅 WhatsApp .txt 文件解析器。逐行讀取文件，用 Task 2 已完成嘅 regex patterns 解析每條訊息，處理多行訊息、系統訊息、media attachments。輸出 ParsedMessage 列表。

必須同時提供 unit test（pytest）+ sample_chat.txt fixture。

## Context
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Tasks Spec：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 3）
- Task 1 代碼（models）：`./ProjectRecord/ProjectWhatsapp/output/assignment-002/src/models/`
- Task 2 代碼（patterns + utils）：`./ProjectRecord/ProjectWhatsapp/output/assignment-004/src/parser/`
- 技術棧：Python 3.9+、pytest
- 代碼輸出位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-006/`

### 依賴嘅已完成代碼
- `src/models/message.py` — ParsedMessage model（timestamp, sender, content, is_system_message, attachments, raw_text）
- `src/parser/patterns.py` — MESSAGE_PATTERN, is_system_message(), extract_attachment(), match_message_line(), split_sender_content()
- `src/parser/utils.py` — parse_timestamp()

### 解析邏輯要求
1. 逐行讀取 .txt 文件
2. 用 `match_message_line(line)` 判斷係咪新訊息開頭
3. 如果匹配 → 建立新 ParsedMessage
4. 如果唔匹配 → 附加到前一條訊息嘅 content（多行訊息）
5. 用 `parse_timestamp()` 轉換時間戳
6. 用 `is_system_message()` 標記系統訊息
7. 用 `extract_attachment()` 提取附件

## 驗證標準
- [ ] `text_parser.py` 實現 `parse_chat_file(file_path: str) -> list[ParsedMessage]`
- [ ] 正確處理多行訊息（無時間戳嘅行歸屬前一條訊息）
- [ ] 正確識別並標記系統訊息
- [ ] 正確提取 `<attached:filename>` 到 attachments 列表
- [ ] 處理空文件（返回空列表 + warning log）
- [ ] 處理大文件（>10MB，分段讀取唔會 OOM）
- [ ] 自動偵測時間格式（唔需要用戶指定）
- [ ] 無法解析嘅行記錄 warning 並跳過

## Test Criteria
- **Happy Path**: 10 條標準格式訊息嘅 .txt 文件正確解析為 10 個 ParsedMessage；含 attachment 嘅訊息正確填充 attachments 列表
- **Error Path**: 文件路徑唔存在時 raise FileNotFoundError 並有清晰錯誤訊息；文件編碼非 UTF-8 時嘗試其他編碼或報錯
- **Edge Case**: 空文件返回空列表；單行超長訊息（>10000字）正確處理；連續多行無時間戳全部歸屬前一條訊息

## 預期輸出
代碼文件 + unit test + fixture，放喺 `./ProjectRecord/ProjectWhatsapp/output/assignment-006/`：
```
output/assignment-006/
├── src/
│   └── parser/
│       └── text_parser.py
└── tests/
    ├── test_parser/
    │   └── test_text_parser.py
    └── fixtures/
        └── sample_chat.txt
```
