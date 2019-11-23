'use strict';

var express = require('express'),
	fs = require('fs'),
	compression = require('compression'),
	logger = require('morgan'),
	session = require('express-session'),
	// mongoStore = require('connect-mongo')(session),
	// cookieParser = require('cookie-parser'),
	bodyParser = require('body-parser');
	// ECT = require('ect'),
	// ectRenderer = ECT({ watch: true, root: global.pathRoot + '/public', ext : '.ect' });

module.exports = function(app, db) {
	// app.set('views', global.pathRoot + '/public');
	// app.set('view engine', 'ect');
	// app.engine('ect', ectRenderer.render);


	app.set('showStackError', true);

	// Should be placed before express.static
	// To ensure that all assets and data are compressed (utilize bandwidth)
	app.use(compression({
		// Levels are specified in a range of 0 to 9, where-as 0 is
		// no compression and 9 is best compression, but slowest
		level: 9
	}));

	// create a write stream (in append mode)
	var accessLogStream = fs.createWriteStream(global.pathRoot + '/log/access.log', {flags: 'a'});
	// setup the logger
	app.use(logger('combined', {stream: accessLogStream}));

	// Only use logger for development environment
	if (process.env.NODE_ENV === 'development') {
		app.use(logger('dev'));
	}

	app.use(bodyParser.json({
		limit: '500mb'
	}));
	app.use(bodyParser.urlencoded({
		extended: true,
		limit: '500mb'
	}));
	// app.use(cookieParser());

	// app.use(session({
	// 	secret: 'LBLOOP',
	// 	store: new mongoStore({
	// 		db: db.connection.db,
	// 		collection: 'sessions'
	// 	}),
	// 	cookie: {
	// 		path: '/',
	// 		httpOnly: true,
	// 		// If secure is set to true then it will cause the cookie to be set
	// 		// only when SSL-enabled (HTTPS) is used, and otherwise it won't
	// 		// set a cookie. 'true' is recommended yet it requires the above
	// 		// mentioned pre-requisite.
	// 		secure: false,
	// 		// Only set the maxAge to null if the cookie shouldn't be expired
	// 		// at all. The cookie will expunge when the browser is closed.
	// 		maxAge: null
	// 	},
	// 	name: 'connect.sid',
	// 	resave: true,
	// 	saveUninitialized: true
	// }));
};
