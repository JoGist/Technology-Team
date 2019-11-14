'use strict';

var controllerName = 'Users',
	Model = require('../models/' + controllerName + '.js'),
	StructResultClient = require('../../responseClient/controllers/StructResultClientController.js')();
	console.log(StructResultClient);
var UsersController = function init(modules) {
  var router = modules.router;

  router.route('/' + controllerName)
	.post(function (req, res) {
    	console.log('POST');
		var sRC = new StructResultClient();
		var body = req.body;
		if (body && body.email && body.password) {
			var user = new Model({
				email : body.email,
				password : body.password
			});
			user.save(function(err, user){
				if (!err) {
					sRC.jsonStruct.result = user;
					sRC.jsonSendToClient(res);
				} else {
					res.sendStatus(400);
				}
			});
		} else {
			res.sendStatus(400);
		}
    })

    .get(function(req, res) {
    	console.log('GET');
    	var query = req.query;
    	if (query && query.email && query.password) {
    		var filter = {
    			email: query.email,
    			password: query.password
    		};
    		Model
			.find(query)
			.exec(function(err, users) {
				console.log(users);
				if (!err && users && users.length===1) {
					res.sendStatus(200);
				} else {
					res.sendStatus(401);
				}
			});
		} else {
			res.sendStatus(400);
		}
    })
}


module.exports = UsersController;
