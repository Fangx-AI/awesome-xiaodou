const fs = require('node:fs');

function readBirth(input) {
  if (!input || !['bazi', 'ziwei'].includes(input.system)) {
    throw new Error('system must be bazi or ziwei');
  }
  if (typeof input.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(input.date)) {
    throw new Error('date must be a Gregorian YYYY-MM-DD');
  }
  if (typeof input.time !== 'string' || !/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(input.time)) {
    throw new Error('time must be known local civil time in HH:MM');
  }

  const [year, month, day] = input.date.split('-').map(Number);
  const utcDate = new Date(Date.UTC(year, month - 1, day));
  if (year < 1900 || year > 2099 || utcDate.toISOString().slice(0, 10) !== input.date) {
    throw new Error('date must be valid and within 1900 to 2099');
  }
  if (input.system === 'ziwei' && !['male', 'female'].includes(input.sex)) {
    throw new Error('ziwei requires explicit sex parameter: male or female');
  }
  return { ...input, year, month, day, clock: input.time.split(':').map(Number) };
}

function bazi(birth) {
  const { Solar } = require('lunar-javascript');
  const [hour, minute] = birth.clock;
  const pillars = Solar.fromYmdHms(birth.year, birth.month, birth.day, hour, minute, 0)
    .getLunar().getEightChar();
  pillars.setSect(2);
  return {
    engine: 'lunar-javascript',
    settings: { calendar: 'gregorian', timeBasis: 'local-civil', dayPillarSect: 2 },
    pillars: {
      year: pillars.getYear(),
      month: pillars.getMonth(),
      day: pillars.getDay(),
      hour: pillars.getTime(),
    },
  };
}

function ziwei(birth) {
  const { astro, version } = require('iztro');
  const [hour] = birth.clock;
  const hourIndex = Math.floor((hour + 1) / 2);
  const dayDivide = 'forward';
  astro.config({ dayDivide });
  const chart = astro.bySolar(birth.date, hourIndex, birth.sex, true, 'zh-CN');
  return {
    engine: 'iztro',
    version,
    settings: { calendar: 'gregorian', timeBasis: 'local-civil', hourIndex, fixLeap: true, dayDivide },
    lunarDate: chart.lunarDate,
    timeRange: chart.timeRange,
    palaces: chart.palaces.map(palace => ({
      name: palace.name,
      branch: palace.earthlyBranch,
      majorStars: palace.majorStars.map(star => star.name),
    })),
  };
}

try {
  const birth = readBirth(JSON.parse(fs.readFileSync(0, 'utf8')));
  const chart = birth.system === 'bazi' ? bazi(birth) : ziwei(birth);
  process.stdout.write(JSON.stringify({ system: birth.system, ...chart }, null, 2) + '\n');
} catch (error) {
  const message = error.code === 'MODULE_NOT_FOUND'
    ? 'Run npm ci --ignore-scripts in the birth-chart directory first.'
    : error instanceof SyntaxError
      ? 'Expected one JSON object on stdin.'
      : error.message;
  process.stderr.write(message + '\n');
  process.exitCode = 1;
}
