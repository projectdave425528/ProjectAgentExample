# Assignment 007

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-28T14:30:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 3: WhatsApp Text Parser — 主解析邏輯
- **TaskID**: ProjectWhatsapp/Task-3
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 3 代碼：WhatsApp Text Parser 主解析邏輯 + Unit Tests + Sample Fixture。

## Context
- 代碼位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-006/`
- 原始需求：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 3 section）
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Generator 回覆：`./ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-006-reply-completed.md`
- 依賴嘅 Task 2 代碼：`./ProjectRecord/ProjectWhatsapp/output/assignment-004/src/parser/`
- 技術棧：Python 3.9+、pytest
- Generator 報告 28 tests passed

### 代碼文件清單
```
output/assignment-006/
├── src/parser/text_parser.py          # 主解析邏輯
└── tests/
    ├── test_parser/test_text_parser.py  # 28 tests
    └── fixtures/sample_chat.txt         # 12 條訊息 fixture
```

## 驗證標準
- [ ] parse_chat_file() 正確解析標準格式訊息
- [ ] 多行訊息正確歸屬前一條
- [ ] 系統訊息正確標記
- [ ] attachment 正確提取
- [ ] 空文件返回空列表 + warning
- [ ] 大文件逐行讀取唔 OOM
- [ ] FileNotFoundError 有清晰訊息
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] Unit test 覆蓋 Happy Path + Error Path + Edge Case

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
