const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const entry = path.resolve(process.argv[2], 'chart.cjs');

function runChart(input) {
  const result = spawnSync(process.execPath, [entry], {
    input: JSON.stringify(input),
    encoding: 'utf8',
    timeout: 10000,
  });
  if (result.error) throw result.error;
  return result;
}

function chart(input) {
  const result = runChart(input);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, '');
  return JSON.parse(result.stdout);
}

// Cross-check the four pillars against the bundled upstream tests (cases A and C).
const bazi = { system: 'bazi', date: '2000-07-20', time: '10:30' };
const ordinary = chart(bazi);
assert.equal(ordinary.settings.dayPillarSect, 2);
assert.deepEqual(ordinary.pillars, { year: '庚辰', month: '癸未', day: '己卯', hour: '己巳' });
const beforeSpring = chart({ ...bazi, date: '2008-01-20', time: '06:00' });
assert.deepEqual(beforeSpring.pillars, { year: '丁亥', month: '癸丑', day: '己未', hour: '丁卯' });

// HKO's 2022 calendar maps April 4 to lunar month 3 day 4, the bundled Case-J4.
const ziwei = { system: 'ziwei', date: '2022-04-04', time: '04:20', sex: 'male' };
const yinHour = chart(ziwei);
assert.equal(yinHour.lunarDate, '二〇二二年三月初四');
assert.equal(yinHour.settings.hourIndex, 2);
assert.equal(yinHour.settings.fixLeap, true);
assert.equal(yinHour.palaces.length, 12);
assert.deepEqual(yinHour.palaces.find(palace => palace.name === '命宫'), {
  name: '命宫', branch: '寅', majorStars: ['紫微', '天府'],
});
assert.deepEqual(Object.fromEntries(yinHour.palaces.map(palace => [palace.branch, palace.majorStars])), {
  寅: ['紫微', '天府'], 卯: ['太阴'], 辰: ['贪狼'], 巳: ['巨门'], 午: ['廉贞', '天相'], 未: ['天梁'],
  申: ['七杀'], 酉: ['天同'], 戌: ['武曲'], 亥: ['太阳'], 子: ['破军'], 丑: ['天机'],
});

const earlyZi = chart({ ...ziwei, time: '00:20' });
assert.equal(earlyZi.settings.hourIndex, 0);
assert.equal(earlyZi.lunarDate, '二〇二二年三月初四');
const lateZi = chart({ ...ziwei, time: '23:20' });
assert.equal(lateZi.settings.hourIndex, 12);
assert.equal(lateZi.settings.dayDivide, 'forward');
assert.equal(lateZi.lunarDate, '二〇二二年三月初五');

const invalid = runChart({ ...bazi, date: '2000-02-30' });
assert.equal(invalid.status, 1);
assert.equal(invalid.stdout, '');
assert.match(invalid.stderr, /date must be valid/);

console.log('Packed BaZi and Zi Wei chart cases verified.');
