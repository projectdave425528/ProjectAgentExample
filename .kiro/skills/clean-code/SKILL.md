---
name: clean-code
description: Clean Code principles for writing and evaluating high-quality code. Use when generating code (naming, functions, error handling, design) or reviewing/evaluating code quality (scoring, violations, feedback). Based on Robert C. Martin's Clean Code philosophy.
keywords: clean code, code quality, naming, functions, refactoring, SOLID, code review, code smells, testability, DRY, single responsibility, abstraction level
---

# Clean Code Principles

> Based on Robert C. Martin's *Clean Code: A Handbook of Agile Software Craftsmanship*.
> Use this skill when generating or evaluating code to ensure quality, readability, and maintainability.

---

## Part A: Writing Clean Code (Generator)

### 1. Naming

| Principle | Rule | Bad → Good |
|-----------|------|------------|
| Reveal Intent | Name should tell WHY it exists | `d` → `elapsedTimeInDays` |
| Avoid Disinformation | Don't use misleading names | `accountList` (not a List) → `accounts` |
| Meaningful Distinction | No noise words | `a1, a2` → `source, destination` |
| Pronounceable | Must be speakable | `genymdhms` → `generationTimestamp` |
| Searchable | Long enough to grep | `e` → `WORK_DAYS_PER_WEEK` |
| Class = Noun | | `Customer`, `Account`, `Parser` |
| Method = Verb | | `postPayment`, `deletePage`, `save` |

### 2. Functions

| Principle | Guideline |
|-----------|-----------|
| Small | < 30 lines ideal |
| Do One Thing | Single responsibility per function |
| One Abstraction Level | All statements at same conceptual height |
| Step-down Rule | Read top-to-bottom, each function leads to next level |
| Few Arguments | 0 best, 1 ok, 2 acceptable, 3+ avoid (use object) |
| No Side Effects | No hidden mutations |
| Command-Query Separation | Either DO something OR ANSWER something, never both |
| DRY | Eliminate duplication |

#### One Abstraction Level — Example

```typescript
// ❌ BAD: Mixed abstraction levels
function generateReport(user: User) {
  const data = fetchReportData(user);       // HIGH level
  let html = '<html><body>';                // LOW level
  html += '<h1>' + data.title + '</h1>';    // LOW level
  sendEmail(user.email, html);              // HIGH level
}

// ✅ GOOD: Same abstraction level
function generateReport(user: User) {
  const data = fetchReportData(user);
  const html = renderReportHtml(data);
  sendEmail(user.email, html);
}
```

### 3. Comments

#### Acceptable
- Legal (copyright)
- Informative (regex explanation)
- Intent explanation (WHY this approach)
- Warning of consequences
- TODO (with ticket reference)

#### Avoid
- Redundant (code already says it)
- Misleading
- Journal comments (use git log)
- Noise (`/** The name */`)
- Commented-out code (use version control)

**Rule: Code should be self-explanatory. Comments compensate for failure to express in code.**

### 4. Error Handling

| Principle | Guideline |
|-----------|-----------|
| Exceptions over return codes | Use exceptions for error flow |
| Write try-catch first | Define scope up front |
| Provide context | Exception message must explain what happened and where |
| Don't return null | Use empty collection, Optional, or Special Case pattern |
| Don't pass null | Disallow null as argument |

### 5. Objects vs Data Structures

| | Objects | Data Structures |
|--|---------|----------------|
| Data | Hidden | Exposed |
| Behavior | Exposed (methods) | None |

#### Law of Demeter
- A method should only call methods on: itself, its parameters, objects it creates, its fields
- ❌ `obj.getA().getB().getC()`
- ✅ Wrap in a single method with clear intent

### 6. Classes & Design

| Principle | Guideline |
|-----------|-----------|
| SRP | One reason to change per class |
| Cohesion | Methods should use multiple instance variables |
| OCP | Open for extension, closed for modification |
| DIP | Depend on abstractions, not concretions |
| Small | Measured by responsibilities, not lines |

### 7. Simple Design Rules (Kent Beck)

Priority order:
1. **Passes all tests** (most important)
2. **No duplication**
3. **Expresses intent** (readable, well-named)
4. **Minimizes classes and methods**

### 8. Refactoring Mindset

- No one writes clean code first time — write dirty, then clean
- Refactoring is continuous, not one-time
- Run tests after every small change
- **First make it work, then make it clean**
- Extract → Rename → Separate responsibilities → Remove duplication

### 9. Unit Tests

#### TDD Three Laws
1. Don't write production code until you have a failing test
2. Don't write more test than sufficient to fail
3. Don't write more production code than sufficient to pass

#### F.I.R.S.T.
| Letter | Meaning | Guideline |
|--------|---------|-----------|
| F | Fast | Tests run quickly |
| I | Independent | No inter-test dependencies |
| R | Repeatable | Works in any environment |
| S | Self-validating | Pass or fail, no manual inspection |
| T | Timely | Written before or alongside production code |

---

## Part B: Evaluating Clean Code (Evaluator)

### Evaluation Dimensions & Weights

| Dimension | Weight | Key Checks |
|-----------|--------|------------|
| Naming | 15% | Intent-revealing, no disinformation, convention match |
| Functions | 25% | Size < 30 lines, SRP, same abstraction level, ≤ 3 args |
| Error Handling | 15% | Exceptions used, context provided, no null returns |
| Comments & Readability | 10% | Self-documenting, no noise, consistent formatting |
| Classes & Design | 20% | SRP, cohesion, OCP, DIP, Law of Demeter |
| Testability | 15% | DI ready, pure functions, interface separation |

### Grade Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Exemplary clean code |
| B | 75-89 | Good, minor improvements possible |
| C | 60-74 | Acceptable, notable issues to address |
| D | 40-59 | Below standard, significant refactoring needed |
| F | < 40 | FAIL — does not meet minimum quality |

### Auto-FAIL Conditions

- Function > 100 lines
- Class > 500 lines with no clear SRP
- No error handling on ANY external call
- Duplicated logic in 3+ places
- Zero tests for business logic

### Scoring Modifiers

| Condition | Modifier |
|-----------|----------|
| Follows all 4 Simple Design Rules | +5 |
| Consistent naming throughout | +3 |
| Mixed abstraction levels in functions | -5 per occurrence |
| God function (> 50 lines, multiple concerns) | -10 |
| Dead code present | -3 per instance |

### Feedback Format

When citing Clean Code violations:

```markdown
**Clean Code Violation:**
- [{severity}] {file}:{line} — {principle violated}
  - Issue: {what's wrong}
  - Fix: {specific suggestion}
  - Reference: Clean Code Ch.{N} — {chapter name}
```

#### Example

```markdown
- [HIGH] user-service.ts:45 — Mixed Abstraction Levels
  - Issue: `createUser()` mixes HTTP response formatting with business logic
  - Fix: Extract response formatting to controller, keep service pure
  - Reference: Clean Code Ch.3 — Functions

- [MEDIUM] utils.ts:12 — Non-revealing Name
  - Issue: Variable `d` does not explain its purpose
  - Fix: Rename to `daysSinceLastLogin`
  - Reference: Clean Code Ch.2 — Meaningful Names
```

---

## Part C: Code Smells Quick Reference

### Critical (Immediate fix)
- Functions > 30 lines
- Too many parameters (> 3)
- Duplicated code
- Mixed abstraction levels
- Deep nesting (> 3 levels)

### High (Should fix)
- Dead code
- Flag arguments (boolean params)
- Output parameters
- Unclear naming
- Comments compensating for bad names
- No error handling on external calls

### Medium (Fix when touching)
- Vertical separation (declaration far from usage)
- Inconsistent conventions
- Unnecessary complexity for single-use logic
- Commented-out code

---

## SOLID Principles Summary

| Principle | Full Name | Meaning |
|-----------|-----------|---------|
| **S** | Single Responsibility | One class/function = one reason to change |
| **O** | Open-Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subtypes must be substitutable for base types |
| **I** | Interface Segregation | Don't force clients to depend on unused interfaces |
| **D** | Dependency Inversion | Depend on abstractions, not concretions |

---

*This skill should be activated when writing new code or evaluating existing code for quality.*
