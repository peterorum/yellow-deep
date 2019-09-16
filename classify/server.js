const path = require('path')
const fs = require('fs')
const express = require('express')
const bodyParser = require('body-parser')
var request = require('request')
var querystring = require('querystring')
var cookieParser = require('cookie-parser')
var url = require('url')

// load json data

// to view prediction results
// const testDataFile = '../data/predictions.json'

// to view functals
const testDataFile = '../data/functal-palettes.json'

// for adding more training
// const testDataFile = '../data/test-palettes.json'

const trainDataFile = '../data/manually-selected-palettes.json'

const testPalettes = require(testDataFile)
let trainPalettes = require(trainDataFile)

// new data or training
let mode

const app = express()

const host = process.env.HOST || 'localhost'
const port = process.env.PORT || 3010

//----- express settings

// create application/json parser
var jsonParser = bodyParser.json()

// create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({
  extended: false
})

app.use(cookieParser())

//--------- serve a file

var sendFile = function(res, filename) {
  var filepath = path.join(process.cwd(), filename)

  res.sendFile(filepath, function(err) {
    if (err) {
      console.log(err)
      res.status(err.status).end()
    } else {
      console.log('sent:', filename)
    }
  })
}

// --- routing

//-- files

app.get(/\.(js|css|png|jpg|html)$/, function(req, res) {
  var uri = url.parse(req.url, true, false)

  console.log(uri.pathname);
  sendFile(res, uri.pathname)
})

//-- data

app.get('/palettes', (req, res) => {
  // /palettes?data=train

  var uri = url.parse(req.url, true, false)

  mode = uri.query.data

  let palettes

  if (mode === 'new') {
    palettes = testPalettes
  } else {
    palettes = trainPalettes
  }

  res.json({
    palettes
  })

  console.log('sent data')
})

//-- toggle selection
// overwrites whole json file on each update

app.post('/update-selection', jsonParser, (req, res) => {
  const { id } = req.body

  const palettes = mode === 'new' ? testPalettes : trainPalettes

  const palette = palettes.find(p => p.id === id)

  if (palette) {
    palette.selected = !palette.selected

    const dataFile = mode === 'new' ? testDataFile : trainDataFile

    fs.writeFile(dataFile, JSON.stringify(palettes, null, 4), function(err) {
      if (err) {
        console.error('Error writing data file', err)
        res.json({ status: 'error', error: err })
      } else {
        res.json({ status: 'ok' })
      }
    })
  } else {
    console.log('Palette not found. Voting on test?')
  }
})

// -- catch-all

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, './index.html'))
})

// -- start listening

app.listen(port, host, err => {
  if (err) {
    log(err)

    return
  }

  console.log('App is listening at http://%s:%s', host, port)
})
