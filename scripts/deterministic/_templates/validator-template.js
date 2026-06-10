/**
 * @deterministic
 * @task {TASK-ID}
 * @description 格式驗證模板（JSON Schema / 日期 / Email 等）
 * @input { data: any, rules: Array<Rule> }
 * @output { valid: boolean, errors: string[] }
 */

'use strict';

const assert = require('assert');

/**
 * 內建驗證規則
 */
const Validators = {
  required: (value) => value !== null && value !== undefined && value !== '',
  isString: (value) => typeof value === 'string',
  isNumber: (value) => typeof value === 'number' && !isNaN(value),
  isBoolean: (value) => typeof value === 'boolean',
  isEmail: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
  isDate: (value) => !isNaN(Date.parse(value)),
  minLength: (value, min) => typeof value === 'string' && value.length >= min,
  maxLength: (value, max) => typeof value === 'string' && value.length <= max,
  min: (value, min) => typeof value === 'number' && value >= min,
  max: (value, max) => typeof value === 'number' && value <= max,
  pattern: (value, regex) => new RegExp(regex).test(value),
  oneOf: (value, options) => options.includes(value),
};

/**
 * 主邏輯 — 逐條規則驗證
 * @param {{ data: Record<string, any>, rules: Array<{ field: string, check: string, args?: any[] }> }} input
 * @returns {{ valid: boolean, errors: string[] }}
 */
function main(input) {
  const { data, rules } = input;
  const errors = [];

  for (const rule of rules) {
    const { field, check, args = [] } = rule;
    const value = data[field];
    const validator = Validators[check];

    if (!validator) {
      errors.push(`Unknown validator: ${check}`);
      continue;
    }

    const isValid = validator(value, ...args);
    if (!isValid) {
      errors.push(`Field "${field}" failed "${check}" check (value: ${JSON.stringify(value)})`);
    }
  }

  return { valid: errors.length === 0, errors };
}

function verify() {
  const testCases = [
    {
      description: '全部通過',
      input: {
        data: { name: 'John', email: 'john@example.com', age: 25 },
        rules: [
          { field: 'name', check: 'required' },
          { field: 'name', check: 'isString' },
          { field: 'email', check: 'isEmail' },
          { field: 'age', check: 'min', args: [18] },
        ],
      },
      expected: { valid: true, errors: [] },
    },
    {
      description: 'Email 格式錯誤',
      input: {
        data: { name: 'John', email: 'not-an-email', age: 25 },
        rules: [
          { field: 'email', check: 'isEmail' },
        ],
      },
      expected: { valid: false, errors: ['Field "email" failed "isEmail" check (value: "not-an-email")'] },
    },
    {
      description: '多重驗證失敗',
      input: {
        data: { name: '', email: 'bad', age: 15 },
        rules: [
          { field: 'name', check: 'required' },
          { field: 'email', check: 'isEmail' },
          { field: 'age', check: 'min', args: [18] },
        ],
      },
      expected: {
        valid: false,
        errors: [
          'Field "name" failed "required" check (value: "")',
          'Field "email" failed "isEmail" check (value: "bad")',
          'Field "age" failed "min" check (value: 15)',
        ],
      },
    },
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
      console.error(`FAIL [${description}]: ${err.message}`);
    }
  }

  const result = { status: failed === 0 ? 'PASS' : 'FAIL', passed, failed, total: testCases.length };
  console.log(JSON.stringify(result, null, 2));
  process.exit(failed === 0 ? 0 : 1);
}

if (require.main === module) {
  verify();
}

module.exports = { main, Validators };
