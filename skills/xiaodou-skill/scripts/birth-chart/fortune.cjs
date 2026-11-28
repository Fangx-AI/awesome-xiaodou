const { randomInt } = require('node:crypto');
const { collection, source, lots } = require('../../references/guandi-lots.json');

const [argument, extra] = process.argv.slice(2);
if (extra !== undefined || (argument !== undefined && !/^(?:[1-9]\d?|100)$/.test(argument))) {
  process.stderr.write('Usage: node fortune.cjs [lot number from 1 to 100]\n');
  process.exitCode = 1;
} else {
  const lot = lots[argument === undefined ? randomInt(lots.length) : Number(argument) - 1];
  process.stdout.write(JSON.stringify({
    collection, selection: argument === undefined ? 'random' : 'lookup',
    ...lot, source: source + '/' + lot.number,
  }, null, 2) + '\n');
}
