# Assignment 003

- **From**: main-agent
- **To**: evaluator
- **Timestamp**: 2026-05-28T11:00:00+08:00
- **Type**: evaluate-request
- **TaskRef**: Task 1: 項目初始化 + Data Models
- **TaskID**: ProjectWhatsapp/Task-1
- **TaskStatus**: in_progress（等待評估）

## 需求
審查 Generator 產出嘅 Task 1 代碼：項目初始化 + Data Models（Pydantic v2）+ Config Loader + Unit Tests。

## Context
- 代碼位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-002/`
- 原始需求（Planner Specs）：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 1 section）
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`（Data Model section）
- Generator 回覆：`./ProjectRecord/ProjectWhatsapp/outbox/generator/assignment-002-reply-completed.md`
- 技術棧：Python 3.9+、Pydantic v2、pytest
- Generator 報告 54 tests passed

### 代碼文件清單
```
output/assignment-002/
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── models/
│       ├── __init__.py
│       ├── message.py         (ParsedMessage)
│       ├── image_result.py    (ImageAnalysisResult)
│       ├── transaction.py     (TransactionRecord)
│       └── config.py          (AppConfig)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py         (40 tests)
│   └── test_config.py         (14 tests)
├── requirements.txt
├── .env.example
├── config.yaml
└── setup.py
```

## 驗證標準
- [ ] 項目目錄結構正確（src/、tests/）
- [ ] requirements.txt 包含所有核心依賴（pinned versions）
- [ ] src/models/ 下所有 data model 已定義且符合 Design Spec
- [ ] Pydantic model 有正確嘅 type hints 同 validators
- [ ] src/config.py 可以載入 .env 同 config.yaml
- [ ] .env.example 已建立
- [ ] config.yaml 有合理嘅預設值
- [ ] Unit test 覆蓋 Happy Path + Error Path + Edge Case
- [ ] 函數 < 30 行、參數 ≤ 3
- [ ] 代碼品質：命名清晰、無安全問題

## Test Criteria（從 Planner Specs）
- **Happy Path**: ParsedMessage 實例正確賦值同序列化；AppConfig 從 yaml 載入正確；TransactionRecord UUID 自動生成且唯一
- **Error Path**: 缺少必填欄位 raise ValidationError；載入唔存在 yaml 用預設值；confidence 超出 0-1 raise ValidationError
- **Edge Case**: sender 含 emoji 正確保存；amount Decimal("0.00") 正確處理；tesseract_path None 正常運作

## 預期輸出
Verdict（PASS/FAIL/REPLAN）+ 評分 + 問題清單 + 修改建議
