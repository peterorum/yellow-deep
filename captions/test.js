const dailyFunctal = require('./daily-functal.js').dailyFunctal

dailyFunctal().then(() => console.log('done'), err => console.error(err))
