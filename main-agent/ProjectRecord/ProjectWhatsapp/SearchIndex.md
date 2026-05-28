# ProjectRecord 搜尋索引

> 所有 Task 嘅輕量索引，Agent 搵記錄時先讀呢個文件，唔使逐個 inbox/outbox 文件讀取。
> 每次寫入 ProjectRecord 後必須同步更新本索引。（由 Main Agent 統一維護）

---

| Task ID | Agent | Type | Status | 關鍵字 | 日期 | 文件路徑 |
|---------|-------|------|--------|--------|------|---------|
| 001 | main-agent | assignment | dispatched | Specs 全部重寫 | 2026-05-28 | inbox/planner/assignment-001.md |
| 001 | planner | assignment-reply | completed | Specs 重寫完成 | 2026-05-28 | outbox/planner/assignment-001-reply-completed.md |
| 002 | main-agent | assignment | dispatched | Task1 項目初始化 | 2026-05-28 | inbox/generator/assignment-002.md |
| 002 | generator | assignment-reply | completed | Task1 Data Models 完成 | 2026-05-28 | outbox/generator/assignment-002-reply-completed.md |
| 003 | main-agent | assignment | dispatched | Task1 評估請求 | 2026-05-28 | inbox/evaluator/assignment-003.md |
| 003 | evaluator | verdict | PASS (88) | Task1 通過評估 | 2026-05-28 | outbox/evaluator/assignment-003-reply-verdict.md |
| 004 | main-agent | assignment | dispatched | Task2 Regex Patterns | 2026-05-28 | inbox/generator/assignment-004.md |
| 004 | generator | assignment-reply | completed | Task2 Regex Patterns 完成 | 2026-05-28 | outbox/generator/assignment-004-reply-completed.md |
| 005 | main-agent | assignment | dispatched | Task2 評估請求 | 2026-05-28 | inbox/evaluator/assignment-005.md |
| 005 | evaluator | verdict | PASS (85) | Task2 Regex Patterns 通過 | 2026-05-28 | outbox/evaluator/assignment-005-reply-verdict.md |

| 006 | main-agent | assignment | dispatched | Task3 Text Parser 主邏輯 | 2026-05-28 | inbox/generator/assignment-006.md |
| 006 | generator | assignment-reply | completed | Task3 Text Parser 完成 | 2026-05-28 | outbox/generator/assignment-006-reply-completed.md |

| 007 | main-agent | assignment | dispatched | Task3 評估請求 | 2026-05-28 | inbox/evaluator/assignment-007.md |
| 007 | evaluator | verdict | PASS (90) | Task3 Text Parser 通過 | 2026-05-28 | outbox/evaluator/assignment-007-reply-verdict.md |

| 008 | main-agent | assignment | dispatched | Task4 Image Analyzer OCR | 2026-05-28 | inbox/generator/assignment-008.md |
| 008 | generator | assignment-reply | completed | Task4 Analyzer 完成 | 2026-05-28 | outbox/generator/assignment-008-reply-completed.md |