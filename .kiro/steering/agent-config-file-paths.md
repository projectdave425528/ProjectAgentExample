---
inclusion: always
description: Root Agent 配置文件路徑索引（L2 - 永遠載入）
---

# Root Agent 配置文件路徑

> 列出本 Agent 可以使用嘅所有配置文件（Steering / Hooks / Settings）。唔包括 Project 文件。

## Steering 文件
| 文件 | 路徑 |
|------|------|
| role.md | `.kiro/steering/role.md` |
| navigation.md | `.kiro/steering/navigation.md` |
| tools.md | `.kiro/steering/tools.md` |
| agent-config-file-paths.md | `.kiro/steering/agent-config-file-paths.md` |
| role-execution.md | `.kiro/steering/role-execution.md` |
| role-constraints.md | `.kiro/steering/role-constraints.md` |

## Hooks
| Hook | 路徑 | 觸發條件 |
|------|------|---------|
| Auto Commit Config | `.kiro/hooks/auto-commit-config.kiro.hook` | fileEdited (.kiro/) |
| Auto Log Session | `.kiro/hooks/auto-log-session.kiro.hook` | agentStop |
| Remind Update Config (Deleted) | `.kiro/hooks/remind-update-config-deleted.kiro.hook` | fileDeleted (.kiro/) |
| Sync Config from GitHub | `.kiro/hooks/sync-config-from-github.kiro.hook` | userTriggered |
| Watch Agent Replies | `.kiro/hooks/watch-agent-replies.kiro.hook` | fileCreated (outbox/) |

## Settings
| 文件 | 路徑 |
|------|------|
| MCP Config | `.kiro/settings/mcp.json`（如存在） |
