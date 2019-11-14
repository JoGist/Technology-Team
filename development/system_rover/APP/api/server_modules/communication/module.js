'use strict';

var controllerName = [
	'Communication'
];

var Communication = function init(modules) {
	console.log('Create Controller');
	for (var k in controllerName) {
		console.log('Controller: ', controllerName[k]);
		require('./controllers/' + controllerName[k] + 'Controller.js')(modules);
	}

	return {};
};

module.exports = Communication;
