// lambda

const dailyFunctal = require('./daily-functal.js').dailyFunctal

exports.handler = function(event, context, callback) {
  dailyFunctal().then(() => callback(null, `posted`))
}
