/*global devstudyAPP*/
'use strict';

devstudyAPP.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
  $routeProvider
    // home page
    .when('/', {
        templateUrl: 'views/pages/home.html',
        controller: 'HomeController'
    })
    .when('/yuma', {
        templateUrl: 'views/pages/monitoring_yuma_view.html',
        controller: 'MonitoringYumaController'
    })
    .when('/hector', {
        templateUrl: 'views/pages/monitoring_hector_view.html',
        controller: 'MonitoringHectorController'
    })
    .when('/surprice', {
        templateUrl: 'views/pages/monitoring_surprice_view.html',
        controller: 'MonitoringSurpriceController'
    })
    .when('/all', {
        templateUrl: 'views/pages/monitoring_view.html',
        controller: 'MonitoringController'
    })
    .otherwise({
			redirectTo: '/'
		});
    $locationProvider.html5Mode(true);
}]);
