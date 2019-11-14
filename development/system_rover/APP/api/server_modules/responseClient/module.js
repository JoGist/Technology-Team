
'use strict';

var controllerName = [
	//'UpdateErrors',
	'StructResultClient'
];

var ResponseClient = function init(modules) {

	var obj = {};

	console.log('Create Controller');
	for (var k in controllerName) {
		console.log('Controller: ', controllerName[k]);
		obj[controllerName[k]] =require('./controllers/' + controllerName[k] + 'Controller.js')(modules);
	}

	return obj;
};

module.exports = ResponseClient;
