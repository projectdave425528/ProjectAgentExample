---
inclusion: manual
description: Generator 自動測試規則（L3 - 手動載入）
---

# 自動測試規則（必須遵守，零例外）

> 生成代碼前必讀。

## 核心原則
- **每個 Task 必須同時產出 production code + unit test**
- **Test 先行思維** — 寫 code 前先想點 test
- **冇 test = 任務未完成** — Evaluator 會直接 FAIL

## Test 結構要求
1. **獨立性** — 每個 test 可以單獨 run
2. **可重複** — Run 100 次結果一樣
3. **快速** — 單個 test < 1 秒（mock 所有外部依賴）
4. **清晰命名** — `test_{功能}_{場景}_{預期結果}` 或 `{Method}_Should{Expected}_When{Condition}`

## Test 覆蓋要求
| 類型 | 最低要求 |
|------|----------|
| Happy Path | 每個 public method 至少 1 個 |
| Error Path | 每個可能出錯嘅地方 1 個 |
| Edge Case | 每個 Task 至少 2 個 |
| Integration Point | 每個外部依賴 1 個 mock test |
| Integration Test | 每個多模組互動 Task 至少 1 個 |

## Integration Test 規則

**觸發條件（任何一個符合就要寫）：**
- Task 涉及 2+ 模組互動
- Task 涉及 DB 讀寫
- Task 涉及 API endpoint
- Task 涉及 message queue / event bus
- Planner 嘅 Integration Points 有列出

**要求：**
1. 用真實模組（唔係 mock），但用 test 環境
2. 測試完整數據流（input → processing → output）
3. 包含 setup + teardown
4. 命名：`{filename}.integration.test.{ext}`
5. 同 unit test 分開文件

**環境隔離：**
| 依賴類型 | 隔離方法 |
|---------|---------|
| Database | In-memory DB / test container |
| External API | Mock server |
| File System | Temp directory |
| Message Queue | In-memory queue |

## Test 文件放置
- 同 production code 放同一個 output 目錄
- 命名：`{filename}.test.{ext}` 或 `{filename}_test.{ext}`

## Test Framework 選擇
| 語言 | Framework | Mock Library |
|------|-----------|--------------|
| C# | xUnit / NUnit | Moq / NSubstitute |
| VB.NET | xUnit / NUnit | Moq |
| Python | pytest | unittest.mock / pytest-mock |
| Node.js / TS | Jest / Vitest | jest.mock / vi.mock |

## Test 模板（AAA）
```
Arrange — 準備 test data + mock
Act — 執行被測試嘅 function
Assert — 驗證結果
```

## 可測試性設計模式
```csharp
// ✅ 正確：依賴注入（DI）— 方便 mock
public class UserService
{
    private readonly IUserRepository _repo;
    public UserService(IUserRepository repo) { _repo = repo; }
}

// ❌ 錯誤：直接 new 依賴 — 無法 mock
public class UserService
{
    private readonly UserRepository _repo = new UserRepository();
}
```

```python
# ✅ 正確：依賴注入
class UserService:
    def __init__(self, repository: IUserRepository):
        self._repo = repository

# ❌ 錯誤：直接建立依賴
class UserService:
    def __init__(self):
        self._repo = UserRepository()  # 無法 mock
```
