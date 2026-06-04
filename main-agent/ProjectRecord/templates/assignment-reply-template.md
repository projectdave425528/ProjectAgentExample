# Assignment Reply: {id}

- **From**: {agent-name}
- **To**: main-agent
- **Timestamp**: {ISO timestamp}
- **AssignmentStatus**: completed | blocked | verdict-pass | verdict-fail | verdict-replan | escalation
- **TaskRef**: Task {task-number}: {task-title}
- **TaskID**: {spec-name}/Task-{task-number}
- **TaskStatus**: in_progress → completed | blocked

## 驗證標準
- [x] {已完成嘅 outcome}
- [ ] {未完成嘅 outcome}

## 結果
{Agent 嘅回覆內容}

## 備註
{任何額外資訊}

## Memory 已更新
✅ / ❌

## Usage 估算
- **Context 使用率**: {百分比}%（例如 45%）
- **估算 Token 數**: {input_tokens} input / {output_tokens} output
- **接近限額警告**: ⚠️ / ✅（如果 Context ≥ 80% 或感覺即將耗盡，標記 ⚠️）

---

## Status 對照表

| Status | 用途 | 使用者 | 文件名後綴 |
|--------|------|--------|-----------|
| completed | 任務完成 | Planner / Generator | `-reply-completed.md` |
| blocked | 無法完成，需要幫助 | Generator | `-reply-blocked.md` |
| verdict-pass | 代碼通過（≥80分） | Evaluator | `-reply-verdict.md` |
| verdict-fail | 代碼需修改（60-79分） | Evaluator | `-reply-verdict.md` |
| verdict-replan | 方案需重設計（<60分） | Evaluator | `-reply-verdict.md` |
| escalation | 需要用戶決定 | Planner | `-reply-escalation.md` |

> 📖 **需要範例？** 5 個完整實例（completed / blocked / verdict-pass / verdict-fail / escalation）
> 見 `examples/reply-examples.md`（唔識格式時先讀，平時唔使載入）。
> 💡 Evaluator 評分 5 項權重：功能 30% + 品質 25% + 安全 20% + 可測試性 15% + 維護 10%。
