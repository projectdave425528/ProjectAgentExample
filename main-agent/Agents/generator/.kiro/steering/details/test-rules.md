---
inclusion: manual
description: Generator 自動測試規則（L3 - 手動載入）
---

# Generator 自動測試規則（必須遵守，零例外）

> 本文件係 L3（manual）。Generator 開始生成代碼前先 `read_file` 載入。
> 由 `00-index.md`（L1）瘦身搬出，內容不變。

## 核心原則
- **每個 Task 必須同時產出 production code + unit test**
- **Test 先行思維** — 寫 code 前先想點 test（唔係 TDD，但要有 test 意識）
- **冇 test = 任務未完成** — Evaluator 會因為冇 test 直接 FAIL

## Test 結構要求
1. **獨立性** — 每個 test 可以單獨 run，唔依賴其他 test 嘅執行順序
2. **可重複** — Run 100 次結果一樣（唔依賴時間、隨機數、外部服務）
3. **快速** — 單個 test < 1 秒（mock 所有外部依賴）
4. **清晰命名** — `test_{功能}_{場景}_{預期結果}` 或 `{Method}_Should{Expected}_When{Condition}`

## Test 覆蓋要求
| 類型 | 最低要求 | 說明 |
|------|----------|------|
| Happy Path | 每個 public method 至少 1 個 | 正常輸入 → 正確輸出 |
| Error Path | 每個可能出錯嘅地方 1 個 | 錯誤輸入 → 正確錯誤處理 |
| Edge Case | 每個 Task 至少 2 個 | null / empty / boundary |
| Integration Point | 每個外部依賴 1 個 mock test | 確認 interface 正確使用 |
| Integration Test | 每個多模組互動 Task 至少 1 個 | 驗證真實模組之間嘅數據流 |

## Integration Test 規則
> 當 Task 涉及多個模組/服務互動時，除咗 Unit Test 仲要寫 Integration Test。

**觸發條件（任何一個符合就要寫）：**
- Task 涉及 2 個或以上模組嘅互動
- Task 涉及 DB 讀寫（CRUD）
- Task 涉及 API endpoint（HTTP request/response）
- Task 涉及 message queue / event bus
- Planner 嘅 Integration Points 欄有列出互動

**Integration Test 要求：**
1. 用真實嘅模組（唔係 mock），但用 test 環境（test DB、test config）
2. 測試完整嘅數據流（input → processing → output）
3. 包含 setup（準備 test data）同 teardown（清理）
4. 命名：`{filename}.integration.test.{ext}` 或 `{filename}_integration_test.{ext}`
5. 同 unit test 分開文件，方便獨立執行

**Integration Test 環境隔離：**
| 依賴類型 | 隔離方法 |
|---------|---------|
| Database | In-memory DB（SQLite）或 test container |
| External API | Mock server（wiremock / nock / responses） |
| File System | Temp directory |
| Message Queue | In-memory queue |

## 可測試性設計模式
```
✅ 正確：依賴注入（DI）
class UserService:
    def __init__(self, repository: IUserRepository):
        self._repo = repository

❌ 錯誤：直接 new 依賴
class UserService:
    def __init__(self):
        self._repo = UserRepository()  # 無法 mock
```

## Test 文件放置
- Test 文件同 production code 放同一個 output 目錄
- 命名：`{filename}.test.{ext}` 或 `{filename}_test.{ext}` 或 `Test{filename}.{ext}`
- 例如：`user-service.ts` → `user-service.test.ts`

## Test Framework 選擇（按語言）
| 語言 | Framework | Mock Library |
|------|-----------|--------------|
| C# | xUnit / NUnit | Moq / NSubstitute |
| VB.NET | xUnit / NUnit | Moq |
| Python | pytest | unittest.mock / pytest-mock |
| Node.js / TS | Jest / Vitest | jest.mock / vi.mock |

## Test 模板
每個 test file 必須包含：
1. **Arrange** — 準備 test data + mock
2. **Act** — 執行被測試嘅 function
3. **Assert** — 驗證結果

```
// 範例結構
describe('UserService', () => {
  describe('getById', () => {
    it('should return user when valid id', () => { /* happy path */ })
    it('should throw NotFound when id not exist', () => { /* error path */ })
    it('should handle null id', () => { /* edge case */ })
  })
})
```
