# Clean Code: 核心概念整理

> 基於 Robert C. Martin《Clean Code: A Handbook of Agile Software Craftsmanship》

---

## 第 1 章：Clean Code（什麼是乾淨的代碼）

- **定義**：Clean code 係容易理解、容易修改、表達意圖清晰嘅代碼
- **核心理念**：代碼被閱讀嘅次數遠多於被編寫嘅次數
- **Boy Scout Rule**：離開時讓代碼比你發現時更乾淨
- **名人觀點**：
  - Bjarne Stroustrup：優雅且高效
  - Grady Booch：讀起來像散文
  - Dave Thomas：可被其他人增強
  - Ron Jeffries：無重複、表達力強、最小化

---

## 第 2 章：Meaningful Names（有意義的命名）

| 原則 | 說明 | 範例 |
|------|------|------|
| 意圖明確 | 名字應揭示目的 | ❌ `d` → ✅ `elapsedTimeInDays` |
| 避免誤導 | 唔好用容易混淆嘅名 | ❌ `accountList`（如果唔係 List）→ ✅ `accounts` |
| 有意義嘅區分 | 避免無意義嘅區分 | ❌ `a1, a2` → ✅ `source, destination` |
| 可發音 | 名字要讀得出 | ❌ `genymdhms` → ✅ `generationTimestamp` |
| 可搜索 | 用足夠長嘅名字 | ❌ `e` → ✅ `WORK_DAYS_PER_WEEK` |
| 類名用名詞 | | `Customer`, `Account`, `AddressParser` |
| 方法名用動詞 | | `postPayment`, `deletePage`, `save` |

---

## 第 3 章：Functions（函數）

- **短小**：函數應該盡可能短，理想 30 行以內
- **只做一件事**（Single Responsibility）：一個函數只做一件事，做好呢件事
- **一個抽象層級**：函數內嘅語句應在同一抽象層級
- **Step-down Rule**：代碼由上而下閱讀，每個函數後面跟住下一層抽象
- **參數數量**：
  - 最好 0 個（niladic）
  - 1 個可以（monadic）
  - 2 個勉強（dyadic）
  - 3 個以上要避免（triadic+）
- **無副作用**：函數唔應該有隱藏嘅副作用
- **Command-Query Separation**：一個函數要嘛做某事（command），要嘛回答某事（query），唔好兩者兼做
- **DRY**（Don't Repeat Yourself）：消除重複

---

## 第 4 章：Comments（註釋）

- **好的註釋**：
  - 法律註釋（版權聲明）
  - 提供信息（解釋正則表達式）
  - 解釋意圖（為什麼選擇某方案）
  - 警告後果
  - TODO 註釋
  - 放大重要性

- **壞的註釋**：
  - 自言自語
  - 多餘的註釋（代碼已經說清楚）
  - 誤導性註釋
  - 日誌式註釋（用 git log）
  - 噪音註釋（`/** The name */`）
  - 被註釋掉的代碼
  - 位置標記（`// ============`）

- **核心理念**：代碼應該自我解釋，註釋係代碼表達力不足嘅補償

---

## 第 5 章：Formatting（格式）

- **垂直格式**：
  - 文件唔好太長（200-500 行理想）
  - 概念之間用空行分隔
  - 相關概念垂直靠近
  - 變量聲明靠近使用位置
  - 被調用嘅函數應在調用者下方

- **水平格式**：
  - 行寬唔好超過 120 字符
  - 用空格突出優先級
  - 縮進表示層次結構

- **團隊規則**：整個團隊用同一套格式規則

---

## 第 6 章：Objects and Data Structures（對象與數據結構）

- **數據抽象**：隱藏實現，暴露抽象接口
- **對象 vs 數據結構**：
  - 對象：隱藏數據，暴露操作數據嘅函數
  - 數據結構：暴露數據，冇有意義嘅函數
- **Law of Demeter**（迪米特法則）：
  - 方法唔應該調用由其他方法返回嘅對象嘅方法
  - ❌ `ctxt.getOptions().getScratchDir().getAbsolutePath()`
  - ✅ 用一個方法封裝
- **DTO**（Data Transfer Object）：純數據結構，用於傳輸

---

## 第 7 章：Error Handling（錯誤處理）

- **用 Exception 而非返回碼**
- **先寫 try-catch-finally**：幫助定義 scope
- **用 Unchecked Exception**：Checked Exception 違反 OCP
- **提供 context**：異常信息要包含足夠上下文
- **根據調用者需要定義異常類別**
- **唔好返回 null**：用 Special Case Pattern 或空集合代替
- **唔好傳 null**：禁止將 null 作為參數傳遞

---

## 第 8 章：Boundaries（邊界）

- **Learning Tests**：用測試學習第三方 API
- **Adapter Pattern**：封裝第三方代碼，控制邊界
- **唔好讓第三方 API 散佈在代碼各處**
- **針對接口編程**：唔好依賴具體實現

---

## 第 9 章：Unit Tests（單元測試）

- **TDD 三定律**：
  1. 唔寫 production code 除非有一個失敗嘅 test
  2. 唔寫更多嘅 test 除非已經有一個失敗
  3. 唔寫更多嘅 production code 除非剛好讓失敗嘅 test 通過

- **F.I.R.S.T. 原則**：
  - **F**ast：測試要快
  - **I**ndependent：測試之間唔好互相依賴
  - **R**epeatable：任何環境都能跑
  - **S**elf-validating：通過或失敗，冇灰色地帶
  - **T**imely：在 production code 之前或同時寫

- **一個測試一個概念**
- **測試代碼同 production code 一樣重要**

---

## 第 10 章：Classes（類）

- **類要短小**：用職責衡量，唔係用行數
- **Single Responsibility Principle (SRP)**：一個類只有一個改變嘅理由
- **Cohesion（內聚性）**：類中嘅方法應操作類中嘅多個變量
- **保持內聚性會產生很多小類**：呢個係好事
- **Open-Closed Principle (OCP)**：對擴展開放，對修改封閉
- **Dependency Inversion Principle (DIP)**：依賴抽象，唔好依賴具體

---

## 第 11 章：Systems（系統）

- **Separation of Concerns**：構造（construction）同使用（use）分離
- **Dependency Injection**：控制反轉嘅一種機制
- **Cross-cutting Concerns**：用 AOP 處理橫切關注點
- **推遲決策**：唔好過早做架構決策
- **用 DSL**：Domain-Specific Language 提高表達力

---

## 第 12 章：Emergence（浮現式設計）

Kent Beck 嘅 4 條簡單設計規則（按優先級）：

1. **通過所有測試**（最重要）
2. **無重複**
3. **表達程序員意圖**
4. **最少化類和方法數量**

---

## 第 13 章：Concurrency（並發）

- **並發唔等於性能**：唔一定更快
- **設計會改變**：並發設計同單線程設計差異大
- **SRP 應用於並發**：並發代碼獨立於非並發代碼
- **限制數據作用域**：用 `synchronized` 保護共享數據
- **用數據副本**：避免共享
- **線程應盡量獨立**

---

## 第 14 章：Successive Refinement（逐步改進）

- **Case Study**：重構一個 command-line argument parser（`Args` class）
- **核心教訓**：
  - 冇人第一次就寫出 clean code，先寫 dirty code 再逐步清理
  - 重構係持續嘅過程，唔係一次性事件
  - 每次小改動後跑測試，確保行為唔變
  - **先讓它 work，再讓它 clean**
- **方法**：抽取方法 → 改名 → 分離職責 → 消除重複

---

## 第 15 章：JUnit Internals（JUnit 內部結構）

- **Case Study**：重構 JUnit 框架中嘅 `ComparisonCompactor` class
- **核心教訓**：
  - 即使係優秀嘅開源代碼都可以改善
  - 命名要更精確（`compact` → `formatCompactedComparison`）
  - 消除負邏輯（`!shouldNotBeCompacted()` → `canBeCompacted()`）
  - 隱藏實現細節，暴露清晰意圖
  - 條件邏輯應該被封裝

---

## 第 16 章：Refactoring SerialDate

- **Case Study**：重構 JCommon library 中嘅 `SerialDate` class
- **核心教訓**：
  - 先寫測試覆蓋現有行為，再開始重構
  - 類名應反映真實用途（`SerialDate` → `DayDate`）
  - 將唔屬於呢個類嘅職責移走
  - 用 Enum 取代 magic numbers / constants
  - Base class 唔應該知道 derived class 嘅存在
  - 移除死代碼同無用嘅註釋

---

## 第 17 章：Smells and Heuristics（壞味道與啟發）

> 呢章係全書嘅「參考手冊」，列出所有 code smells 同作者嘅經驗法則。

## 代碼壞味道（Code Smells）

### 環境類
- 構建需要多步
- 測試需要多步

### 函數類
- 太多參數
- 輸出參數
- Flag 參數（Boolean 參數）
- 死函數（從未被調用）

### 一般類
- 一個源文件多種語言
- 明顯行為未被實現
- 邊界處理不正確
- 重複
- 錯誤抽象層級
- 基類依賴派生類
- 信息過多（接口太寬）
- 死代碼
- 垂直分離（聲明同使用距離太遠）
- 不一致性
- 雜亂（無用嘅構造函數、未使用嘅變量）

### 命名類
- 用描述性名稱
- 名稱反映抽象層級
- 用標準命名法
- 名稱長度匹配作用域

---

## SOLID 原則（貫穿全書）

| 原則 | 全名 | 含義 |
|------|------|------|
| **S** | Single Responsibility | 一個類/函數只有一個改變嘅理由 |
| **O** | Open-Closed | 對擴展開放，對修改封閉 |
| **L** | Liskov Substitution | 子類能替代父類使用 |
| **I** | Interface Segregation | 客戶端唔應該被迫依賴唔用嘅接口 |
| **D** | Dependency Inversion | 依賴抽象，唔好依賴具體實現 |

---

## 實用 Checklist

寫代碼時問自己：
- [ ] 名字表達意圖嗎？
- [ ] 函數只做一件事嗎？
- [ ] 函數夠短嗎（< 20 行）？
- [ ] 參數少於 3 個嗎？
- [ ] 有冇重複代碼？
- [ ] 有冇副作用？
- [ ] 錯誤處理乾淨嗎？
- [ ] 註釋係必要嘅嗎？（代碼本身表達唔到？）
- [ ] 格式一致嗎？
- [ ] 有測試覆蓋嗎？
- [ ] 遵循 SRP 嗎？

---

*整理日期：2026-06-07*
*來源：基於 AI 訓練資料中對 Clean Code 核心概念嘅理解，非逐字引用*
