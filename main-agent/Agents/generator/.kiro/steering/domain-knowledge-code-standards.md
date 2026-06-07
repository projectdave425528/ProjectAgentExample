---
inclusion: manual
description: Generator 代碼規範（L3 - 手動載入）
---

# 代碼規範

> 寫 code 時讀取。包含結構、命名、安全、錯誤處理、可測試性規範。

## 1. 結構規範
| 規則 | 限制 |
|------|------|
| 函數長度 | < 30 行 |
| 參數數量 | ≤ 3 個（超過用 object） |
| Loop 嵌套 | ≤ 3 層 |
| 文件長度 | < 300 行 |
| Class 方法數 | ≤ 10 個 |

## 2. 命名規範

### 通用
| 類型 | 格式 | 例子 |
|------|------|------|
| 變數 | camelCase | `userName` |
| Class | PascalCase | `UserService` |
| 常數 | UPPER_SNAKE | `MAX_RETRY` |
| 文件 | kebab-case / PascalCase | `user-service.ts` |

### 語言特定
| 語言 | 函數命名 |
|------|----------|
| C# / VB.NET | PascalCase |
| JavaScript / TypeScript | camelCase |
| Python | snake_case |

## 3. 安全規範

### Critical（違反即 FAIL）
- SQL：必須用 Parameterized Query
- Auth：唔好 hardcode credentials
- Error：唔好暴露 stack trace 俾用戶
- Log：唔好 log 敏感資料

### 安全代碼範例
```csharp
// ✅ 正確：Parameterized Query
var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = @id", conn);
cmd.Parameters.AddWithValue("@id", userId);

// ❌ 錯誤：String Concatenation
var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = " + userId, conn);
```

```python
# ✅ 正確：Parameterized Query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# ❌ 錯誤：f-string
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### High（強烈建議）
- Input：所有用戶輸入必須 validate
- XSS：Output 必須 encode
- CSRF：表單操作要有 token
- Connection String：用 config / environment variable

## 4. 錯誤處理

### 規則
- 每個外部調用（DB / API / File）都要 try-catch
- Error message 要有意義
- 區分 user error vs system error
- System error 要 log，user error 返回友好訊息

### 錯誤處理模板
```csharp
try
{
    var result = await _repository.GetByIdAsync(id);
    if (result == null)
        return NotFound($"Record with ID {id} not found");  // User error
    return Ok(result);
}
catch (SqlException ex)
{
    _logger.LogError(ex, "Database error when fetching record {Id}", id);
    return StatusCode(500, "Internal server error");  // 唔暴露細節
}
```

### 錯誤分類
| 類型 | 處理方式 |
|------|----------|
| Validation Error | 返回 400 + 具體原因 |
| Not Found | 返回 404 |
| Auth Error | 返回 401/403 |
| System Error | 返回 500 + log 詳情 |

## 5. 可測試性設計

### 依賴注入（DI）— 所有外部依賴必須可注入
```csharp
// ✅ 正確：透過 constructor 注入 interface
public class UserService
{
    private readonly IUserRepository _repo;
    private readonly ILogger<UserService> _logger;
    public UserService(IUserRepository repo, ILogger<UserService> logger)
    {
        _repo = repo;
        _logger = logger;
    }
}

// ❌ 錯誤：直接 new 具體 class
public class UserService
{
    private readonly UserRepository _repo = new UserRepository();
}
```

```python
# ✅ 正確：依賴注入
class UserService:
    def __init__(self, repository: IUserRepository, logger: ILogger):
        self._repo = repository
        self._logger = logger

# ❌ 錯誤：直接建立依賴
class UserService:
    def __init__(self):
        self._repo = UserRepository("connection_string")
```

### Interface 分離 — 外部依賴必須有 interface
```csharp
// ✅ 定義 interface
public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id);
    Task<IEnumerable<User>> GetAllAsync();
    Task<int> CreateAsync(User user);
}
```

### Pure Function 優先 — 業務邏輯盡量寫成 pure function
```python
# ✅ Pure function — 容易 test
def calculate_discount(price: float, membership_level: str) -> float:
    rates = {"gold": 0.2, "silver": 0.1, "bronze": 0.05}
    return price * rates.get(membership_level, 0)

# ❌ 有 side effect — 難 test
def apply_discount(order_id: int) -> None:
    order = db.get_order(order_id)  # side effect
    order.price *= 0.8
    db.save(order)  # side effect
```

### 分層架構 — Controller → Service → Repository（interface）→ DB

### 避免 Static / Global State
```csharp
// ❌ 錯誤：static method 依賴 global state
public static class UserHelper
{
    public static User GetCurrentUser() => HttpContext.Current.User;  // 無法 mock
}

// ✅ 正確：注入 context
public class UserHelper
{
    private readonly IHttpContextAccessor _context;
    public UserHelper(IHttpContextAccessor context) { _context = context; }
    public User GetCurrentUser() => _context.HttpContext.User;
}
```
