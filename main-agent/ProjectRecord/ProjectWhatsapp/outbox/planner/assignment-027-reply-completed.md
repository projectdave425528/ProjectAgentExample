# Assignment Reply: 027

- **From**: planner
- **To**: main-agent
- **Timestamp**: 2026-06-05T13:45:00+08:00
- **AssignmentStatus**: completed
- **TaskRef**: N/A (research/planning task)
- **TaskID**: ProjectWhatsapp/Assignment-027
- **TaskStatus**: completed

## 驗證標準
- [x] 可行性分析：CodeGraph 數據能做到咩程度嘅自動化測試
- [x] 設計方案：利用 callers/callees + impact graph 自動生成 coverage 報告
- [x] 實作建議：工具鏈 + 架構圖
- [x] 限制同風險：方法嘅 limitations
- [x] 同其他方法嘅對比：vs pytest-cov、vs data-driven testing

## 結果

已產出完整規劃文件：`./ProjectRecord/ProjectWhatsapp/UserDocument/codegraph-auto-testing-plan.md`

### 核心結論

**可行性：Conditionally Feasible（有條件可行）**

CodeGraph 提供嘅結構性資訊（2145 nodes、3813 edges）可以有效用於：
1. **Gap Discovery** — 搵出未測試嘅 modules/functions（透過 file tree + symbol cross-reference）
2. **Impact Analysis** — 用 callers/callees graph 計算變更影響範圍，精準揀 regression test set
3. **Risk Scoring** — 按 caller count × centrality 排優先級
4. **Test Skeleton Generation** — 自動生成 pytest 骨架（正確 import + mock setup）

但 CodeGraph **唔能夠**取代 pytest-cov（冇 runtime branch coverage），亦唔能自動生成有意義嘅 test data。

### 建議方案

Hybrid 系統：
- Layer 1: CodeGraph → WHERE to test（結構性缺口）
- Layer 2: pytest-cov → HOW WELL（runtime coverage depth）
- Layer 3: Data-Driven → WITH WHAT（domain-specific test data）

### 實作估算
- **MVP（Gap Discovery + Risk Scoring）**: 4-5 days
- **Full System（10 tasks）**: 14-15 days
- 5 個 Phase，可逐步交付

### 風險摘要
- CodeGraph 係 static analysis，無法偵測 runtime-only paths
- 自動生成嘅 test skeleton 需要人手補充 test data（尤其廣東話金額、OCR 場景）
- 對 ProjectWhatsapp 嘅 pipeline 架構特別適合（線性依賴，impact 分析結果直接可用）

## 備註
- 呢份係純研究/規劃文件，唔涉及 code implementation
- 如用戶想進入實作階段，建議從 Phase 1（Gap Discovery MVP）開始
- 文件用英文撰寫（按 assignment 要求）

## Memory 已更新
❌（研究任務，唔需要更新 memory）

## Usage 估算
- **Context 使用率**: ~35%
- **估算 Token 數**: 8000 input / 4500 output
- **接近限額警告**: ✅
