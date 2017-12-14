const path = require('path');
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');
var request = require('request');
var querystring = require('querystring');
var cookieParser = require('cookie-parser');

// load json data
const data = require('./data/train-hsls.json');

// spotify access tokens. part of project.

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

//---------------- catch-all

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, './index.html'));
});

//--------------- start listening

app.listen(port, host, err => {
    if (err) {
        log(err);

        return;
    }

    console.log('App is listening at http://%s:%s', host, port);
});
