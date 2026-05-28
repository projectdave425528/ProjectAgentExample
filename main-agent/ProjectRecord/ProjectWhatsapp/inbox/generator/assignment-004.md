# Assignment 004

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-28T12:00:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 2: WhatsApp Text Parser — Regex Patterns
- **TaskID**: ProjectWhatsapp/Task-2
- **TaskStatus**: pending → in_progress

## 需求
實現 WhatsApp 對話文件嘅 regex patterns，支援多種時間格式（12/24小時制、唔同日期順序）。定義 pattern 常量同 utility functions。

必須同時提供 unit test（pytest），覆蓋率 > 90%。

## Context
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Tasks Spec：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 2）
- Task 1 已完成嘅代碼：`./ProjectRecord/ProjectWhatsapp/output/assignment-002/`（可 import src.models）
- 技術棧：Python 3.9+、pytest
- 代碼輸出位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-004/`

### WhatsApp 匯出格式範例
```
[2024/01/15, 14:30:00] John: Hello
[2024/01/15, 14:30:05] 陳大文: 你好
[1/15/24, 2:30 PM] John: Hi there
[15/01/2024, 14:30:00] John: Hello
[2024-01-15, 14:30:00] John: Hello
[2024.01.15, 14:30:00] John: Hello
[2024/01/15, 14:30:00] John: <attached: IMG-20240115-WA0001.jpg>
[2024/01/15, 14:30:00] System: 陳大文 加入了群組
[2024/01/15, 14:30:00] Dr. Wong: 醫生: 你好
```

### 系統訊息範例
- 「XXX 加入了群組」
- 「XXX 更改了群組名稱」
- 「XXX 已離開」
- 「你已被移除」
- 「訊息已刪除」

## 驗證標準
- [ ] 定義主訊息 regex pattern：`[YYYY/MM/DD, HH:MM:SS] Sender: Message`
- [ ] 支援 24 小時制同 12 小時制（AM/PM）格式
- [ ] 支援日期順序變體（YYYY/MM/DD、DD/MM/YYYY、MM/DD/YYYY）
- [ ] 支援日期分隔符變體（/、-、.）
- [ ] 定義系統訊息識別 patterns
- [ ] 定義 `<attached:filename>` 提取 pattern
- [ ] 所有 patterns 有對應嘅單元測試，覆蓋率 > 90%

## Test Criteria
- **Happy Path**: 標準格式 `[2024/01/15, 14:30:00] John: Hello` 正確匹配並提取 timestamp/sender/content；12小時制 `[1/15/24, 2:30 PM] John: Hi` 正確解析
- **Error Path**: 完全唔符合任何 pattern 嘅行返回 None/不匹配；空字串輸入唔 crash
- **Edge Case**: sender 名稱含冒號（如 `Dr. Wong: 醫生`）時正確分割；日期 `31/02/2024`（無效日期）時 pattern 匹配但後續 datetime 轉換失敗處理

## 預期輸出
代碼文件 + unit test，放喺 `./ProjectRecord/ProjectWhatsapp/output/assignment-004/`：
```
output/assignment-004/
├── src/
│   └── parser/
│       ├── __init__.py
│       ├── patterns.py       # Regex pattern 常量
│       └── utils.py          # 時間格式轉換 utility functions
└── tests/
    └── test_parser/
        ├── __init__.py
        └── test_patterns.py  # 覆蓋率 > 90%
```
