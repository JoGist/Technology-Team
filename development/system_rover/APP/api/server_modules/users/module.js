'use strict';

var controllerName = [
	'Users'
];

var Storekeepers = function init(modules) {

	console.log('Create Controller');
	for (var k in controllerName) {
		console.log('Controller: ', controllerName[k]);
		require('./controllers/' + controllerName[k] + 'Controller.js')(modules);
	}

	return {};
};

module.exports = Storekeepers;
