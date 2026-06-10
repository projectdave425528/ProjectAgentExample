---
inclusion: always
description: 確定性任務優先用腳本（JS/TS）原則 — 所有 Agent 必須遵守
---

# Deterministic-First 原則

> **「可確定嘅嘢用代碼，唔確定嘅嘢用 AI」**

## 核心規則

當一個 Step 或 Task 符合以下任一條件時，Agent **必須**編寫一個 JS/TS 腳本去執行，**唔可以**用 LLM 推理代替：

1. **有標準答案** — 輸入同輸出有明確嘅對應關係（例：1+1=2）
2. **可驗證** — 結果可以用 assert/expect 判斷對錯
3. **重複性高** — 同一邏輯會跑 >1 次
4. **唔容許錯誤** — 精度要求高（金額計算、日期推算等）
5. **有明確規則** — 邏輯可以寫成 if/else 或 lookup table

## 適用場景一覽

| 場景 | 腳本做 | AI 做 |
|------|--------|-------|
| 測試斷言 | ✅ 寫 test runner 腳本 | ❌ |
| 會計帳目計算 | ✅ 寫計算腳本 | ❌ |
| 數學運算 | ✅ 寫算式腳本 | ❌ |
| 格式驗證（JSON/日期/email） | ✅ 寫 validator 腳本 | ❌ |
| 數據轉換（CSV→JSON） | ✅ 寫 transform 腳本 | ❌ |
| 字串解析（regex） | ✅ 寫 parser 腳本 | ❌ |
| 文件模板生成 | ✅ 寫 template engine | ❌ |
| 需求分析 | ❌ | ✅ AI 理解語意 |
| 架構設計 | ❌ | ✅ AI 綜合判斷 |
| 代碼審查意見 | ❌ | ✅ AI 品質評估 |
| 自然語言生成 | ❌ | ✅ AI 創作 |

## 各 Agent 適用方式

### Planner
- 設計任務時，標記每個 Step 係「deterministic」定「AI-driven」
- Deterministic Step 必須喺 acceptance criteria 寫明預期 input/output

### Generator
- 遇到 deterministic Step → 寫 JS/TS 腳本放入 `scripts/deterministic/`
- 腳本必須：可獨立執行（`node script.js`）、有 exit code（0=pass, 1=fail）、輸出 JSON 結果
- 唔好用 LLM 去做本應係腳本做嘅計算

### Evaluator
- 驗證 deterministic Step 時 → 直接跑腳本，唔好用 LLM 判斷結果
- 腳本 exit code = 0 → pass；≠ 0 → fail（零歧義）

## 腳本規範

```
scripts/deterministic/
├── _templates/
│   ├── deterministic-template.js     ← 通用模板
│   └── validator-template.js         ← 格式驗證模板
├── {project-name}/
│   ├── {task-id}-{description}.js   ← 主腳本
│   ├── {task-id}-{description}.test.js  ← 腳本自身嘅 test
│   └── README.md                     ← 說明文檔
```

### 腳本模板

```javascript
/**
 * @deterministic
 * @task {task-id}
 * @description {一句話描述}
 * @input {描述輸入}
 * @output {描述預期輸出}
 */

const assert = require('assert');

function main(input) {
  // 確定性邏輯（唔涉及 AI/LLM）
  const result = /* 計算 */;
  return result;
}

// 自帶驗證
function verify() {
  const testCases = [
    { input: /* ... */, expected: /* ... */ },
  ];

  for (const { input, expected } of testCases) {
    const actual = main(input);
    assert.deepStrictEqual(actual, expected,
      `FAIL: input=${JSON.stringify(input)}, expected=${JSON.stringify(expected)}, got=${JSON.stringify(actual)}`
    );
  }
  console.log(JSON.stringify({ status: 'PASS', cases: testCases.length }));
}

if (require.main === module) {
  verify();
}

module.exports = { main };
```

## 判斷流程圖

```
收到 Task/Step
    │
    ▼
有標準答案？─── Yes ──→ 寫 JS 腳本
    │ No
    ▼
可驗證？──────── Yes ──→ 寫 JS 腳本
    │ No
    ▼
重複性 > 1？──── Yes ──→ 寫 JS 腳本
    │ No
    ▼
用 AI 處理
```
