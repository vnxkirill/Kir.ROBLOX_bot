function buildMessage(name) {
  return `Hello, ${name}! Your Roblox bot is ready.`;
}

function main() {
  console.log(buildMessage('Kir'));
}

if (require.main === module) {
  main();
}

module.exports = { buildMessage };
