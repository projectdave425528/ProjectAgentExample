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

### 2.3 Backtesting

| ID | 需求 | 優先級 |
|----|------|--------|
| BT-01 | 支持歷史數據回測 | P0 |
| BT-02 | 分散式計算 — 可將 backtest 拆分到多個 worker 並行執行 | P0 |
| BT-03 | 支持多資產同時回測 | P1 |
| BT-04 | 參數優化（grid search / random search） | P1 |
| BT-05 | Walk-forward analysis（滾動窗口驗證） | P2 |
| BT-06 | Backtest 結果持久化，可重覆查看比較 | P0 |

### 2.4 Live Trading（自動交易）

| ID | 需求 | 優先級 |
|----|------|--------|
| LT-01 | 接收即時市場數據 → 觸發策略 → 發送訂單 | P0 |
| LT-02 | 風險管理（止損、止盈、最大持倉、每日最大虧損） | P0 |
| LT-03 | 訂單管理（市價/限價/止損單） | P0 |
| LT-04 | Paper Trading 模式（模擬交易，唔落真錢） | P0 |
| LT-05 | 支持多個帳戶同時運行 | P1 |

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

## 10. 開放問題（待決定）

1. 目標市場？（美股 / 港股 / 加密貨幣 / 外匯？）
2. 用邊個 Broker 做第一個 Adapter？
3. 前端技術偏好？（React / Vue / Svelte？）
4. 部署環境？（自己 server / cloud？）
5. 團隊規模？（影響技術複雜度取捨）
6. Budget 限制？（影響 infrastructure 選擇）
