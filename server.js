const path = require('path');
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');
var request = require('request');
var querystring = require('querystring');
var cookieParser = require('cookie-parser');
var url = require('url');

// load json data
const data = require('./data/train-hsls.json');

const app = express();

const host = process.env.HOST || 'localhost';
const port = process.env.PORT || 3010;

//----- express settings

// create application/json parser
var jsonParser = bodyParser.json();

// create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({
  extended: false
});

app.use(cookieParser());

//--------- serve a file

var sendFile = function(res, filename) {
  var filepath = path.join(process.cwd(), filename);

  res.sendFile(filepath, function(err) {
    if (err) {
      console.log(err);
      res.status(err.status).end();
    } else {
      console.log('Sent:', filename);
    }
  });
};

// --- routing

//-- files

app.get(/\.(js|css|png|jpg|html)$/, function(req, res) {
  var uri = url.parse(req.url, true, false);

  sendFile(res, uri.pathname);
});

// -- catch-all

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, './index.html'));
});

// -- start listening

app.listen(port, host, err => {
  if (err) {
    log(err);

    return;
  }

  console.log('App is listening at http://%s:%s', host, port);
});
