---
inclusion: manual
description: Main Agent 任務大小管理規則（L3 - 手動載入）
---

# 任務大小管理規則（防止 Cancel / Timeout）
> 🔒 **本文件只可由用戶修改或刪除，Agent 唔可以自行更改。**

1. **任務大小自我評估** — 調度大任務時按重要性排序，逐步處理
   - 需要派 > 5 個 Assignment → 按重要性排序
   - 需要寫 > 50 行記錄 → 分批寫入
   - 需要處理 > 3 個 Agent reply → 逐個處理
2. **優先保證寫入** — 寧願簡化內容，確保 inbox/outbox + conversation-log 寫入
3. **分階段完成** — 任務太大就拆階段，每階段完成即更新 checkpoint
4. **Context 使用率監控** — 接近上限時停止、寫低結果、標記「部分完成」

## 異常上報機制（Sub Agent 應遵守）

> Main Agent 收到 Sub Agent 嘅 reply 時，根據 status 做決定。

### Sub Agent 異常 Status 值
| status | 意思 | Main Agent 動作 |
|--------|------|----------------|
| `completed` | 正常完成 | 繼續流程 |
| `partial` | 部分完成（核心已做，補充未做） | 評估是否足夠 / 開新 Assignment 補充 |
| `blocked` | 無法繼續（缺資訊/決策） | 讀原因 → 自己解決或問用戶 |
| `failed` | 重試後仍然失敗 | 讀原因 → 重試/REPLAN/問用戶 |
| `timeout-risk` | 預判會超時，提前上報 | 評估拆細方案 |

### Sub Agent Reply 必須包含（status ≠ completed 時）
```markdown
## 異常上報

### 狀態
{status 值}

### 已完成項目
- [列出已完成嘅工作]

### 未完成項目
- [列出未做嘅工作 + 預估工作量]

### 原因
{點解唔係 completed — 具體描述}

### 建議下一步
{Sub Agent 自己嘅建議：拆細？補 context？換方案？}
```

### Sub Agent 行為優先級（遇到異常時）
```
1. 寫 checkpoint（記錄進度）          ← 最高優先
2. 寫 outbox reply（上報狀態）        ← 第二優先
3. 更新 memory（記錄教訓）            ← 第三優先
4. 繼續做未完成嘅工作                 ← 最低優先
```

### 嚴禁行為
- ❌ 唔寫 reply 就停止（Main Agent 無法知道發生咩事）
- ❌ 明知做唔完仍然繼續直到被 cancel（浪費 token + 冇 output）
- ❌ 喺 reply 入面標 `completed` 但實際未做完
