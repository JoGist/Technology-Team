/*global devstudyAPP*/
'use strict';

devstudyAPP.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
  $routeProvider
    // home page
    .when('/', {
        templateUrl: 'views/pages/leds.html',
        controller: 'LedsController'
    })
    .when('/Gyroscope', {
        templateUrl: 'views/pages/gyroscope.html',
        controller: 'GyroscopeController'
    })
    .when('/Accelerometer', {
        templateUrl: 'views/pages/accelerometer.html',
        controller: 'AccelerometerController'
    })
    .when('/Imu', {
        templateUrl: 'views/pages/imu.html',
        controller: 'ImuController'
    })
    .otherwise({
			redirectTo: '/'
		});
    $locationProvider.html5Mode(true);

}]);
