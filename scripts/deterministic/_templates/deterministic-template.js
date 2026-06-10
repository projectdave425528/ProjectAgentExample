/**
 * @deterministic
 * @task {TASK-ID}
 * @description {一句話描述呢個腳本做咩}
 * @input {描述輸入格式}
 * @output {描述預期輸出格式}
 */

'use strict';

const assert = require('assert');

/**
 * 主邏輯函數 — 確定性計算，唔涉及任何 AI/LLM
 * @param {*} input - 輸入數據
 * @returns {*} 計算結果
 */
function main(input) {
  // TODO: 實現確定性邏輯
  throw new Error('Not implemented');
}

/**
 * 自帶驗證 — 跑所有 test cases
 * Exit code 0 = 全部 pass, 1 = 有 fail
 */
function verify() {
  const testCases = [
    // TODO: 加入 test cases
    // { input: ..., expected: ... },
  ];

  let passed = 0;
  let failed = 0;

  for (const { input, expected, description } of testCases) {
    try {
      const actual = main(input);
      assert.deepStrictEqual(actual, expected);
      passed++;
    } catch (err) {
      failed++;
      console.error(`FAIL [${description || 'unnamed'}]: ${err.message}`);
    }
  }

  const result = {
    status: failed === 0 ? 'PASS' : 'FAIL',
    passed,
    failed,
    total: testCases.length,
  };

  console.log(JSON.stringify(result, null, 2));
  process.exit(failed === 0 ? 0 : 1);
}

if (require.main === module) {
  verify();
}

module.exports = { main };
