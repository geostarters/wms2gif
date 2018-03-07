var express = require('express');
var logger = require('morgan');
var serveStatic = require('serve-static');
var path = require('path');

var routes = require('./routes/index');
var config = require('./config');

var app = express();

app.set('view engine', 'jade');
app.use(logger('dev'));
app.use('/' + config.pathMainWeb + '/generated/', serveStatic(path.join(__dirname, 'generated')));
app.use('/', routes);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found!!');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

app.listen(3006, () => console.log("Listening on port 3006"));

module.exports = app;
