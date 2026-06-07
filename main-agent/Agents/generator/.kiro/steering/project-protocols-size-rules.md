---
inclusion: manual
description: Generator 任務大小管理規則（L3 - 手動載入）
---

# 任務大小管理規則（防止 Cancel / Timeout）
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

## 通用規則

1. **任務大小自我評估** — 收到 Assignment 後，先評估任務量：
   - 需要產出 > 5 個文件 → 優先完成核心文件，確保 outbox reply 寫入
   - 需要跑 > 50 個 tests → 分批跑（每批 ≤ 25 個），每批完成後記錄結果
   - 需要 review > 3 個文件 → 按重要性排序，逐個 review
2. **優先保證 outbox 寫入** — 寧願簡化內容，都要確保 outbox reply 成功寫入
3. **分階段完成** — 如果任務太大，主動拆分：
   - 階段 1：核心功能（最重要）
   - 階段 2：補充內容 / 次要部分
   - 每個階段完成後立即寫入 checkpoint
4. **Context 使用率監控** — 如果感覺 context 接近上限，立即：
   - 停止當前步驟
   - 寫入已完成嘅結果到 outbox（即使唔完整）
   - 喺 reply 標記「部分完成」，列出未做嘅項目
5. **異常必須上報** — 遇到 cancel/timeout/blocked/partial/failed，必須寫 outbox reply 上報

## 異常上報機制

### 觸發條件
| 情況 | 觸發時機 |
|------|---------|
| Context 接近上限 | output 已經好長 / compaction 提示 |
| 任務太大做唔完 | 自我評估後超出單次能力 |
| 無法解決嘅 Error | 重試 3 次仍然失敗 |
| Blocked | 缺少資訊 / 技術決策 / 依賴未就緒 |
| 部分完成 | 核心已做，補充未做 |

### Status 值
| status | 意思 | Main Agent 動作 |
|--------|------|----------------|
| `completed` | 正常完成 | 繼續流程 |
| `partial` | 部分完成 | 評估是否足夠 |
| `blocked` | 無法繼續 | 讀原因 → 解決或問用戶 |
| `failed` | 重試後仍然失敗 | 重試/REPLAN/問用戶 |
| `timeout-risk` | 預判會超時 | 評估拆細方案 |

### Reply 必須包含（status ≠ completed 時）
```markdown
## 異常上報
### 狀態
{status 值}
### 已完成項目
- [列出已完成嘅工作]
### 未完成項目
- [列出未做嘅工作 + 預估工作量]
### 原因
{點解唔係 completed}
### 建議下一步
{拆細？補 context？換方案？}
```

### 行為優先級（遇到異常時）
```
1. 寫 checkpoint ← 最高
2. 寫 outbox reply（上報）
3. 更新 memory
4. 繼續做未完成嘅工作 ← 最低
```

### 嚴禁行為
- ❌ 唔寫 reply 就停止
- ❌ 明知做唔完仍然繼續直到被 cancel
- ❌ 標 `completed` 但實際未做完
