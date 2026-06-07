---
name: codegraph-usage
description: Guide for using CodeGraph MCP tools to explore, search, and analyze code efficiently. Use this skill whenever you need to understand code structure, find symbols, trace callers/callees, analyze impact of changes, or navigate a codebase. Trigger on tasks involving code exploration, architecture understanding, refactoring planning, bug investigation, or when you need to find where something is defined or used. Also trigger when the user mentions codegraph, code graph, symbol search, call graph, impact analysis, or code navigation.
keywords: codegraph, code graph, symbol, callers, callees, impact, explore, code navigation, architecture, call graph, codebase
---

# CodeGraph MCP Usage Guide

CodeGraph provides a pre-indexed semantic knowledge graph of the codebase. Use it instead of grep/find/read for code exploration - it is faster and uses fewer tokens.

## Project Integration Rule

**After receiving CodeGraph results, automatically save relevant outputs to the active project:**

1. Read `./ProjectRecord/active-project.md` to determine the current project name.
2. Save CodeGraph exploration results to `./ProjectRecord/{active-project}/.codegraph/` as a local cache.
3. If the `.codegraph/` directory does not exist in the active project, create it.
4. Store query results in `./ProjectRecord/{active-project}/.codegraph/explore-cache.md` (append mode).

**Format for cached results:**

```markdown
## [{timestamp}] Query: {query}
- Files found: {count}
- Symbols: {list of key symbols}
- Summary: {one-line summary of findings}
```

This ensures each project maintains its own CodeGraph knowledge base for future reference.

---

## Available Tools

### Primary Tool: codegraph_explore

**Use FIRST for almost any code question.** Returns verbatim source of relevant symbols grouped by file.

- Query can be a natural-language question OR a bag of symbol/file names
- Usually the ONLY call you need - answers without further search/node/read
- Returns source code grouped by file (do NOT re-open shown files)
- Max 12 files by default (adjustable via maxFiles)

**Examples:**
- codegraph_explore(query: "AuthService loginUser session-manager")
- codegraph_explore(query: "how does the payment flow work")
- codegraph_explore(query: "GraphTraverser BFS impact traversal.ts")

### Secondary Tools

Use these when codegraph_explore does not give enough detail:

| Tool | Purpose | When to use |
|------|---------|-------------|
| codegraph_search | Find symbols by name | When you know the name but not the location |
| codegraph_node | Get ONE symbol in full detail | When explore trimmed a body you need |
| codegraph_callers | List functions that call a symbol | Tracing who uses something |
| codegraph_callees | List functions a symbol calls | Understanding what something depends on |
| codegraph_impact | List symbols affected by changing a symbol | Before refactoring |
| codegraph_files | Indexed file tree with language + symbol counts | Project layout overview |
| codegraph_status | Index health check | Debugging only |

## Decision Flow

- "How does X work?" - codegraph_explore(query: "X")
- "Where is X defined?" - codegraph_search(query: "X")
- "Who calls X?" - codegraph_callers(symbol: "X")
- "What does X call?" - codegraph_callees(symbol: "X")
- "What breaks if I change X?" - codegraph_impact(symbol: "X")
- "Show me the full source of X" - codegraph_node(symbol: "X", includeCode: true)
- "What is the project structure?" - codegraph_files()

## Best Practices

1. **Start with codegraph_explore** - it handles 80% of questions in one call
2. **Do not re-read files** that explore already showed you
3. **Use codegraph_search first** if you need to find the exact symbol name before calling other tools
4. **Use codegraph_impact before refactoring** - know what will break
5. **Prefer codegraph over grep/read** for code understanding - it is semantically aware
6. **Pass includeCode: true to codegraph_node** only when you need the full body (explore may have trimmed it)
7. **Always cache results** to the active project .codegraph/explore-cache.md for future reference

## When NOT to Use CodeGraph

- Writing new files (use fs_write)
- Editing existing code (use str_replace)
- Reading non-code files (config, markdown, JSON - use read_file)
- The file is not indexed (check with codegraph_status if unsure)

## Supported Languages

TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Objective-C, Swift, Kotlin, Dart, Lua, Svelte, and more (20+ total via tree-sitter).
