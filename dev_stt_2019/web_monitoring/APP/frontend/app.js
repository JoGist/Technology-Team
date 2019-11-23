'use strict';
var express = require('express'),
	path = require('path'),
	//favicon = require('serve-favicon'),
	logger = require('morgan'),
	cookieParser = require('cookie-parser'),
	bodyParser = require('body-parser'),
	app = express();

/*
 * Gloabal Options
 */
 global.frontendPath = __dirname;

/*
 * Template Engine
 */
/*var ECT = require('ect');
var ectRenderer = ECT({ watch: true, root: __dirname + '/views', ext : '.ect' });

app.set('views', __dirname + '/views');
app.set('view engine', 'ect');
app.engine('ect', ectRenderer.render);*/

// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());


app.use(express.static(path.join(__dirname, 'public')));
app.use('*', function(req, res) {
	res.sendFile( global.frontendPath + '/public/index.html');
});


// catch 404 and forward to error handler
app.use(function(req, res, next) {
	var err = new Error('Not Found');
	err.status = 404;
	next(err);
});

// error handlers

// development error handler
// will print stacktrace
// if (app.get('env') === 'development') {
// 	app.use(function(err, req, res) {
// 		res.status(err.status || 500);
// 		res.render('index', {
// 			message: err.message,
// 			error: err
// 		});
// 	});
// }

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res) {
	res.status(err.status || 500);
	res.render('index', {
		message: err.message,
		error: {}
	});
});


module.exports = app;
