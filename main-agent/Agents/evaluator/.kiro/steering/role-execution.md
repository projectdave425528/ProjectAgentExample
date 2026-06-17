---
inclusion: manual
description: Evaluator 任務執行流程（L3 - 評估前必讀）
---

# Evaluator 任務執行流程

## 啟動流程
1. 讀 `./ProjectRecord/active-project.md` → 確認當前 Project
2. 讀 `./ProjectRecord/{active-project}/inbox/evaluator/assignment-{id}.md` → 取得評估任務
3. 讀 `domain-knowledge-evaluation-criteria.md` → 了解評分標準
4. 讀 `../../.kiro/skills/clean-code/SKILL.md`（Part B）→ Clean Code 評估標準
   → 完成後：寫 Decision Log（記錄評估策略選擇）
5. 讀 `../../.kiro/skills/design-patterns/SKILL.md`（Part C）→ Design Patterns 評估標準
   → 完成後：寫 Decision Log
6. 讀取 Generator 嘅 output → 開始評估
   → 每個評估維度完成後：寫 Decision Log（記錄點解俾呢個分、考慮過邊啲標準）
7. 得出 Verdict → 寫 Decision Log（記錄 PASS/FAIL/REPLAN 嘅完整推理同權衡）

> 🔒 **Decision Log 規則**：每個 Step 完成後必須寫一份 Decision Log，見 `project-protocols-decision-log.md`。唔寫 = Step 未完成。

## 自動測試驗證規則（必須遵守，零例外）

### 測試執行流程
1. **確認 test 文件存在** — 冇 test → 直接 FAIL（分數上限 50）
2. **分析 test 覆蓋度** — 對照 Planner 嘅 Test Criteria 逐項檢查
3. **確認 Integration Test 存在**（如果 Task 涉及多模組互動）：
   - 有 → 正常評分
   - 冇但應該有 → 扣分（分數上限 70）
4. **嘗試執行 test**（如果環境允許）：
   - Unit test 全部 PASS → 正常評分
   - Integration test 全部 PASS → 加分
   - 有 FAIL → 記錄失敗嘅 test，扣分
   - 無法執行（缺少依賴）→ 靜態分析 test 品質
5. **評估 test 品質** — test 本身要有意義

### Integration Test 驗證標準
| # | 檢查項 | 判斷標準 |
|---|--------|----------|
| I1 | 存在 | 涉及多模組互動嘅 Task 必須有 |
| I2 | 真實互動 | 至少有一層真實互動（唔係全 mock） |
| I3 | 數據流完整 | 覆蓋 input → processing → output |
| I4 | Setup/Teardown | 有正確嘅 test data 準備同清理 |
| I5 | 環境隔離 | 唔影響 production data |

### Test 執行結果對 Verdict 嘅影響
| 情況 | 影響 |
|------|------|
| 全部 test PASS | 正常評分 |
| 有 test FAIL | 直接 FAIL verdict |
| 冇 test 文件 | 直接 FAIL（分數上限 50） |
| Test 有但品質差 | T1-T4 扣分 |
| 環境唔支援執行 | 靜態分析，verdict 註明 |

## FAIL Output 標記規則

> Verdict 為 FAIL 時，必須重命名 output folder。

- 原路徑：`./ProjectRecord/{active-project}/output/assignment-{id}/`
- FAIL 後：`./ProjectRecord/{active-project}/output/assignment-{id}-FAILED/`
- 第 2 次 FAIL：`assignment-{id}-FAILED-2/`
- 第 3 次 FAIL：`assignment-{id}-FAILED-3/`
- 重命名失敗 → 唔影響主流程，喺 verdict 備註標記
