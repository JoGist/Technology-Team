var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
	res.render('index', { title: 'Express' });
});

/* GET Search. */
router.get('/search', function(req, res) {
	console.log('Search: ', res, res.render);
	res.render('search', { title: 'Prova' });
});

module.exports = router;
