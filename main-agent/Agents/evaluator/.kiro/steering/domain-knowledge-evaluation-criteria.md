---
inclusion: manual
description: Evaluator 評分標準領域知識（L3）
---

# 評分標準領域知識

## IT 公司特別關注

### Critical（發現即 FAIL，唔理其他分數）
| 問題 | 原因 | 嚴重性 |
|------|------|--------|
| SQL Injection | 企業數據安全 | Critical |
| Hardcoded Password | 合規要求 | Critical |
| 無 Error Handling 嘅 DB 操作 | 生產穩定性 | Critical |
| 暴露 Stack Trace 俾用戶 | 安全風險 | Critical |
| 完全冇 Unit Test | 品質保證基本要求 | Critical |
| Test 有但全部冇 Assert | 假 test，冇驗證價值 | Critical |
| Test 依賴真實外部服務 | 唔可重複、唔可獨立 | Critical |

### High（扣分 ×2）
| 問題 | 原因 |
|------|------|
| 無 Input Validation | 數據完整性 |
| Connection String 寫死 | 部署困難 |
| 無 Transaction 嘅多步 DB 操作 | 數據一致性 |
| 無 Logging | 生產除錯困難 |

## 自動測試執行流程

### 執行步驟
1. 確認 test 文件存在（掃描 `*.test.*` / `*_test.*` / `Test*.*`）
2. 靜態分析 test 品質（assert/mock/命名/AAA）
3. 嘗試執行 test（確認 framework 已安裝）
4. 對照 Planner 嘅 Test Criteria

## 反饋寫作規則

### 必須遵守
- 每個扣分項都要有具體位置（file:line）
- 每個扣分項都要有修改建議
- FAIL 反饋要有優先順序
- REPLAN 反饋要指出方案層面嘅問題
- Test 反饋要具體（缺少邊個 test case）

### 禁止行為
- ❌ 模糊反饋（如「代碼品質差」）
- ❌ 冇位置嘅扣分
- ❌ 冇建議嘅扣分
- ❌ 主觀偏好扣分
- ❌ 只講「冇 test」但唔講需要咩 test

## Test 反饋格式

當 test 相關扣分時，必須提供以下格式：
```markdown
**缺少嘅 Test Case:**
- [ ] {method_name} - Happy Path: {描述預期 test}
- [ ] {method_name} - Error: {描述預期 test}
- [ ] {method_name} - Edge: {描述預期 test}

**Test 品質問題:**
- {test_file}:{line} — {問題描述} → {修改建議}
```
