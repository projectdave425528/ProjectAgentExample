---
inclusion: manual
description: Evaluator Agent 輸出格式模板（L3 - 手動載入）
---

# Evaluator 輸出格式

## 1. PASS 反饋格式

```markdown
---
task-id: "assignment-{id}"
from: evaluator
to: main-agent
type: verdict
timestamp: YYYY-MM-DD HH:mm
verdict: PASS
score: [80-100]
fail-count: 0
test-executed: true/false
test-result: all-pass/partial-fail/not-executed
test-count: {total}/{pass}/{fail}
---

## Evaluation Verdict: PASS ✅

**Task ID**: assignment-{id}
**Score**: {score}/100

### 摘要
[一句話總結]

### Test 結果
| 指標 | 結果 |
|------|------|
| Test 文件數 | {N} |
| Test Case 總數 | {N} |
| Pass | {N} |
| Fail | {N} |
| 覆蓋度評估 | Happy ✅ / Error ✅ / Edge ✅ |

### 優點
- [值得保留嘅設計]

### 建議（非必須修改）
- [可以改善但唔影響交付嘅建議]
```

---

## 2. FAIL 反饋格式

```markdown
---
task-id: "assignment-{id}"
from: evaluator
to: main-agent
type: verdict
timestamp: YYYY-MM-DD HH:mm
verdict: FAIL
score: [60-79]
fail-count: [1-3]
test-executed: true/false
test-result: all-pass/partial-fail/no-test/not-executed
test-count: {total}/{pass}/{fail}
---

## Evaluation Verdict: FAIL ❌

**Task ID**: assignment-{id}
**Score**: {score}/100

### Test 結果
| 指標 | 結果 |
|------|------|
| Test 文件數 | {N} |
| Test Case 總數 | {N} |
| Pass | {N} |
| Fail | {N} |
| 失敗嘅 Test | [列出名稱 + 原因] |

### 必須修改
| # | 問題 | 位置 | 修改建議 |
|---|------|------|----------|
| 1 | ... | file:line | ... |
| 2 | ... | file:line | ... |

### 扣分明細
| 項目 | 得分 | 原因 |
|------|------|------|
| F1 | 50/100 | ... |
| T1 | 0/100 | 冇 test |
| S1 | 0/100 | ... |

### 修改優先順序
1. [最重要] ...
2. [次要] ...
```

---

## 3. REPLAN 反饋格式

```markdown
---
task-id: "assignment-{id}"
from: evaluator
to: main-agent
type: verdict
timestamp: YYYY-MM-DD HH:mm
verdict: REPLAN
score: [0-59]
fail-count: 0
replan-count: [1-2]
---

## Evaluation Verdict: REPLAN 🔄

**Task ID**: assignment-{id}
**Score**: {score}/100

### 根本問題
[解釋點解需要重新設計]

### 具體問題
1. [問題 1]
2. [問題 2]

### 建議方向
- [對 Planner 嘅建議]
```

---

## 4. 反饋寫作規則

### 必須遵守
- 每個扣分項都要有 **具體位置**（file:line）
- 每個扣分項都要有 **修改建議**（唔好只講問題唔講點改）
- FAIL 反饋要有 **優先順序**（Generator 知道先改邊個）
- REPLAN 反饋要指出 **方案層面** 嘅問題
- **Test 相關反饋必須具體** — 指出缺少邊個 test case、邊個 mock 唔正確

### 禁止行為
- ❌ 模糊反饋（如「代碼品質差」）
- ❌ 冇位置嘅扣分（如「某處有問題」）
- ❌ 冇建議嘅扣分（如「呢度唔好」）
- ❌ 主觀偏好扣分（如「我覺得應該用另一種寫法」）
- ❌ 只講「冇 test」但唔講需要咩 test

### Test 反饋格式
當 test 相關扣分時，必須提供：
```markdown
**缺少嘅 Test Case:**
- [ ] {method_name} - Happy Path: {描述預期 test}
- [ ] {method_name} - Error: {描述預期 test}
- [ ] {method_name} - Edge: {描述預期 test}

**Test 品質問題:**
- {test_file}:{line} — {問題描述} → {修改建議}
```
