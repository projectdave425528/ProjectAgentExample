/**
 * @deterministic
 * @description 建立新 Project 嘅完整目錄結構
 * @input process.argv[2] = project name
 * @output 建立 §6.1 標準結構 + 空白 SearchIndex + conversation-log
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

const PROJECT_RECORD_BASE = path.join(__dirname, '..', '..', 'main-agent', 'ProjectRecord');

const AGENTS = ['main-agent', 'planner', 'generator', 'evaluator'];

const DIRECTORIES = [
  'specs',
  'memory',
  'inbox/main-agent',
  'inbox/planner',
  'inbox/generator',
  'inbox/evaluator',
  'outbox/main-agent',
  'outbox/planner',
  'outbox/generator',
  'outbox/evaluator',
  'checkpoints/main-agent',
  'checkpoints/planner',
  'checkpoints/generator',
  'checkpoints/evaluator',
  'decision-logs/main-agent',
  'decision-logs/planner',
  'decision-logs/generator',
  'decision-logs/evaluator',
  'output',
  'control',
  'UserConfig/sessions',
  'UserDocument',
];

const MEMORY_FILES = AGENTS.map(a => `memory/${a}-memory.md`);

const MEMORY_TEMPLATE = (agentName) => `# ${agentName} Memory

## 最近任務
| 日期 | 摘要 | 結果 | 學到咩 |
|------|------|------|--------|

## 重要教訓（永久）
（空）

## 項目知識
（空）
`;

function main(projectName) {
  if (!projectName) {
    console.error('Usage: node create-project.js <project-name>');
    process.exit(1);
  }

  const projectDir = path.join(PROJECT_RECORD_BASE, projectName);

  // 檢查係咪已存在
  if (fs.existsSync(projectDir)) {
    console.error(`ERROR: Project "${projectName}" already exists at ${projectDir}`);
    process.exit(1);
  }

  // 建立所有目錄
  for (const dir of DIRECTORIES) {
    const fullPath = path.join(projectDir, dir);
    fs.mkdirSync(fullPath, { recursive: true });
    // 加 .gitkeep
    fs.writeFileSync(path.join(fullPath, '.gitkeep'), '');
  }

  // 建立 memory 文件
  for (const agent of AGENTS) {
    const memPath = path.join(projectDir, 'memory', `${agent}-memory.md`);
    fs.writeFileSync(memPath, MEMORY_TEMPLATE(agent));
  }

  // 建立空白 SearchIndex
  fs.writeFileSync(
    path.join(projectDir, 'SearchIndex.md'),
    `# SearchIndex: ${projectName}\n\n| # | ID | Agent | Type | Status | Summary | File |\n|---|----|----|------|--------|---------|------|\n`
  );

  // 建立空白 conversation-log
  fs.writeFileSync(
    path.join(projectDir, 'conversation-log.md'),
    `# Conversation Log: ${projectName}\n\n---\n`
  );

  console.log(JSON.stringify({
    status: 'PASS',
    project: projectName,
    path: projectDir,
    directories: DIRECTORIES.length,
    files: MEMORY_FILES.length + 2, // memory + SearchIndex + conversation-log
  }, null, 2));
}

// 自帶驗證
function verify() {
  const testName = '__test_project_' + Date.now();
  const testDir = path.join(PROJECT_RECORD_BASE, testName);

  try {
    // 執行建立
    main(testName);

    // 驗證目錄存在
    for (const dir of DIRECTORIES) {
      assert.ok(
        fs.existsSync(path.join(testDir, dir)),
        `Missing directory: ${dir}`
      );
    }

    // 驗證 memory 文件
    for (const agent of AGENTS) {
      const memPath = path.join(testDir, 'memory', `${agent}-memory.md`);
      assert.ok(fs.existsSync(memPath), `Missing memory: ${agent}`);
      const content = fs.readFileSync(memPath, 'utf-8');
      assert.ok(content.includes('重要教訓（永久）'), `Memory missing 永久 section: ${agent}`);
    }

    // 驗證 SearchIndex
    assert.ok(fs.existsSync(path.join(testDir, 'SearchIndex.md')));

    // 驗證 conversation-log
    assert.ok(fs.existsSync(path.join(testDir, 'conversation-log.md')));

    console.log(JSON.stringify({ status: 'VERIFY_PASS', testProject: testName }));
  } finally {
    // 清理
    fs.rmSync(testDir, { recursive: true, force: true });
  }
}

if (require.main === module) {
  const arg = process.argv[2];
  if (arg === '--verify') {
    verify();
  } else {
    main(arg);
  }
}

module.exports = { main };
