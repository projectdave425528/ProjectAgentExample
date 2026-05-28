# Assignment 002

- **From**: main-agent
- **To**: generator
- **Timestamp**: 2026-05-28T10:30:00+08:00
- **Type**: generate-request
- **TaskRef**: Task 1: 項目初始化 + Data Models
- **TaskID**: ProjectWhatsapp/Task-1
- **TaskStatus**: pending → in_progress

## 需求
根據 Design Spec 同 Task 1 嘅定義，建立項目結構、定義所有 Pydantic data models（ParsedMessage、ImageAnalysisResult、TransactionRecord、AppConfig），同埋建立 config 載入機制（.env + config.yaml）。

必須同時提供 unit test（pytest）。

## Context
- Design Spec：`./ProjectRecord/ProjectWhatsapp/specs/design.md`
- Tasks Spec：`./ProjectRecord/ProjectWhatsapp/specs/tasks.md`（Task 1）
- 技術棧：Python 3.9+、Pydantic v2、pytest
- 代碼輸出位置：`./ProjectRecord/ProjectWhatsapp/output/assignment-002/`

### Data Model 定義（從 Design Spec）

**ParsedMessage**: timestamp(datetime), sender(str), content(str), is_system_message(bool=False), attachments(list[str]=[]), raw_text(str)

**ImageAnalysisResult**: filename(str), image_date(date|None), analysis_mode(Literal["ocr","ai_vision"]), payment_method(Literal["payme","fps","bank_transfer","unknown"]|None), amount(Decimal|None), transaction_date(date|None), transaction_id(str|None), confidence(float 0-1), raw_text(str|None), needs_review(bool=False), error(str|None)

**TransactionRecord**: id(str UUID), date(date), customer_name(str), repair_item(str|None), quoted_amount(Decimal|None), received_amount(Decimal|None), payment_method(Literal["payme","fps","bank_transfer","cash","unknown"]|None), payment_status(Literal["paid","unpaid","partial"]), source_messages(list[int]=[]), source_images(list[str]=[]), notes(str=""), confidence(float 0-1), needs_review(bool=False)

**AppConfig**: analysis_mode(Literal["ocr","ai_vision"]="ocr"), ai_vision_api_key(str|None), tesseract_path(str|None), output_dir(str="./output"), confidence_threshold(float=0.7), language(str="chi_tra+eng")

## 驗證標準
- [ ] 項目目錄結構已建立（src/、tests/、docs/）
- [ ] requirements.txt 包含所有核心依賴（pinned versions）
- [ ] src/models/ 下所有 data model 已定義
- [ ] Pydantic model 有正確嘅 type hints 同 validators
- [ ] src/config.py 可以載入 .env 同 config.yaml
- [ ] .env.example 已建立（包含 API Key placeholder）
- [ ] config.yaml 有合理嘅預設值
- [ ] pytest 可以成功 import 所有 models
- [ ] Unit test 覆蓋 Happy Path + Error Path + Edge Case

## Test Criteria
- **Happy Path**: 建立 ParsedMessage 實例所有欄位正確賦值同序列化為 JSON；AppConfig 從有效 config.yaml 載入所有欄位值正確；TransactionRecord UUID 自動生成且唯一
- **Error Path**: ParsedMessage 缺少必填欄位時 raise ValidationError；AppConfig 載入唔存在嘅 yaml 時用預設值；ImageAnalysisResult confidence 超出 0-1 範圍時 raise ValidationError
- **Edge Case**: sender 包含 emoji/特殊字符時正確保存；amount 為 Decimal("0.00") 時正確處理；tesseract_path 為 None 時正常運作

## 預期輸出
完整可運行嘅代碼文件 + unit test，放喺 `./ProjectRecord/ProjectWhatsapp/output/assignment-002/` 目錄
