---
inclusion: manual
description: Context 管理規則（Generator 本地副本）
---

# Context 管理規則（防止 Cancel / Timeout）
> 🔒 **本 section 只可由用戶修改或刪除，Agent 唔可以自行更改。**
> 📌 本文件係 Generator workspace 嘅本地副本，內容應與 Main Agent 嘅 `.kiro/steering/shared/context-management.md` 一致。

## 通用規則（Planner / Generator / Evaluator 共用）

1. **任務大小自我評估** — 收到 Assignment 後，先評估任務量：
   - 需要分析 / 產出 > 5 個文件 → 按重要性排序，逐個處理，優先完成核心
   - 需要跑 > 50 個 tests → 分批跑（每批 ≤ 25 個），每批完成後記錄結果
   - 需要 review > 3 個文件 → 按重要性排序，逐個 review
2. **優先保證 outbox 寫入** — 寧願簡化內容，都要確保 outbox reply 成功寫入。被 cancel 但冇寫 outbox = 任務完全浪費
3. **分階段完成** — 如果任務太大，主動拆分為多個階段，每個階段完成後立即寫入 checkpoint：
   - 階段 1：核心功能 / 最重要嘅部分（最優先）
   - 階段 2：補充內容 / 次要部分
4. **Context 使用率監控** — 如果感覺 context 接近上限（output 已經好長），立即：
   - 停止當前步驟
   - 寫入已完成嘅結果到 outbox（即使唔完整）
   - 喺 reply 標記「部分完成」，列出未做嘅項目
