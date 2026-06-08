# 自動交易系統 — 需求規格

> 建立日期：2026-06-04
> 狀態：Draft
> 來源：用戶對話需求整理

---

## 1. 系統概述

建立一個模組化、解耦嘅自動交易系統，支持：
- 多種策略（向量 + 非向量）
- Backtesting + Live Trading
- 分散式計算
- 多 Broker API 整合
- 用戶友好嘅 Web UI

---

## 2. 核心需求

### 2.1 用戶介面（UI）

| ID | 需求 | 優先級 |
|----|------|--------|
| UI-01 | Web-based UI，非 programmer 都可以操作 | P0 |
| UI-02 | 可視化 Dashboard：持倉、PnL、交易歷史、策略表現 | P0 |
| UI-03 | 策略管理介面：新增/編輯/啟停策略 | P0 |
| UI-04 | Backtest 結果可視化（equity curve、drawdown、trade list） | P0 |
| UI-05 | 即時市場數據顯示（K 線圖 + indicators） | P1 |
| UI-06 | 告警/通知系統（Telegram / Email / Webhook） | P1 |

### 2.2 策略系統

| ID | 需求 | 優先級 |
|----|------|--------|
| ST-01 | 支持向量類型策略（K 線 pattern matching via similarity search） | P0 |
| ST-02 | 支持非向量類型策略（傳統 rule-based：MACD crossover、RSI 等） | P0 |
| ST-03 | 策略以 Plugin 形式加入，統一 interface | P0 |
| ST-04 | 可通過 UI 新增/配置策略參數（唔需要改 code） | P0 |
| ST-05 | 策略可組合（例如：向量 filter + rule-based entry） | P1 |
| ST-06 | 策略版本控制（記錄每次修改） | P2 |
| ST-07 | 多單交易組合 — 一個策略可以同時開幾張單組成一個 position group（例如：分批入場、對沖組合、grid trading） | P0 |
| ST-08 | Position Group 管理 — 組合內嘅單可以獨立管理但共享一個整體 PnL 同風險配額 | P0 |
| ST-09 | 多策略並行 — 系統可以同時運行多個不同策略，每個策略各自有自己嘅 position groups，互不干擾但共享帳戶風險額度 | P0 |
| ST-10 | 多次交易支持 — 同一策略可以喺同一標的上開多次獨立交易（唔係加倉，係完全獨立嘅 trade lifecycle） | P0 |

### 2.3 Backtesting

| ID | 需求 | 優先級 |
|----|------|--------|
| BT-01 | 支持歷史數據回測 | P0 |
| BT-02 | 分散式計算 — 可將 backtest 拆分到並行執行 | P0 |
| BT-03 | 支持多資產同時回測 | P1 |
| BT-04 | 參數優化（grid search / random search） | P1 |
| BT-05 | Walk-forward analysis（滾動窗口驗證） | P2 |
| BT-06 | Backtest 結果持久化，可重覆查看比較 | P0 |
| BT-07 | 期望值計算（Expected Value）— 計算每個策略嘅期望值：`EV = (Win% × Avg Win) - (Loss% × Avg Loss)`，包含 profit factor、payoff ratio、Kelly criterion | P0 |
| BT-08 | 期望值報告 — 每次 backtest 結果自動計算並顯示 EV、最大連續虧損、風險回報比 | P0 |

### 2.4 Live Trading（自動交易）

| ID | 需求 | 優先級 |
|----|------|--------|
| LT-01 | 接收即時市場數據 → 觸發策略 → 發送訂單 | P0 |
| LT-02 | 風險管理（止損、止盈、最大持倉、每日最大虧損） | P0 |
| LT-03 | 訂單管理（市價/限價/止損單） | P0 |
| LT-04 | Paper Trading 模式（模擬交易，唔落真錢） | P0 |
| LT-05 | 支持多個帳戶同時運行 | P1 |
| LT-06 | 風險管理系統（獨立模組）— 包含：每日最大虧損限額、每策略最大持倉量、整體帳戶風險敞口上限、Drawdown 熔斷機制（達到 X% drawdown 自動暫停所有交易）、風險事件 log | P0 |
| LT-07 | 平倉系統 — 支持多種平倉策略：移動止損（trailing stop）、時間止損（持倉超過 N 天自動平）、條件止損（indicator 觸發平倉）、一鍵全平（緊急情況）、部分平倉（減倉） | P0 |
| LT-08 | 多單 Position Group 管理 — 策略產生嘅多張單歸入同一 group，group level 嘅風控（整體 stop loss、整體 take profit）、group 整體 PnL 追蹤 | P0 |

### 2.5 數據層 / API 整合

| ID | 需求 | 優先級 |
|----|------|--------|
| DA-01 | 輸入/輸出嘅交易數據格式標準化，為唔同 Broker API 準備 | P0 |
| DA-02 | Adapter 模式 — 每個 Broker 一個 Adapter，統一內部格式 | P0 |
| DA-03 | 支持多個 Data Provider（歷史數據 + 即時數據） | P0 |
| DA-04 | 數據緩存 + 本地存儲（減少 API call） | P1 |
| DA-05 | 標準化 Data Schema（OHLCV + metadata） | P0 |

### 2.6 架構要求

| ID | 需求 | 優先級 |
|----|------|--------|
| AR-01 | 各 Layer 解耦 — 用 Data Bus / Message Queue 傳輸資料 | P0 |
| AR-02 | 分散式計算支持（Backtest worker 可水平擴展） | P0 |
| AR-03 | 每個模組可獨立部署/升級/替換 | P0 |
| AR-04 | 事件驅動架構（Event-Driven） | P0 |
| AR-05 | 狀態持久化（系統重啟後可恢復） | P1 |
| AR-06 | 日誌 + 審計追蹤（所有交易決策可追溯） | P0 |

---

## 3. 系統架構（高層設計）

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web UI Layer                              │
│  Dashboard | Strategy Config | Backtest Results | Trade Monitor  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ REST API / WebSocket
┌───────────────────────────────▼─────────────────────────────────┐
│                      API Gateway Layer                           │
│  Authentication | Rate Limiting | Request Routing                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         ↓                      ↓                      ↓
┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│ Strategy Engine │  │ Backtest Engine  │  │ Live Trading Engine  │
│                 │  │                  │  │                      │
│ • Plugin Loader │  │ • Job Scheduler  │  │ • Signal Generator   │
│ • Vector Strat  │  │ • Worker Pool    │  │ • Order Manager      │
│ • Rule Strat    │  │ • Result Agg     │  │ • Risk Manager       │
│ • Signal Output │  │ • Distributed    │  │ • Position Tracker   │
└────────┬────────┘  └────────┬─────────┘  └──────────┬───────────┘
         │                    │                        │
         └────────────────────┼────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Message Bus / Event Bus                       │
│  (Redis Streams / RabbitMQ / Kafka)                             │
│                                                                 │
│  Events: MarketData | Signal | Order | Fill | Position | Alert  │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                  │
├──────────────────┬──────────────────┬───────────────────────────┤
│ Market Data Svc  │ Trade Data Svc   │ Vector Store              │
│                  │                  │                           │
│ • Data Providers │ • Order History  │ • Pattern Library         │
│ • OHLCV Cache    │ • Position State │ • Similarity Index        │
│ • Normalization  │ • PnL Calc       │ • Embedding Cache         │
└──────────────────┴──────────────────┴───────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                   Broker Adapter Layer                           │
├─────────────┬─────────────┬─────────────┬───────────────────────┤
│ Broker A    │ Broker B    │ Broker C    │ Paper Trading         │
│ Adapter     │ Adapter     │ Adapter     │ Simulator             │
└─────────────┴─────────────┴─────────────┴───────────────────────┘
```

---

## 4. 解耦設計 — Data Bus 通訊

### 4.1 Event Types

| Event | Producer | Consumer | Payload |
|-------|----------|----------|---------|
| `market.tick` | Data Provider | Strategy Engine, UI | `{symbol, ohlcv, timestamp}` |
| `market.bar` | Data Provider | Strategy Engine | `{symbol, timeframe, ohlcv}` |
| `signal.entry` | Strategy Engine | Live Trading Engine | `{strategy_id, symbol, direction, confidence, metadata}` |
| `signal.exit` | Strategy Engine | Live Trading Engine | `{strategy_id, symbol, reason}` |
| `order.new` | Live Trading Engine | Broker Adapter | `{order_id, symbol, side, qty, type, price}` |
| `order.fill` | Broker Adapter | Position Tracker, UI | `{order_id, fill_price, fill_qty, timestamp}` |
| `position.update` | Position Tracker | Risk Manager, UI | `{symbol, qty, avg_price, unrealized_pnl}` |
| `risk.alert` | Risk Manager | Live Trading Engine, UI | `{type, message, action}` |
| `backtest.job` | UI / Scheduler | Backtest Workers | `{job_id, strategy, params, data_range}` |
| `backtest.result` | Backtest Worker | Result Aggregator, UI | `{job_id, metrics, trades}` |

### 4.2 解耦原則

```
Rule 1: 模組之間唔直接 call function，只透過 Event Bus 通訊
Rule 2: 每個模組只知道自己嘅 Event Schema，唔知其他模組嘅實現
Rule 3: 新增 Broker = 只加一個 Adapter，其他模組唔需要改
Rule 4: 新增策略 = 只加一個 Strategy Plugin，其他模組唔需要改
Rule 5: 每個模組可以獨立 scale（例如加多幾個 Backtest Worker）
```

---

## 5. 策略 Plugin Interface

### 5.1 統一 Interface（向量 + 非向量都用同一個）

```typescript
interface Strategy {
  id: string;
  name: string;
  type: "vector" | "rule-based" | "hybrid";
  params: Record<string, any>;  // UI 可配置嘅參數
  
  // 初始化（載入 pattern library / indicator 設定）
  initialize(config: StrategyConfig): void;
  
  // 接收市場數據 → 輸出 signal
  onBar(bar: OHLCV): Signal | null;
  
  // 策略參數 schema（UI 用嚟生成表單）
  getParamSchema(): ParamSchema[];
}
```

### 5.2 向量策略 Plugin 例子

```typescript
class VectorPatternStrategy implements Strategy {
  type = "vector";
  params = {
    window_size: 20,
    threshold: 0.68,
    top_k: 10,
    pattern_library: "head_and_shoulder_v1"
  };
  
  getParamSchema() {
    return [
      { name: "window_size", type: "number", min: 5, max: 100, default: 20 },
      { name: "threshold", type: "number", min: 0.3, max: 0.95, default: 0.68 },
      { name: "top_k", type: "number", min: 1, max: 50, default: 10 },
      { name: "pattern_library", type: "select", options: [...] },
    ];
  }
}
```

### 5.3 Rule-based 策略 Plugin 例子

```typescript
class MACDCrossoverStrategy implements Strategy {
  type = "rule-based";
  params = {
    fast_period: 12,
    slow_period: 26,
    signal_period: 9,
  };
}
```

---

## 6. 分散式 Backtest 設計

```
┌─────────────────────────────────────────────┐
│ UI: 用戶提交 Backtest Job                    │
│ - Strategy: MACD Crossover                  │
│ - Params: fast=8-16, slow=20-30             │
│ - Data: SPY 2020-2024                       │
│ - Parallelism: 按參數組合拆分               │
└─────────────────────┬───────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│ Job Scheduler                               │
│ - 拆分成 N 個 sub-jobs                      │
│ - 例如 fast=8,slow=20 / fast=8,slow=21 ... │
│ - 發送到 Message Queue                      │
└─────────────────────┬───────────────────────┘
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Worker 1     │ │ Worker 2     │ │ Worker N     │
│ fast=8,s=20  │ │ fast=8,s=21  │ │ fast=16,s=30 │
│ → Run        │ │ → Run        │ │ → Run        │
│ → Result     │ │ → Result     │ │ → Result     │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       └────────────────┼────────────────┘
                        ↓
┌─────────────────────────────────────────────┐
│ Result Aggregator                           │
│ - 收集所有 sub-job results                  │
│ - 排名（by Sharpe / by PnL / by Drawdown） │
│ - 寫入 DB + 通知 UI                        │
└─────────────────────────────────────────────┘
```

---

## 7. 數據格式標準（跨 Broker 通用）

### 7.1 Market Data Schema

```json
{
  "symbol": "AAPL",
  "timeframe": "1d",
  "timestamp": "2024-01-15T00:00:00Z",
  "open": 185.50,
  "high": 187.20,
  "low": 184.80,
  "close": 186.90,
  "volume": 52340000
}
```

### 7.2 Order Schema（統一內部格式）

```json
{
  "order_id": "ORD-2024-001",
  "strategy_id": "macd-cross-v1",
  "symbol": "AAPL",
  "side": "BUY",
  "quantity": 100,
  "type": "LIMIT",
  "price": 186.50,
  "stop_loss": 184.00,
  "take_profit": 192.00,
  "timestamp": "2024-01-15T09:30:00Z",
  "metadata": {
    "signal_confidence": 0.73,
    "pattern_match": "double_bottom"
  }
}
```

### 7.3 Broker Adapter 職責

```
Internal Format ←→ Broker Adapter ←→ Broker-specific API Format

每個 Adapter 負責：
1. 將內部 Order Schema 轉換成 Broker API 格式
2. 將 Broker 回覆轉換成內部 Fill/Position 格式
3. 處理 Broker-specific 嘅 authentication
4. 處理 reconnection / error retry
```

---

## 8. 技術選型建議（待確認）

| 組件 | 候選 | 備註 |
|------|------|------|
| Frontend | React / Next.js | Dashboard + 策略配置 |
| Backend API | Node.js / Python FastAPI | API Gateway |
| Strategy Engine | Python | 數學計算 + indicator library |
| Message Bus | Redis Streams / RabbitMQ | 解耦通訊 |
| Database | PostgreSQL + TimescaleDB | 交易記錄 + 時序數據 |
| Vector Store | Qdrant / Milvus / FAISS | 向量策略用 |
| Backtest Workers | Celery (Python) / Bull (Node) | 分散式 job queue |
| Deployment | Docker + Kubernetes | 水平擴展 |

---

## 9. 非功能需求

| 需求 | 指標 |
|------|------|
| 延遲 | Signal → Order < 100ms（live trading） |
| 可用性 | 99.9%（交易時段內） |
| 數據完整性 | 所有交易決策可追溯 |
| 安全 | API key 加密存儲、RBAC 權限控制 |
| 可擴展 | 加新 Broker / 新策略唔需要改核心 |

---

## 10. 風控計算需求

### 10.1 破產風險（Risk of Ruin）< 1%

| ID | 需求 | 優先級 |
|----|------|--------|
| RK-01 | 系統必須計算當前策略嘅破產風險 | P0 |
| RK-02 | 破產風險必須低於 1%，否則唔允許開倉 | P0 |
| RK-03 | 即時更新 RoR（每次交易完結後重新計算） | P0 |

**計算公式：**

簡化版：
```
RoR = ((1 - Edge) / (1 + Edge)) ^ Capital_Units
```
- `Edge` = (Win% × Avg_Win) - (Loss% × Avg_Loss)
- `Capital_Units` = 帳戶總資金 ÷ 每次風險金額

Ralph Vince 公式（更精確）：
```
RoR = ((1 - W + W×R) / R) ^ (A / B)
```
- `W` = 勝率
- `R` = 盈虧比（Avg Win / Avg Loss）
- `A` = 帳戶單位數（總資金 ÷ 單次風險金額）
- `B` = 連續虧損可承受次數

**控制變數：**
- 降低每次 risk per trade（建議 1-2%）
- 提高 Edge（勝率 × 盈虧比）
- 資金越大，RoR 越低

### 10.2 策略最大回撤（Max Drawdown）

| ID | 需求 | 優先級 |
|----|------|--------|
| RK-04 | 系統必須實時計算策略嘅 Max Drawdown | P0 |
| RK-05 | 用作風控參考同策略評估指標 | P0 |
| RK-06 | 支持 Monte Carlo 模擬預估未來 MDD | P1 |

**計算方法：**
```
Max_Drawdown = (Peak - Trough) / Peak × 100%
```

步驟：
1. 遍歷 equity curve，記錄歷史最高點（Peak）
2. 每個時間點計算當前值相對 Peak 嘅跌幅
3. 取所有跌幅中嘅最大值 = Max Drawdown

Monte Carlo 模擬（預估未來 MDD）：
1. 將歷史交易結果隨機重新排列 N 次（建議 10,000 次）
2. 每次計算 MDD
3. 取 95th percentile 作為預期最壞情況

### 10.3 支持線與阻力線計算

| ID | 需求 | 優先級 |
|----|------|--------|
| RK-07 | 系統需要自動識別支持線（Support）同阻力線（Resistance） | P0 |
| RK-08 | 作為入場/出場參考，可配合策略 Signal 使用 | P0 |
| RK-09 | 支持多種計算方法，可由 UI 選擇 | P1 |

**方法 A：Pivot Points（經典）**
```
PP = (High + Low + Close) / 3
R1 = 2 × PP - Low;  R2 = PP + (High - Low)
S1 = 2 × PP - High; S2 = PP - (High - Low)
```

**方法 B：歷史高低點聚集**
- 搵價格多次觸及但未突破嘅價位區域
- 可用 Volume Profile 輔助確認

**方法 C：移動平均線（動態支持/阻力）**
- MA50 / MA200 經常充當動態支持或阻力

**方法 D：Fibonacci Retracement**
- 關鍵回撤位：23.6%, 38.2%, 50%, 61.8%, 78.6%

---

## 11. 計算架構設計（Local / Cloud Hybrid）

### 11.1 需求

| ID | 需求 | 優先級 |
|----|------|--------|
| CMP-01 | 系統必須支援 Local 電腦同 Cloud 兩種計算模式 | P0 |
| CMP-02 | 向量數據（Vector Data）嘅計算同儲存需兼容兩種環境 | P0 |
| CMP-03 | 可根據資源需求動態切換計算模式 | P1 |
| CMP-04 | Local ↔ Cloud 數據同步機制 | P0 |

### 11.2 Local 計算模式
- **適用場景**：低延遲策略、隱私敏感數據、離線回測
- **計算內容**：
  - 實時 tick data 處理
  - 向量 embedding 推論（inference）
  - 支持/阻力線即時計算
  - Risk of Ruin 即時驗證
- **儲存**：本地 vector database（ChromaDB / LanceDB / FAISS）
- **硬件建議**：GPU 加速向量計算（CUDA / Metal）

### 11.3 Cloud 計算模式
- **適用場景**：大規模回測、模型訓練、歷史數據分析
- **計算內容**：
  - Monte Carlo 模擬（大量 iteration）
  - 向量 embedding 批量生成
  - 模型訓練同超參數搜尋
  - 多策略並行回測
- **服務選項**：AWS / GCP / Azure（GPU instance）
- **儲存**：雲端 vector database（Pinecone / Weaviate / Qdrant）

### 11.4 數據同步策略
```
Local ←→ Cloud 同步機制：
- Local 生成嘅 embedding → 批量上傳到 Cloud 備份
- Cloud 訓練完嘅模型 → 下載到 Local 做 inference
- 增量同步，避免全量傳輸
```

---

## 12. AI 整合與訓練設計

### 12.1 需求

| ID | 需求 | 優先級 |
|----|------|--------|
| AI-01 | 系統架構必須保留使用 AI 模型同訓練 AI 模型嘅可能性 | P0 |
| AI-02 | 唔強制依賴 AI，但所有 data pipeline 要 AI-ready | P0 |
| AI-03 | 支持模型版本控制同 A/B Testing | P1 |
| AI-04 | 模型 drift detection + 自動 retrain 觸發 | P2 |

### 12.2 數據格式（AI-Ready）
```json
{
  "timestamp": "datetime",
  "features": [0.1, 0.5, ...],
  "labels": {
    "direction": 1,
    "magnitude": 0.023
  },
  "metadata": {
    "symbol": "AAPL",
    "timeframe": "1d"
  }
}
```

### 12.3 可接入嘅 AI 方向

| 方向 | 用途 | 模型類型 |
|------|------|---------|
| 趨勢預測 | 預測未來 N 根 K 線方向 | LSTM / Transformer |
| 支持阻力識別 | 自動搵 S/R zone | CNN / Clustering |
| 風險評估 | 動態調整 position size | Reinforcement Learning |
| 異常檢測 | 識別市場異常狀態 | Autoencoder / Isolation Forest |
| 策略優化 | 超參數自動調優 | Bayesian Optimization / GA |

### 12.4 訓練 Pipeline
```
Raw Data → Feature Engineering → Vector Embedding → Storage
                                                      ↓
                                         ┌─── Local Inference（快速）
                                         │
                                         └─── Cloud Training（大規模）
                                                      ↓
                                              Model → Local Deploy
```

### 12.5 模型管理
- 版本控制：每個 trained model 有版本號 + 訓練日期
- A/B Testing：新模型同舊模型並行跑，比較績效
- Rollback：績效下降自動切返舊模型
- 監控：模型 drift detection，定期 retrain

---

## 13. AI Agent 開發架構

> 用 Kiro Harness Engineering 的 Sub Agent（Planner-Generator-Evaluator）去**開發**本交易系統。

### 13.1 開發模式

```
唔係：AI Agent 幫你交易
而係：AI Agent 幫你寫交易程式
```

### 13.2 Agent 角色定義

| Agent | 角色 | 輸入 | 輸出 | 工具權限 |
|-------|------|------|------|---------|
| **Planner** | 分析需求、設計架構、拆分任務 | 用戶需求描述 | Spec 文件（requirements + design + tasks） | 只讀 |
| **Generator** | 根據設計寫代碼 | tasks.md | 源代碼、測試、配置 | 全部（讀寫 + 執行） |
| **Evaluator** | 審查代碼、跑測試、提改善 | Generator 嘅代碼 | 審查報告（PASS/FAIL） | 只讀 + 執行測試 |

### 13.3 開發流程

```
Step 1: 用戶描述需求
        ↓
Step 2: Planner 分析 → requirements.md + design.md + tasks.md
        ↓
Step 3: 用戶審核 Spec
        ↓
Step 4: Generator 按 tasks.md 逐步寫代碼
        ↓
Step 5: Evaluator 審查 → PASS → 下一個 Task / FAIL → 返回 Generator
        ↓
Step 6: 全部完成 → 最終整合測試 → 交付
```

### 13.4 Orchestrator 架構

```
┌─────────────────────────────────────────────────────────────┐
│                     用戶（你）                                │
│              描述需求 / 審核代碼 / 測試結果                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Orchestrator（主 Agent / Kiro）                  │
│              接收需求 → 調度 Sub Agent → 匯總結果             │
└──────┬──────────────┬──────────────┬────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Planner  │   │Generator │   │Evaluator │
│ 分析需求 │   │ 寫代碼   │   │ 審查代碼 │
│ 設計架構 │   │ 寫測試   │   │ 跑測試   │
│ 拆分任務 │   │ 寫文件   │   │ 提改善   │
└──────────┘   └──────────┘   └──────────┘
```

---

## 14. DataFlow 流程圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                        外部數據源                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │交易所 API│  │新聞 API  │  │社交媒體  │  │鏈上數據  │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
└───────┼──────────────┼──────────────┼──────────────┼────────────────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    數據獲取層（Data Ingestion）                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ REST Client  │  │ WebSocket    │  │ Scheduler    │             │
│  │ (歷史數據)   │  │ (實時數據)   │  │ (定時拉取)   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    數據處理層（Data Processing）                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 數據清洗     │  │ 指標計算     │  │ 特徵工程     │             │
│  │ (去重/補缺)  │  │ (RSI/MACD)   │  │ (ML 特徵)    │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    數據存儲層（Data Storage）                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 時序數據庫   │  │ 交易記錄     │  │ 配置存儲     │             │
│  │ (行情/K線)   │  │ (訂單/持倉)  │  │ (策略參數)   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    策略引擎層（Strategy Engine）                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 信號生成     │  │ 倉位計算     │  │ 風險評估     │             │
│  │ (買/賣/持有) │  │ (Kelly/固定) │  │ (VaR/回撤)   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    執行層（Execution）                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 訂單管理     │  │ 風控攔截     │  │ 滑點控制     │             │
│  │ (市價/限價)  │  │ (止損/限額)  │  │ (拆單/延遲)  │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    監控層（Monitoring）                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ 績效追蹤     │  │ 告警通知     │  │ 日誌記錄     │             │
│  │ (PnL/Sharpe) │  │ (Telegram)   │  │ (操作審計)   │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

**DataFlow 摘要：**
```
外部數據 → 獲取 → 處理 → 存儲 → 策略 → 執行 → 監控
                                    ↑                │
                                    └── 反饋循環 ────┘
```

---

## 15. 編寫風格規範

### 15.1 核心原則
- **Clean Code**：代碼即文件，命名清晰，函數短小
- **Design Pattern**：適當使用設計模式，唔好過度設計
- **解耦**：模組之間低耦合、高內聚
- **高效率**：喺唔影響人類理解的前提下，追求執行效率
- **可讀性優先**：效率同可讀性衝突時，優先可讀性

### 15.2 函數規則
- 每個函數只做一件事（Single Responsibility）
- 函數長度 < 30 行
- 參數 ≤ 3 個，超過用 dataclass/dict 包裝
- Loop 嵌套最多 3 層，超過必須拆分
- 避免深層 if-else，用 early return

### 15.3 設計模式使用指引

| 場景 | 建議模式 |
|------|---------|
| 多種策略切換 | Strategy Pattern |
| 交易所 API 統一接口 | Adapter Pattern |
| 事件通知（信號、風控） | Observer Pattern |
| 複雜物件建立（訂單） | Builder Pattern |
| 全局配置/連接池 | Singleton Pattern |
| 數據處理流水線 | Pipeline / Chain of Responsibility |

### 15.4 代碼結構（每個模組）

```
module/
├── __init__.py          ← 公開 API
├── models.py            ← 數據模型（dataclass）
├── interfaces.py        ← 抽象接口（Protocol/ABC）
├── service.py           ← 業務邏輯
├── repository.py        ← 數據存取
├── exceptions.py        ← 自定義異常
└── tests/
    └── test_service.py  ← 測試
```

### 15.5 禁止事項
- ❌ 全局可變狀態（global mutable state）
- ❌ 函數內超過 3 層 loop 嵌套
- ❌ 超過 100 行的函數
- ❌ 超過 500 行的文件
- ❌ Magic number（用常數代替）
- ❌ 註釋解釋「做咩」，只註釋「點解」

---

## 16. 自動測試規範

### 16.1 測試分層

| 層次 | 覆蓋範圍 | 數量 | 執行速度 |
|------|---------|:---:|---------|
| Unit Test | 單一函數/類 | 多 | < 1 秒/個 |
| Integration Test | 模組之間互動 | 中 | < 10 秒/個 |
| E2E Test | 完整交易流程 | 少 | < 60 秒/個 |

### 16.2 測試框架

| 工具 | 用途 |
|------|------|
| `pytest` | 測試框架 |
| `pytest-asyncio` | 異步測試 |
| `pytest-cov` | 覆蓋率報告 |
| `pytest-mock` / `unittest.mock` | Mock 外部依賴 |
| `hypothesis` | Property-based testing |
| `freezegun` | 時間凍結 |

### 16.3 覆蓋率要求

| 模組 | 最低覆蓋率 |
|------|:---:|
| 策略引擎 | 90% |
| 風控系統 | 95% |
| 訂單管理 | 90% |
| 數據處理 | 80% |
| UI / 通知 | 60% |

### 16.4 必須測試的場景

| 場景 | 測試內容 |
|------|---------|
| 策略信號 | 正確生成買/賣/持有信號 |
| 風控觸發 | 止損/止盈/最大回撤正確觸發 |
| 訂單執行 | 市價單/限價單正確下單 |
| 異常處理 | API 超時/斷線/餘額不足 |
| 數據邊界 | 空數據/缺失數據/極端值 |
| 並發安全 | 多個信號同時觸發唔會重複下單 |
| 回測一致性 | 回測結果同實盤邏輯一致 |

### 16.5 測試命名規範
```python
# 格式：test_[被測函數]_[場景]_[預期結果]
def test_calculate_rsi_with_14_periods_returns_valid_range():
    ...

def test_place_order_when_insufficient_balance_raises_error():
    ...
```

### 16.6 Mock 規則

| 外部依賴 | Mock 方式 |
|---------|---------|
| 交易所 API | Mock response |
| 數據庫 | In-memory SQLite |
| 時間 | `freezegun` |
| 網絡 | `responses` / `aioresponses` |

### 16.7 禁止事項
- ❌ 測試依賴外部網絡
- ❌ 測試之間有順序依賴
- ❌ 測試修改全局狀態
- ❌ 跳過失敗的測試（需註明原因）
- ❌ 冇 assertion 的測試

---

## 17. Kiro Harness Engineering 配置

### 17.1 Steering（開發規範）

| 文件 | 用途 |
|------|------|
| `auto-trade-requirements.md` | 交易程式的功能需求 |
| `tech-stack.md` | 技術棧（Python、框架、庫） |
| `code-standards.md` | 代碼規範（命名、結構、測試） |
| `trading-domain.md` | 交易領域知識（術語、概念） |

### 17.2 Hooks（開發自動化）

| Hook | 觸發 | 動作 |
|------|------|------|
| `lint-on-save` | fileEdited `*.py` | 自動 lint |
| `test-after-task` | postTaskExecution | 自動跑測試 |
| `review-on-complete` | agentStop | 觸發 Evaluator 審查 |

### 17.3 Specs（開發計劃）

| Spec | 內容 |
|------|------|
| `data-module` | 數據獲取模組開發 |
| `strategy-module` | 策略引擎模組開發 |
| `execution-module` | 交易執行模組開發 |
| `backtest-module` | 回測框架開發 |
| `risk-module` | 風控模組開發 |
| `ui-module` | 監控界面開發 |

### 17.4 Kiro 整合方式

**方案 A：單一 Workspace + Spec（推薦起步）**
```
用 Kiro Spec workflow：
  1. 建立 Spec → requirements + design + tasks
  2. 逐個 Task 執行（Kiro 自動寫代碼）
  3. Hook 自動跑測試
  4. 用戶審核結果
```

**方案 B：Multi-Root Workspace（進階）**
```
planner/     ← 獨立 Steering（只分析）
generator/   ← 獨立 Steering（只寫 code）
evaluator/   ← 獨立 Steering（只審查）
auto-trade/  ← 實際程式碼
```

---

## 18. 開發路線圖

```
Phase 1：基礎設施（Planner 主導）
  - 確認需求 + 設計架構
  - 建立項目結構
  - 設定開發環境

Phase 2：核心模組（Generator 主導）
  - 數據獲取模組
  - 策略引擎
  - 回測框架

Phase 3：交易執行（Generator + Evaluator）
  - 交易所 API 連接
  - 訂單管理
  - 風控系統

Phase 4：優化 + UI（全部 Agent）
  - 策略優化
  - 監控面板
  - 通知系統
  - 文件生成
```

---

## 19. 開放問題（待決定）

1. 目標市場？（美股 / 港股 / 加密貨幣 / 外匯？）
2. 用邊個 Broker 做第一個 Adapter？
3. 前端技術偏好？（React / Vue / Svelte？）
4. 部署環境？（自己 server / cloud？）
5. 團隊規模？（影響技術複雜度取捨）
6. Budget 限制？（影響 infrastructure 選擇）
7. AI 模型訓練用邊個 Cloud Provider？
8. Local 機器 GPU 規格？（影響 inference 能力）
9. 交易頻率？（高頻 / 日內 / 波段 / 長線）
10. 風控要求？（保守 / 中等 / 激進）
