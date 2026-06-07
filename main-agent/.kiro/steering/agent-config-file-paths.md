---
inclusion: always
description: Main Agent 配置文件路徑索引（L2 - 永遠載入）
---

# Main Agent 配置文件路徑

> 列出本 Agent 可以使用嘅所有配置文件（Steering / Hooks / Agents / Settings）。唔包括 Project 文件。

## Steering 文件
| 文件 | 路徑 |
|------|------|
| role.md | `main-agent/.kiro/steering/role.md` |
| navigation.md | `main-agent/.kiro/steering/navigation.md` |
| tools.md | `main-agent/.kiro/steering/tools.md` |
| agent-config-file-paths.md | `main-agent/.kiro/steering/agent-config-file-paths.md` |
| project-file-paths.md | `main-agent/.kiro/steering/project-file-paths.md` |
| project-protocols-comm.md | `main-agent/.kiro/steering/project-protocols-comm.md` |
| project-protocols-checkpoint.md | `main-agent/.kiro/steering/project-protocols-checkpoint.md` |
| project-protocols-memory.md | `main-agent/.kiro/steering/project-protocols-memory.md` |
| project-protocols-record-write.md | `main-agent/.kiro/steering/project-protocols-record-write.md` |
| project-protocols-format.md | `main-agent/.kiro/steering/project-protocols-format.md` |
| project-protocols-git.md | `main-agent/.kiro/steering/project-protocols-git.md` |
| project-protocols-error-handling.md | `main-agent/.kiro/steering/project-protocols-error-handling.md` |
| project-protocols-size-rules.md | `main-agent/.kiro/steering/project-protocols-size-rules.md` |
| project-protocols-shell-policy.md | `main-agent/.kiro/steering/project-protocols-shell-policy.md` |
| role-execution.md | `main-agent/.kiro/steering/role-execution.md` |
| role-constraints.md | `main-agent/.kiro/steering/role-constraints.md` |

## Hooks
| Hook | 路徑 | 觸發條件 |
|------|------|---------|
| Auto Log Session | `main-agent/.kiro/hooks/auto-log-session.kiro.hook` | agentStop |
| Watch Evaluator Reply | `main-agent/.kiro/hooks/watch-evaluator-reply.kiro.hook` | fileCreated (outbox/evaluator/) |
| Watch Generator Reply | `main-agent/.kiro/hooks/watch-generator-reply.kiro.hook` | fileCreated (outbox/generator/) |
| Watch Planner Reply | `main-agent/.kiro/hooks/watch-planner-reply.kiro.hook` | fileCreated (outbox/planner/) |

## Agent Configs
| Agent | 路徑 |
|-------|------|
| Evaluator | `main-agent/.kiro/agents/evaluator.json` |
| Generator | `main-agent/.kiro/agents/generator.json` |
| Planner | `main-agent/.kiro/agents/planner.json` |
