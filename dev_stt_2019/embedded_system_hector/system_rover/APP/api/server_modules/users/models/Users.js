'use strict';

var mongoose = require('mongoose'),
	Schema = mongoose.Schema;


var UsersSchema = new Schema({
	email: {
		type : String,
		required : true
	},
	password: {
		type : String,
		required : true
	},
});

module.exports = mongoose.model('Users', UsersSchema);
