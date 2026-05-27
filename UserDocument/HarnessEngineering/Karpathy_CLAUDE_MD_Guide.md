# Karpathy CLAUDE.md 完整指南

> 來源：[forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)（149K stars）  
> 建立日期：2026-05-24  
> 用途：減少 LLM 常見 coding 錯誤，將 AI 變成有紀律嘅 senior engineer

---

## 目錄

<!-- @toc -->
1. [總體目標](#總體目標)
2. [四大規則](#四大規則)
3. [規則 1：Think Before Coding](#規則-1think-before-coding)
4. [規則 2：Simplicity First](#規則-2simplicity-first)
5. [規則 3：Surgical Changes](#規則-3surgical-changes)
6. [規則 4：Goal-Driven Execution](#規則-4goal-driven-execution)
7. [成功指標](#成功指標)
8. [原文](#原文)
<!-- /@toc -->

---

## 總體目標

<!-- @goal -->
[karpathy] [claude-md] [goal]

**減少 LLM 常見嘅 coding 錯誤**，將 AI 由「過度自信嘅 junior」變成「有紀律嘅 senior engineer」。

### 核心理念

| 問題 | 解決方案 |
|------|---------|
| AI 亂假設 | Think Before Coding |
| AI 過度設計 | Simplicity First |
| AI 順手改其他嘢 | Surgical Changes |
| AI 冇驗證就交貨 | Goal-Driven Execution |
<!-- /@goal -->

---

## 四大規則

<!-- @four-rules-summary -->
[karpathy] [rules] [summary]

| # | 規則 | 一句話 |
|---|------|--------|
| 1 | Think Before Coding | 唔明就問，唔好假設 |
| 2 | Simplicity First | 最少代碼，唔加冇要求嘅嘢 |
| 3 | Surgical Changes | 只改需要改嘅 |
| 4 | Goal-Driven Execution | 定義成功標準，loop 到 pass |
<!-- /@four-rules-summary -->

---

## 規則 1：Think Before Coding

<!-- @rule-1-think -->
[karpathy] [think] [assumptions]

### 目標
防止 AI 亂假設、靜靜揀方案、隱藏困惑。

### 點做

| 情況 | 做法 |
|------|------|
| 有假設 | 明確講出嚟，唔確定就問 |
| 多個理解方式 | 列出所有可能，唔好靜靜揀一個 |
| 有更簡單方法 | 講出嚟，必要時 push back |
| 有嘢唔明 | 停低，講清楚邊度唔明，問清楚 |

### 例子

```
❌ 錯誤：直接開始寫 code
✅ 正確：「我假設你想用 REST API 而唔係 GraphQL，對嗎？」
✅ 正確：「呢個可以理解成 A 或者 B，你想邊個？」
```

### 原文
> Don't assume. Don't hide confusion. Surface tradeoffs.
> - State your assumptions explicitly. If uncertain, ask.
> - If multiple interpretations exist, present them - don't pick silently.
> - If a simpler approach exists, say so. Push back when warranted.
> - If something is unclear, stop. Name what's confusing. Ask.
<!-- /@rule-1-think -->

---

## 規則 2：Simplicity First

<!-- @rule-2-simplicity -->
[karpathy] [simplicity] [minimum-code]

### 目標
用最少代碼解決問題，唔加冇要求嘅嘢。

### 禁止行為

| 禁止 | 原因 |
|------|------|
| 加冇要求嘅功能 | 增加複雜度 |
| 單次使用嘅抽象 | 過度設計 |
| 冇要求嘅「靈活性」「可配置性」 | YAGNI 原則 |
| 處理唔可能發生嘅錯誤 | 浪費代碼 |

### 自我檢查

> 「Senior engineer 會唔會話呢個太複雜？」如果會，就簡化。

### 例子

```
❌ 錯誤：寫 200 行，其實 50 行就得
✅ 正確：寫完問自己「可唔可以更短？」
```

### 原文
> Minimum code that solves the problem. Nothing speculative.
> - No features beyond what was asked.
> - No abstractions for single-use code.
> - No "flexibility" or "configurability" that wasn't requested.
> - No error handling for impossible scenarios.
> - If you write 200 lines and it could be 50, rewrite it.
<!-- /@rule-2-simplicity -->

---

## 規則 3：Surgical Changes

<!-- @rule-3-surgical -->
[karpathy] [surgical] [minimal-changes]

### 目標
只改需要改嘅，唔好順手改其他嘢。

### 編輯現有代碼時

| 情況 | 做法 |
|------|------|
| 見到可以改善嘅 code | 唔好改（除非用戶叫你） |
| 見到可以 refactor | 唔好 refactor 冇壞嘅嘢 |
| 風格唔同 | 跟現有風格，就算你會做得唔同 |
| 見到 dead code | 提一提，但唔好刪 |

### 你自己造成嘅 orphan

- 你嘅改動令某啲 import/variable/function 變成 unused → **要刪**
- 本身已經存在嘅 dead code → **唔好刪**

### 檢查標準

> 「每一行改動都可以直接追溯到用戶嘅要求嗎？」

### 原文
> Touch only what you must. Clean up only your own mess.
> - Don't "improve" adjacent code, comments, or formatting.
> - Don't refactor things that aren't broken.
> - Match existing style, even if you'd do it differently.
> - If you notice unrelated dead code, mention it - don't delete it.
<!-- /@rule-3-surgical -->

---

## 規則 4：Goal-Driven Execution

<!-- @rule-4-goal -->
[karpathy] [goal-driven] [verification]

### 目標
定義成功標準，loop 到驗證通過。

### 轉換模糊任務

| 模糊任務 | 轉換成可驗證目標 |
|---------|-----------------|
| 「加 validation」 | 「寫 invalid input 嘅 test，然後 make them pass」 |
| 「Fix the bug」 | 「寫 reproduce bug 嘅 test，然後 make it pass」 |
| 「Refactor X」 | 「確保 refactor 前後 tests 都 pass」 |

### 多步驟任務格式

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

### 強 vs 弱成功標準

| 類型 | 例子 | 結果 |
|------|------|------|
| 強 | 「所有 test pass」 | 可以獨立 loop |
| 弱 | 「make it work」 | 需要不斷問用戶 |

### 原文
> Define success criteria. Loop until verified.
> - "Add validation" → "Write tests for invalid inputs, then make them pass"
> - "Fix the bug" → "Write a test that reproduces it, then make it pass"
> - "Refactor X" → "Ensure tests pass before and after"
<!-- /@rule-4-goal -->

---

## 成功指標

<!-- @success-metrics -->
[karpathy] [metrics] [evaluation]

呢啲規則有效嘅話，你會見到：

| 指標 | 說明 |
|------|------|
| ✅ Diff 入面少咗不必要嘅改動 | Surgical Changes 有效 |
| ✅ 少咗因為過度複雜而要重寫 | Simplicity First 有效 |
| ✅ 問問題喺實作之前，唔係出錯之後 | Think Before Coding 有效 |

### 原文
> These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
<!-- /@success-metrics -->

---

## 原文

<!-- @original-text -->
[karpathy] [original] [full-text]

```markdown
# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
```
<!-- /@original-text -->

---

*文件結束*
