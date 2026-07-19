const test = require('node:test');
const assert = require('node:assert/strict');
const { buildMessage } = require('../index');

test('buildMessage includes the provided name', () => {
  assert.equal(buildMessage('Kir'), 'Hello, Kir! Your Roblox bot is ready.');
});
