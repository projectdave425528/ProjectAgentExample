# CodeGraph-Driven Automated Testing System — Feasibility & Design Plan

> **Project**: ProjectWhatsapp  
> **Author**: Planner Agent  
> **Date**: 2026-06-05  
> **Status**: Research / Planning Document  
> **Assignment**: 027

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Feasibility Analysis](#2-feasibility-analysis)
3. [Design Proposal](#3-design-proposal)
4. [Architecture](#4-architecture)
5. [Implementation Recommendations](#5-implementation-recommendations)
6. [Limitations & Risks](#6-limitations--risks)
7. [Comparison with Alternatives](#7-comparison-with-alternatives)
8. [Task Breakdown](#8-task-breakdown)

---

## 1. Executive Summary

This document evaluates whether the existing CodeGraph (code knowledge graph — 139 files, 2145 nodes, 3813 edges) can be leveraged to build an automated testing system for ProjectWhatsapp. The conclusion is **conditionally feasible**: CodeGraph provides structural intelligence (call graphs, impact paths, symbol relationships) that traditional coverage tools lack, making it useful for test gap discovery, regression risk scoring, and guided test generation. However, it cannot replace runtime coverage analysis and requires integration with pytest-cov for a complete solution.

**Recommended approach**: A hybrid system that uses CodeGraph for static structural analysis (what SHOULD be tested) and pytest-cov for dynamic runtime analysis (what IS tested), with a reconciliation layer that identifies gaps and prioritizes test generation.

---

## 2. Feasibility Analysis

### 2.1 What CodeGraph Data Provides

| CodeGraph Capability | Testing Use Case | Feasibility |
|---------------------|-----------------|-------------|
| `codegraph_callers` / `codegraph_callees` | Map function dependency chains → identify integration test boundaries | ✅ High |
| `codegraph_impact` | Determine blast radius of a change → prioritize regression tests | ✅ High |
| `codegraph_search` (symbol search) | Find all implementations of an interface → ensure all variants are tested | ✅ High |
| `codegraph_files` (file tree) | Identify modules without corresponding test files | ✅ High |
| `codegraph_explore` (structure) | Understand module boundaries → define test scope | ✅ Medium |
| Node/Edge relationships | Build function-level dependency graph → detect untested paths | ⚠️ Medium |

### 2.2 What CodeGraph Cannot Do

| Limitation | Impact |
|-----------|--------|
| No runtime execution data | Cannot determine actual code coverage at branch level |
| No data flow analysis | Cannot infer what input values exercise which paths |
| No type-level constraint analysis | Cannot auto-generate boundary value test cases |
| Static structure only | Cannot detect dead code that is structurally reachable but never called at runtime |
| No test outcome history | Cannot correlate which tests catch which regressions |

### 2.3 Feasibility Verdict

| Capability | CodeGraph Alone | CodeGraph + pytest-cov |
|-----------|-----------------|----------------------|
| Find untested modules | ✅ Yes | ✅ Yes (enhanced) |
| Find untested functions | ⚠️ Partial (structural only) | ✅ Yes |
| Find untested branches | ❌ No | ✅ Yes |
| Regression risk scoring | ✅ Yes (via impact graph) | ✅ Yes (enhanced with history) |
| Auto-generate test skeletons | ⚠️ Partial (signatures only) | ⚠️ Partial |
| Auto-generate test data | ❌ No | ❌ No (needs LLM) |
| Prioritize what to test next | ✅ Yes | ✅ Yes |

---

## 3. Design Proposal

### 3.1 Core Concept: Graph-Aware Test Intelligence

The system operates in three modes:

**Mode A — Gap Discovery** (What's not tested?)
```
CodeGraph nodes → filter functions/classes → cross-reference with existing test files
→ produce "untested symbols" report with risk score (based on caller count)
```

**Mode B — Impact-Driven Regression** (What should I re-test after a change?)
```
Changed file → codegraph_impact → affected nodes → map to existing tests
→ produce "minimum test set" for the change
```

**Mode C — Test Skeleton Generation** (Help me write new tests)
```
Target function → codegraph_callers + codegraph_callees → understand context
→ generate pytest skeleton with:
  - Correct imports
  - Mock setup for dependencies (callees)
  - Test method names based on function signature
  - TODO markers for test data
```

### 3.2 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT SOURCES                              │
├──────────────────┬──────────────────┬───────────────────────────┤
│   CodeGraph API  │  pytest-cov XML  │  Git diff (optional)      │
│   (structure)    │  (runtime cov)   │  (change context)         │
└────────┬─────────┴────────┬─────────┴──────────┬────────────────┘
         │                  │                    │
         ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RECONCILIATION ENGINE                           │
│                                                                   │
│  1. Build "expected coverage" from CodeGraph (all public symbols)│
│  2. Build "actual coverage" from pytest-cov                      │
│  3. Diff → untested symbols with structural context              │
│  4. Score by impact (callers count × depth)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT ARTIFACTS                             │
├──────────────────┬──────────────────┬───────────────────────────┤
│  Coverage Gap    │  Regression Risk │  Test Skeleton             │
│  Report (.md)    │  Report (.md)    │  Files (.py)              │
└──────────────────┴──────────────────┴───────────────────────────┘
```

---

## 4. Architecture

### 4.1 System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                     CodeGraph Auto-Testing System                      │
│                                                                        │
│  ┌────────────┐    ┌─────────────────┐    ┌───────────────────────┐  │
│  │ CodeGraph  │    │  Coverage        │    │  Test Generator       │  │
│  │ Adapter    │    │  Reconciler      │    │  (Skeleton)           │  │
│  │            │    │                  │    │                       │  │
│  │ - query()  │───▶│ - gap_analysis() │───▶│ - gen_skeleton()      │  │
│  │ - impact() │    │ - risk_score()   │    │ - gen_imports()       │  │
│  │ - graph()  │    │ - prioritize()   │    │ - gen_mocks()         │  │
│  └────────────┘    └─────────────────┘    └───────────────────────┘  │
│        ▲                   ▲                         │                 │
│        │                   │                         ▼                 │
│  ┌─────┴──────┐    ┌──────┴────────┐    ┌───────────────────────┐   │
│  │ CodeGraph  │    │  pytest-cov   │    │  Output Formatter     │   │
│  │ Tools API  │    │  XML Parser   │    │  (MD / pytest files)  │   │
│  └────────────┘    └───────────────┘    └───────────────────────┘   │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘

External Dependencies:
  - CodeGraph index (already exists: 139 files, 2145 nodes, 3813 edges)
  - pytest-cov (coverage.xml output)
  - Git (optional, for change-based analysis)
```

### 4.2 Component Responsibilities

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| CodeGraph Adapter | Wraps CodeGraph tool calls into a queryable interface | Symbol names, file paths | Structured graph data (nodes, edges, callers, callees) |
| Coverage Reconciler | Compares structural expectations vs actual coverage | Graph data + coverage XML | Gap list with risk scores |
| Test Generator | Produces pytest skeleton files for uncovered symbols | Symbol metadata + dependency graph | `.py` test files with TODO markers |
| Output Formatter | Produces human-readable reports | Analysis results | Markdown reports |

### 4.3 Data Model

```
TestableSymbol:
  - name: str
  - file: str
  - type: "function" | "class" | "method"
  - callers_count: int
  - callees: list[str]
  - has_test: bool
  - coverage_pct: float | None
  - risk_score: float  # computed: callers_count × centrality

CoverageGap:
  - symbol: TestableSymbol
  - reason: "no_test_file" | "no_test_function" | "low_coverage"
  - suggested_test_path: str
  - priority: "P0" | "P1" | "P2"

ImpactReport:
  - changed_files: list[str]
  - affected_symbols: list[TestableSymbol]
  - suggested_tests: list[str]
  - risk_level: "high" | "medium" | "low"
```

---

## 5. Implementation Recommendations

### 5.1 Recommended Toolchain

| Tool | Purpose | Why |
|------|---------|-----|
| Python 3.9+ | Implementation language | Matches project stack |
| pytest + pytest-cov | Test runner + coverage | Already in project |
| CodeGraph API (existing) | Structural analysis | Already indexed (2145 nodes) |
| Jinja2 | Test skeleton templates | Clean template generation |
| Click | CLI interface | Already in project dependencies |
| coverage.py XML output | Coverage data source | Standard, parseable |

### 5.2 Phased Implementation

**Phase 1 — Gap Discovery (MVP)**
- Parse CodeGraph to list all public functions/classes
- Cross-reference with `tests/` directory (file-level matching)
- Produce markdown report of untested modules
- Estimated effort: 2-3 days

**Phase 2 — Risk Scoring**
- Use `codegraph_callers` to count callers for each symbol
- Compute centrality-based risk score
- Sort gaps by risk priority
- Estimated effort: 1-2 days

**Phase 3 — Impact Analysis**
- Accept a file/function as input
- Use `codegraph_impact` to trace blast radius
- Map affected nodes to existing test files
- Output "minimum regression test set"
- Estimated effort: 2-3 days

**Phase 4 — Test Skeleton Generation**
- For uncovered symbols, generate pytest file skeletons
- Use callees info to auto-generate mock setup
- Include correct import paths from CodeGraph
- Estimated effort: 3-4 days

**Phase 5 — Integration with CI (Optional)**
- Run gap analysis on every PR
- Compare before/after coverage
- Block PRs that reduce structural coverage
- Estimated effort: 2-3 days

### 5.3 Example Usage (Conceptual)

```bash
# Gap analysis
python -m cg_testing gap-report --output reports/coverage-gaps.md

# Impact analysis for a specific change
python -m cg_testing impact --changed src/parser/text_parser.py

# Generate test skeleton for uncovered function
python -m cg_testing gen-test --symbol "amount_extractor.extract_amount"

# Full report
python -m cg_testing full-report --cov-xml coverage.xml --output reports/
```

---

## 6. Limitations & Risks

### 6.1 Technical Limitations

| Limitation | Severity | Mitigation |
|-----------|----------|-----------|
| CodeGraph is static — cannot detect runtime-only paths | Medium | Combine with pytest-cov for runtime data |
| No branch-level analysis from graph alone | Medium | Use coverage.xml for branch data |
| Cannot generate meaningful test data | High | Requires human input or LLM assistance |
| CodeGraph index may become stale | Low | Re-index on file changes (already supported) |
| Dynamic dispatch / monkey-patching invisible to graph | Low | ProjectWhatsapp uses minimal dynamic patterns |
| Graph doesn't capture configuration-dependent paths | Medium | Document known config variants manually |

### 6.2 Project-Specific Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| WhatsApp format variants not captured in graph | Medium | Test gaps for edge cases | Maintain format variant registry separately |
| OCR/Vision API mocking complexity | High | Generated skeletons may be incomplete | Provide mock templates for external services |
| Cantonese NLP patterns need domain knowledge for test data | High | Auto-generated tests won't cover linguistic edge cases | Human-curated test data library |
| Over-reliance on structural coverage may miss semantic bugs | Medium | False sense of completeness | Complement with property-based testing |

### 6.3 Effort vs Value Assessment

| Phase | Effort | Value | ROI |
|-------|--------|-------|-----|
| Phase 1 (Gap Discovery) | Low (2-3 days) | High — immediate visibility | ⭐⭐⭐ |
| Phase 2 (Risk Scoring) | Low (1-2 days) | Medium — prioritization | ⭐⭐⭐ |
| Phase 3 (Impact Analysis) | Medium (2-3 days) | High — regression prevention | ⭐⭐⭐ |
| Phase 4 (Skeleton Gen) | Medium (3-4 days) | Medium — saves boilerplate time | ⭐⭐ |
| Phase 5 (CI Integration) | Medium (2-3 days) | High — automated guardrail | ⭐⭐ |

---

## 7. Comparison with Alternatives

### 7.1 CodeGraph Approach vs pytest-cov (Traditional Coverage)

| Dimension | CodeGraph Approach | pytest-cov |
|-----------|-------------------|-----------|
| **What it measures** | Structural reachability + dependency importance | Actual line/branch execution |
| **Granularity** | Function/class level | Line/branch level |
| **Requires running tests** | No | Yes |
| **Finds "important but untested" code** | ✅ Yes (via caller count) | ❌ No (all lines equal) |
| **Finds dead code** | ❌ No | ✅ Yes (0% coverage) |
| **Change impact analysis** | ✅ Yes (graph traversal) | ❌ No |
| **Setup cost** | Low (index already exists) | Low (already in project) |
| **False positives** | May flag internal helpers as "untested" | May show 100% on trivial code |

**Verdict**: Complementary. CodeGraph tells you WHAT to test (priority). pytest-cov tells you HOW WELL it's tested (depth).

### 7.2 CodeGraph Approach vs Data-Driven Testing

| Dimension | CodeGraph Approach | Data-Driven Testing |
|-----------|-------------------|-------------------|
| **Focus** | Test coverage completeness | Test data completeness |
| **Automation level** | Structural (skeleton generation) | Data (parameterized tests) |
| **Domain knowledge needed** | Low (graph is objective) | High (need domain-specific test data) |
| **Best for** | Finding gaps, regression risk | Thorough validation of known scenarios |
| **Weakness** | Cannot generate test data | Cannot discover missing test targets |

**Verdict**: Different concerns. CodeGraph approach decides WHERE to test; Data-Driven decides WITH WHAT to test. Ideal system uses both.

### 7.3 CodeGraph Approach vs State-Aware Testing

| Dimension | CodeGraph Approach | State-Aware Testing |
|-----------|-------------------|-------------------|
| **Model** | Dependency graph (static) | State machine (dynamic) |
| **Discovers** | Untested functions | Untested state transitions |
| **Best for** | Unit/integration test gaps | End-to-end flow coverage |
| **Complexity** | Low-Medium | High |
| **ProjectWhatsapp fit** | ✅ Good (pipeline = clear dependencies) | ⚠️ Overkill (simple linear pipeline) |

**Verdict**: For ProjectWhatsapp's pipeline architecture, CodeGraph approach gives better ROI than state-aware testing. State-aware testing would be more valuable for a system with complex user interactions.

### 7.4 Recommended Combination

```
Layer 1: CodeGraph (structural intelligence) — WHERE to test
Layer 2: pytest-cov (runtime coverage) — HOW WELL it's tested  
Layer 3: Data-Driven (parameterized) — WITH WHAT to test
Layer 4: State-Aware (optional) — FLOWS to test (if complexity grows)
```

---

## 8. Task Breakdown

If this plan is approved for implementation:

| # | Task | Priority | Depends On | Estimated Effort |
|---|------|----------|-----------|-----------------|
| 1 | Create CodeGraph Adapter module (wraps API calls) | P0 | — | 1 day |
| 2 | Implement file-level gap detection (module ↔ test file mapping) | P0 | Task 1 | 1 day |
| 3 | Implement function-level gap detection (symbol ↔ test function) | P0 | Task 1 | 1.5 days |
| 4 | Implement risk scoring (callers count × centrality) | P1 | Task 3 | 1 day |
| 5 | Implement impact analysis (changed file → affected tests) | P1 | Task 1 | 2 days |
| 6 | Implement test skeleton generator (Jinja2 templates) | P1 | Task 3 | 2.5 days |
| 7 | Build CLI interface (Click commands) | P1 | Tasks 2-6 | 1 day |
| 8 | Integrate pytest-cov XML parsing | P2 | Task 2 | 1 day |
| 9 | Build reconciliation engine (graph gaps + runtime coverage) | P2 | Tasks 3, 8 | 1.5 days |
| 10 | CI integration (GitHub Actions / pre-commit hook) | P2 | Task 7 | 1.5 days |

**Total estimated effort**: 14-15 days (for full system)  
**MVP (Phase 1+2)**: 4-5 days

---

## Appendix A: ProjectWhatsapp-Specific Application

Given the pipeline architecture:

```
TextParser → ImageAnalyzer → RecordBuilder → ExcelExporter
```

CodeGraph impact analysis would be particularly valuable for:

1. **TextParser changes** → Impact on RecordBuilder (most callers)
2. **Pydantic model changes** → Impact on ALL downstream modules
3. **AmountExtractor changes** → Impact on PaymentDetector + RecordBuilder
4. **Pattern regex changes** → Impact on TextParser + all dependents

The linear pipeline means CodeGraph traversal is straightforward and the impact analysis results will be highly actionable.

---

## Appendix B: Comparison Summary Matrix

| Criterion | CodeGraph | pytest-cov | Data-Driven | State-Aware |
|-----------|-----------|-----------|-------------|-------------|
| Find untested code | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐ |
| Prioritize testing effort | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ |
| Regression risk detection | ⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐ |
| Test data generation | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| End-to-end flow coverage | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Setup effort | ⭐⭐⭐ (low) | ⭐⭐⭐ (low) | ⭐⭐ (medium) | ⭐ (high) |
| ProjectWhatsapp fit | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |

---

*End of document.*
