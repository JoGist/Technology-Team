/* global devstudyAPP */
'use strict';

devstudyAPP.controller('LedsController',
    function($scope, $http) {
      var url = 'http://api.devstudy.com/';

      $scope.greenActive = false;
      $scope.yellowActive = false;
      $scope.redActive = false;

      $scope.leds = {
        green : false,
        yellow: false,
        red: false
      }
      var callParams = {
          url: url+"Leds",
          method: 'GET',
          params: {color:'green'}
        };
        $http(callParams)
         .success(function(data, status, headers, config) {
              	if(data.result === 1){
			$scope.leds.green = true;
		}
		//console.log('Sucees: ',data);
              //console.log('Status: ',status);
            }).error(function(data, status, headers, config) {
             // console.log('Error: ',data);
             // console.log('Status: ',data);
            });
	callParams.params = {color:'yellow'};
	$http(callParams)
	 .success(function(data){
	 	if(data.result === 1){
			$scope.leds.yellow = true;
		}
	 });
	callParams.params = {color:'red'};
	$http(callParams)
	 .success(function(data){
	 	if(data.result === 1){
			$scope.leds.red = true;
		}
	 });
            
      $scope.click = function(value) {
        if (value === 'green') {
          $scope.leds.green = !$scope.leds.green;
        } else if(value === 'yellow') {
          $scope.leds.yellow = !$scope.leds.yellow;
        } else if(value === 'red') {
          $scope.leds.red = !$scope.leds.red;
        }
        var object = {color:value};
          $http.post(url+"Leds", object)
            .success(function(data, status, headers, config) {
              console.log('Sucees: ',data);
              console.log('Status: ',status);
            }).error(function(data, status, headers, config) {
              console.log('Error: ',data);
              console.log('Status: ',data);
            });
          
      };
    }
);
