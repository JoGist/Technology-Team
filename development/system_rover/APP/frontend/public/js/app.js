'use strict';

var devstudyAPP = angular.module('devstudyAPP', [
	'ngRoute',
	'n3-line-chart'
]);

devstudyAPP.factory('APPConfig', function() {
	var nameUrl = 'devstudy';
	//var nameUrl = 'labeloop';
	return {
		apiBaseUrl: 'http://api.'+nameUrl+'.com/',
		apiImagesBaseUrl: 'http://api.labeloop.com/',//labeloop
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
