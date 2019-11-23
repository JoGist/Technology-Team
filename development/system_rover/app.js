'use strict';

var express = require('express'),
	vhost = require('vhost'),
	app = express();

global.domainName = 'devstudy.com';
global.subdomainDisabled = false;

var server = require('http').Server(app);
var io = require('socket.io')(server);


app.all('/*', function(req, res, next) {
	var origin = 'http://www.' + global.domainName;
	if (!global.subdomainDisabled && (
		req.headers.origin === 'http://api.' + global.domainName ||
		req.headers.origin === 'http://www.' + global.domainName)) {
		origin = req.headers.origin;
	}

	res.setHeader('Access-Control-Allow-Origin', origin);
	res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
	res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,Content-type,Accept,X-Access-Token,X-Key,authorization');
	res.setHeader('Access-Control-Allow-Credentials', true);

	if (req.method === 'OPTIONS') {
		res.status(200).end();
	} else {
		next();
	}
});

app
	.use(vhost(global.domainName, function(req, res) {
		res.writeHead(303, {'Location': 'http://www.' + global.domainName + req.url});
		res.end();
	}))
	.use('/api',		require('./APP/api/app')(io))
	.use('/',			require('./APP/frontend/app'));


app.set('port', 80);




console.log('--------SYSTEM LOADED--------');
app.listen(app.get('port'), function() {
	console.log('Express server listening on port ' + app.get('port'));
});
