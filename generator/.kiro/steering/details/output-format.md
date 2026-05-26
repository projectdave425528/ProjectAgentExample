---
inclusion: manual
description: Generator Agent 輸出格式模板（L3 - 手動載入）
---

# Generator 輸出格式

## 1. 完成報告格式

```markdown
---
task-id: "task-{id}"
from: generator
to: main-agent
type: reply
timestamp: YYYY-MM-DD HH:mm
status: done
files-generated: [文件列表]
---

## Task Completion Report

**Task ID**: task-{id}
**Status**: DONE

### 生成嘅文件
| 文件 | 用途 | 行數 |
|------|------|------|
| ... | ... | ... |

### 自我檢查
- [ ] 函數 < 30 行
- [ ] 參數 ≤ 3
- [ ] Loop ≤ 3 層
- [ ] Parameterized Query
- [ ] Input Validation
- [ ] Error Handling
- [ ] 有意義嘅命名

### 備註
- [任何需要 Evaluator 注意嘅嘢]
```

---

## 2. 常見項目模式

### 2.1 CRUD 模式
```
結構：
├── Models/          ← 數據模型
├── Controllers/     ← API 端點
├── Services/        ← 業務邏輯
├── Repositories/    ← 數據訪問
└── DTOs/            ← 數據傳輸對象

流程：Controller → Service → Repository → DB
```

### 2.2 API 模式
```
結構：
├── Routes/          ← 路由定義
├── Middleware/      ← 認證 / 日誌 / 錯誤處理
├── Handlers/        ← 請求處理
├── Services/        ← 業務邏輯
└── Models/          ← 數據模型

重點：Input validation、Rate limiting、Error handling
```

### 2.3 工具 / Script 模式
```
結構：
├── main.{ext}       ← 入口
├── config.{ext}     ← 配置
├── utils/           ← 工具函數
└── output/          ← 輸出目錄

重點：CLI 參數解析、Progress 顯示、Error recovery
```

### 2.4 報表模式
```
結構：
├── Queries/         ← SQL 查詢
├── DataSources/     ← 數據源連接
├── Transformers/    ← 數據轉換
├── Templates/       ← 報表模板
└── Output/          ← 生成嘅報表

重點：SQL 性能、數據準確性、格式化
```
