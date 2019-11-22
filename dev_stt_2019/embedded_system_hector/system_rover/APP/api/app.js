'use strict';

global.passwordSalt = 'LABMANP';

global.secretsSalt = {
	storekeeper: 'LABSTRMANP',
	user: 'LABUSRMANP',
	admin: 'ADMANP'
};

global.pathRoot = __dirname + '/';

var express = require('express'),
	app = express();

	//mongoose = require('mongoose'),
	//db = mongoose.connect('mongodb://185.17.107.27:27017/labeloop_new'); // connect to our database
	 //db = mongoose.connect('mongodb://localhost:27017/devstudy'); // connect to our database



require('./config/express.js')(app);

//db.connection.on('error', console.error.bind(console, 'connection error:'));
/*
	INCLUDE SERVER MODULE

*/


var io = require('socket.io')(3001);



var router = express.Router();
var serverModulesPath = './server_modules/';
var serverModules = [
	'leds',
	'responseClient',
	'imu'
];

var modulesList = {
	'express': app,
	'router': router,
	'io': io
};

// Include Modules
for (var k in serverModules) {
	var moduleName = serverModules[k];
	console.log('Module: ', moduleName + '/module.js');
	modulesList[moduleName] = require(serverModulesPath + moduleName + '/module.js')(modulesList);
}

modulesList.express.use('/', modulesList.router);

// catch 404 and forward to error handler
modulesList.express.use(function(req, res, next) {
	var err = new Error('Not Found');
	err.status = 404;
	res.json({
		Error: err
	});
});


module.exports = function(io) {
	return modulesList.express;
};
