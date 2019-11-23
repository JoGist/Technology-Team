'use strict';

var ErrorModel = require('../models/Errors.js'),
	async = require('async'),
	thisModules = {};


var StructResultClient  = function StructResultClient() {
	this.jsonStruct = {
		success: false,
		result: {},
		errors: [
			{
				code: '',
				message: ''
			}
		]
	};

	this.jsonStruct.errors = [];
	this.asyncTasks = [];
};

StructResultClient.prototype.existError = function() {
		return (this.jsonStruct.errors.length > 0);
};

StructResultClient.prototype.appendError = function (code) {
	var errorUnacknowledged = {
			code: '000',
			message: 'Errore Sconosciuto'
	};

	var taskFunction = function(callback) {
		this.jsonStruct.success = false;
		
		var setErrors = function (err, record) {
			if (err || !record) {
				this.jsonStruct.errors.push(errorUnacknowledged);
			} else {
				this.jsonStruct.errors.push(record);
			}
			callback();
		};

		ErrorModel
			.findOne({code: code})
			.select('-_id -lang -__v')
			.exec(setErrors.bind(this));
	};
	this.asyncTasks.push(taskFunction.bind(this));
};


StructResultClient.prototype.jsonSendToClient = function(res, status) {
	var sendToClientFunction = function () {
		if (!status) {
			status = 200;
		}
		if (this.jsonStruct.errors && this.jsonStruct.errors.length > 0) {
			this.jsonStruct.success = false;
			this.jsonStruct.result = {};
			res.status(status).json(this.jsonStruct);
		} else {
			this.jsonStruct.success = true;
			res.status(200).json(this.jsonStruct);
		}
	};
	async.parallel(this.asyncTasks, sendToClientFunction.bind(this));
};

StructResultClient.prototype.quickSendToClient = function(res) {
	this.jsonStruct.result = (!this.existError());
	this.jsonSendToClient(res);
};

module.exports = function(modules) {
	thisModules = modules;
	return StructResultClient;
};
