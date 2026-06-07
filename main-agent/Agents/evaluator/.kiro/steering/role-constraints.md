---
inclusion: manual
description: Evaluator 角色限制 + 評分細則 + 循環限制（L3）
---

# Evaluator 角色限制

## 完整 Checklist

### 功能性（30%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| F1 | 滿足 acceptance criteria | 12% | 逐項對照計劃 |
| F2 | 邊界情況處理 | 8% | null / empty / max |
| F3 | 錯誤處理完整 | 6% | try-catch + 有意義 message |
| F4 | 輸入驗證 | 4% | 所有用戶輸入都有 validate |

### 代碼品質（25%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| Q1 | 函數長度 | 7% | < 30 行 |
| Q2 | 命名清晰 | 7% | 一睇就知做咩 |
| Q3 | 結構合理 | 6% | 分層清晰，職責單一 |
| Q4 | 重複代碼 | 5% | DRY |

### 安全性（20%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| S1 | SQL Injection | 10% | 必須 Parameterized Query |
| S2 | XSS 防護 | 5% | Output encoding |
| S3 | 認證/授權 | 3% | 唔好 hardcode credentials |
| S4 | 敏感資料 | 2% | 唔好 log password/token |

### 可測試性（15%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| T1 | Test 存在 | 5% | 每個 public method 都有 test |
| T2 | Test 覆蓋度 | 4% | Happy + Error + Edge |
| T3 | Test 獨立性 | 3% | 唔依賴執行順序/外部服務 |
| T4 | Test 可讀性 | 3% | 命名清晰、AAA pattern |

### 可維護性（10%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| M1 | 註釋充足 | 4% | 複雜邏輯有解釋 |
| M2 | 文件結構 | 3% | 文件 < 300 行 |
| M3 | 依賴管理 | 3% | 版本固定 |

## 計分方法
```
總分 = Σ(每項得分 × 權重)
每項得分 = 0（完全唔合格）/ 50（部分合格）/ 100（完全合格）
```

## Critical 問題（發現即 FAIL）
| 問題 | 原因 |
|------|------|
| SQL Injection | 企業數據安全 |
| Hardcoded Password | 合規要求 |
| 無 Error Handling 嘅 DB 操作 | 生產穩定性 |
| 暴露 Stack Trace | 安全風險 |
| 完全冇 Unit Test | 品質保證基本要求 |
| Test 全部冇 Assert | 假 test |
| Test 依賴真實外部服務 | 唔可重複/獨立 |

## 循環限制
- FAIL 第 1 次 → 退回 Generator，正常修改
- FAIL 第 2 次 → 退回 Generator，加強反饋
- FAIL 第 3 次 → 自動升級為 REPLAN
- REPLAN 第 1 次 → 退回 Planner
- REPLAN 第 2 次 → 上報 Main Agent

## Correctness Properties
- 同一份代碼，評兩次分數差距 ≤ 5 分
- Critical 問題永遠觸發 FAIL
- 每個扣分項都要有具體位置（file:line）+ 修改建議
- PASS 嘅代碼唔可以有 Critical 問題
- 唔好因為語言/風格偏好扣分
