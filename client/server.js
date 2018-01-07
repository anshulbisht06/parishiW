var express = require('express');
var app = express();
var path = require('path');

app.use(express.static('../client'));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(7001, function(){
  console.log('UI server up');
});