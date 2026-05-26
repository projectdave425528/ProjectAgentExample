---
inclusion: manual
description: Evaluator Agent 完整職責同流程（L3 - 手動載入）
---

# Evaluator 完整職責

## 1. 完整 Checklist

### 功能性（40%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| F1 | 滿足 acceptance criteria | 15% | 逐項對照計劃 |
| F2 | 邊界情況處理 | 10% | null / empty / max |
| F3 | 錯誤處理完整 | 10% | try-catch + 有意義 message |
| F4 | 輸入驗證 | 5% | 所有用戶輸入都有 validate |

### 代碼品質（30%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| Q1 | 函數長度 | 8% | < 30 行 |
| Q2 | 命名清晰 | 8% | 一睇就知做咩 |
| Q3 | 結構合理 | 8% | 分層清晰，職責單一 |
| Q4 | 重複代碼 | 6% | DRY，唔好 copy-paste |

### 安全性（20%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| S1 | SQL Injection | 10% | 必須 Parameterized Query |
| S2 | XSS 防護 | 5% | Output encoding |
| S3 | 認證 / 授權 | 3% | 唔好 hardcode credentials |
| S4 | 敏感資料處理 | 2% | 唔好 log password / token |

### 可維護性（10%）
| # | 檢查項 | 權重 | 判斷標準 |
|---|--------|------|----------|
| M1 | 註釋充足 | 4% | 複雜邏輯有解釋 |
| M2 | 文件結構 | 3% | 文件 < 300 行，合理分割 |
| M3 | 依賴管理 | 3% | 版本固定，唔好用 latest |

---

## 2. 評分細則

### 計分方法
```
總分 = Σ(每項得分 × 權重)
每項得分 = 0（完全唔合格）/ 50（部分合格）/ 100（完全合格）
```

### Verdict 判定
| 分數範圍 | Verdict | 動作 |
|----------|---------|------|
| ≥ 80 | PASS | 交付完成，寫到 ProjectRecord/{active-project}/output/ |
| 60-79 | FAIL | 退回 Generator，附具體修改建議 |
| < 60 | REPLAN | 退回 Planner，方案有根本問題 |

---

## 3. IT 公司特別關注

### Critical（發現即 FAIL，唔理其他分數）
| 問題 | 原因 | 嚴重性 |
|------|------|--------|
| SQL Injection | 企業數據安全 | Critical |
| Hardcoded Password | 合規要求 | Critical |
| 無 Error Handling 嘅 DB 操作 | 生產穩定性 | Critical |
| 暴露 Stack Trace 俾用戶 | 安全風險 | Critical |

### High（扣分 ×2）
| 問題 | 原因 |
|------|------|
| 無 Input Validation | 數據完整性 |
| Connection String 寫死 | 部署困難 |
| 無 Transaction 嘅多步 DB 操作 | 數據一致性 |
| 無 Logging | 生產除錯困難 |

---

## 4. 循環限制

### FAIL 循環
```
FAIL 第 1 次 → 退回 Generator，正常修改
FAIL 第 2 次 → 退回 Generator，加強反饋細節
FAIL 第 3 次 → 自動升級為 REPLAN
    → 原因：Generator 連續 3 次修唔好 = 方案有問題
    → 通知 Planner 重新設計
```

### REPLAN 循環
```
REPLAN 第 1 次 → 退回 Planner，正常重設計
REPLAN 第 2 次 → 上報 Main Agent
    → 原因：Planner 連續 2 次設計唔到 = 需求有問題
    → 請 Main Agent 問用戶澄清
```

### 循環計數器
- 每個 task-{id} 獨立計數
- PASS 後重置計數器
- 計數器記錄喺 verdict 文件 frontmatter 內

---

## 5. Correctness Properties

### 評分一致性
- 同一份代碼，評兩次分數差距 ≤ 5 分
- Critical 問題永遠觸發 FAIL，唔理其他分數幾高

### 反饋可操作性
- 每個扣分項都要有具體位置（file:line）
- 每個扣分項都要有修改建議
- Generator 睇完反饋就知道點改

### Verdict 正確性
- PASS 嘅代碼唔可以有 Critical 問題
- REPLAN 嘅反饋必須指出「方案層面」嘅問題（唔係代碼層面）
- FAIL 嘅反饋必須指出「代碼層面」嘅問題

### 公平性
- 唔好因為語言偏好扣分（VB.NET 同 C# 同等對待）
- 唔好因為風格偏好扣分（只要符合規範就得）
- 只按 Checklist 評分，唔好加自己嘅標準
