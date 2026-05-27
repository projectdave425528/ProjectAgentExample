---
inclusion: manual
---

# Kiro 機制知識庫

## 五大核心機制

### 1. Specs（規格驅動開發）
- **4種類型**：Feature（Requirements-First / Design-First / Quick Plan）、Bugfix
- **3個文件**：requirements.md、design.md、tasks.md
- **EARS格式**：`WHEN [條件] THE SYSTEM SHALL [行為]`
- **Task並行**：Kiro 自動建立 Dependency Graph，分 Wave 並行執行

### 2. Steering（持久化記憶）
- **3種範圍**：Workspace（.kiro/steering/）、Global（~/.kiro/steering/）、Team
- **4種 inclusion**：always、fileMatch、manual、auto
- **3個基礎文件**：product.md、tech.md、structure.md
- **File References**：`#[[file:<relative_file_name>]]`
- **AGENTS.md**：永遠自動載入，唔支援 inclusion modes

### 3. Hooks（事件驅動自動化）
- **10種觸發事件**：fileEdited、fileCreated、fileDeleted、promptSubmit、agentStop、preToolUse、postToolUse、preTaskExecution、postTaskExecution、userTriggered
- **2種動作**：askAgent（prompt）、runCommand（shell）
- **toolTypes**：read、write、shell、web、spec、*、regex
- **位置**：.kiro/hooks/*.json

### 4. MCP Servers
- **配置位置**：.kiro/settings/mcp.json（workspace）、~/.kiro/settings/mcp.json（global）
- **用戶 MCP**：fetch（uvx，disabled）、playwright（npx，disabled）
- **Template MCP**：supabase、fetch、git、chrome、docker、time、memory、sequential-thinking

### 5. Agent Skills
- **位置**：.kiro/skills/（workspace）、~/.kiro/skills/（global）
- **格式**：每個 Skill 係一個有 SKILL.md 的 folder
- **已安裝**：17 個 Anthropic 官方 Skills

## 記憶系統 4 層
1. **Steering Files** — 永久規範記憶（最重要）
2. **Codebase Index** — 代碼語義記憶（自動）
3. **Session History** — 對話短期記憶（IDE History 按鈕）
4. **Bedrock AgentCore Memory** — 跨 session 長期記憶（需額外設定）

## Session 管理
- IDE：Chat Panel → History 按鈕 → 還原舊 session
- IDE：右鍵 Tab → Export Conversation → 輸出 .md
- CLI：`kiro-cli chat --resume`、`--resume-picker`

## 重要參考
- 官方文檔：https://kiro.dev/docs
- Template GitHub：https://github.com/BinarySword/kiro-project-template
- Harness + Kiro：https://www.harness.io/blog/amazon-kiro-and-harness
