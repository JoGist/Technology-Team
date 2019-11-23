'use strict';

var devstudyAPP = angular.module('devstudyAPP', [
	'ngRoute',
	'ngMaterial',
	'chart.js'
]);

devstudyAPP.factory('APPConfig', function() {
	var nameUrl = 'ground_control_system_yuma_rover';

	return {
		apiBaseUrl: 'http://api.'+nameUrl+'.com/',
		domain:nameUrl+'.com'
	};
});

devstudyAPP.factory('PageSettings', function() {
	return {
		fields: {
			title: '',
			description: '',
			keywords: ''
		},
		setMeta: function (title, description, keywords) {
			this.fields.title = title;
			this.fields.description = description;
			this.fields.keywords = keywords;
		}
	};
});


devstudyAPP.controller('MainController', function($scope, PageSettings){
	$scope.PageSettings = PageSettings.fields;

});
