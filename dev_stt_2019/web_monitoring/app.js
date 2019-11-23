'use strict';

var express = require('express'),
	vhost = require('vhost'),
	app = express();

global.domainName = 'ground_control_stt.com';
global.subdomainDisabled = true;

app.all('/*', function(req, res, next) {
	var origin = 'http://' + global.domainName;
	if (!global.subdomainDisabled && (
		req.headers.origin === 'http://api.' + global.domainName ||
		req.headers.origin === 'http://' + global.domainName)) {
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

if (global.subdomainDisabled) {
	app
		// .use(vhost(global.domainName, function(req, res) {
		// 	res.writeHead(303, {'Location': 'http://' + global.domainName + req.url});
		// 	res.end();
		// }))
		.use('/api',		require('./APP/api/app'))
		.use('/',			require('./APP/frontend/app'));
} else {
	app
		.use( vhost(''+ global.domainName, function(req, res) {
			res.writeHead(303, {'Location': 'http://' + global.domainName + req.url});
			res.end();
		}))
		.use(vhost(global.domainName, require('./APP/frontend/app')))
		.use(vhost('api.' + global.domainName, require('./APP/api/app')));
}

app.set('port', 80);

console.log('--------SYSTEM LOADED--------');
app.listen(app.get('port'), function() {
	console.log('Express server listening on port ' + app.get('port'));
});
