'use strict';

var express = require('express'),
	app = express();


require('./config/express.js')(app);

var io = require('socket.io')(3001);

var router = express.Router();
var serverModulesPath = './server_modules/';
var serverModules = [
	'communication'
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
