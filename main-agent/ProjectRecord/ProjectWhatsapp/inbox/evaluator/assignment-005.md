# Assignment 005

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-28T12:30:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 2: WhatsApp Text Parser — Regex Patterns
- **TaskID**: ProjectWhatsapp/Task-2
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 2 代碼：WhatsApp Text Parser Regex Patterns + Utility Functions + Unit Tests。

## Context
- 代碼位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-004/`
- 原始需求：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 2 section）
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Generator 回覆：`./ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-004-reply-completed.md`
- 技術棧：Python 3.9+、pytest
- Generator 報告 105 tests passed

### 代碼文件清單
```
output/assignment-004/
├── src/
│   └── parser/
│       ├── __init__.py
│       ├── patterns.py       # MESSAGE_PATTERN, ATTACHMENT_PATTERN, system message detection
│       └── utils.py          # parse_timestamp, normalize_date_string, split_sender_content
└── tests/
    └── test_parser/
        ├── __init__.py
        └── test_patterns.py  # 105 tests
```

## 驗證標準
- [ ] 定義主訊息 regex pattern 支援所有格式變體
- [ ] 支援 24 小時制同 12 小時制（AM/PM）格式
- [ ] 支援日期順序變體（YYYY/MM/DD、DD/MM/YYYY、MM/DD/YYYY）
- [ ] 支援日期分隔符變體（/、-、.）
- [ ] 定義系統訊息識別 patterns
- [ ] 定義 `<attached:filename>` 提取 pattern
- [ ] 所有 patterns 有對應嘅單元測試，覆蓋率 > 90%
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] sender 含冒號時正確分割

## Test Criteria（從 Planner Specs）
- **Happy Path**: 標準格式正確匹配並提取 timestamp/sender/content；12小時制正確解析
- **Error Path**: 唔符合 pattern 嘅行返回 None；空字串唔 crash
- **Edge Case**: sender 含冒號正確分割；無效日期（31/02）pattern 匹配但 datetime 轉換失敗處理

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
