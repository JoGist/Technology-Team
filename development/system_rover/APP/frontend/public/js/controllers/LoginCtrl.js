/* global devstudyAPP */
'use strict';

devstudyAPP.controller('LoginController',
    function($scope, $http) {
      var url = 'http://api.devstudy.com/';

     
      $scope.login = function () {
        var callParams = {
          url: url+"Users",
          method: 'GET',
          params: {email:$scope.email, password:$scope.password}
        };
        $http(callParams)
         .success(function(data, status, headers, config) {
              console.log('Sucees: ',data);
              console.log('Status: ',status);
            }).error(function(data, status, headers, config) {
              console.log('Error: ',data);
              console.log('Status: ',data);
            });
      };
      $scope.register = function () {
        console.log($scope.email,$scope.password,$scope.repeatPassword);
        if ($scope.email && $scope.password && $scope.repeatPassword && $scope.password === $scope.repeatPassword) {
          var object = {email:$scope.email, password:$scope.password};
          $http.post(url+"Users", object)
            .success(function(data, status, headers, config) {
              console.log('Sucees: ',data);
              console.log('Status: ',status);
            }).error(function(data, status, headers, config) {
              console.log('Error: ',data);
              console.log('Status: ',data);
            });
        }
      };

      $scope.toggleClick = function(){
        $scope.activeRegister = ' active';
      };
      $scope.closeClick = function(){
        $scope.activeRegister = '';
      };
    }
);
