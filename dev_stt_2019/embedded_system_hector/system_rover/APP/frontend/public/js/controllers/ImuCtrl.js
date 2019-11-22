/* global devstudyAPP */
'use strict';
// Converts from degrees to radians.
Math.radians = function(degrees) {
  return degrees * Math.PI / 180;
};

// Converts from radians to degrees.
Math.degrees = function(radians) {
  return radians * 180 / Math.PI;
};
devstudyAPP.controller('ImuController',
    function($scope, $http, $interval) {
      var url = 'http://api.devstudy.com/';


      $scope.imuData = {};
      $scope.gyroscope = {
          roll:'0',
          pitch:'0',
          yaw:'0'
      };
      $scope.fusionPose = {
          roll:'0',
          pitch:'0',
          yaw:'0'
      };
      $scope.fusionQPose = {
          roll:'0',
          pitch:'0',
          yaw:'0'
      };

      $scope.compass = {
          x:'0',
          y:'0',
          z:'0'
      };
      $scope.accelerometer = {
          x:'0',
          y:'0',
          z:'0'
      };

      $scope.temperature = '0';
      $scope.pressure = '0';

      var callParams = {
          url: url+"Imu",
          method: 'GET',
          params: {color:'green'}
        };
         $interval(function(){
             $http(callParams)
              .success(function(data, status, headers, config) {
                //  console.log('Sucees: ',data.result);
                 $scope.imuData = data.result;
                 $scope.gyroscope.roll = parseFloat($scope.imuData.gyro[0]);
                 $scope.gyroscope.pitch = parseFloat($scope.imuData.gyro[1]);
                 $scope.gyroscope.yaw = parseFloat($scope.imuData.gyro[2]);

                 $scope.fusionPose.roll = Math.degrees($scope.imuData.fusionPose[0]);
                 $scope.fusionPose.pitch = Math.degrees($scope.imuData.fusionPose[1]);
                 $scope.fusionPose.yaw = Math.degrees($scope.imuData.fusionPose[2]);

                 $scope.figureStyle={
                      'transform':' rotateX( '+$scope.fusionPose.roll+'deg )'
                 };
                 $scope.figureStyle={
                      'transform':' rotateY( '+$scope.fusionPose.pitch+'deg )'
                 };
                 $scope.figureStyle={
                      'transform':' rotateZ( '+$scope.fusionPose.yaw+'deg )'
                 };

                 $scope.fusionQPose.roll = Math.degrees($scope.imuData.fusionQPose[0]);
                 $scope.fusionQPose.pitch = Math.degrees($scope.imuData.fusionQPose[1]);
                 $scope.fusionQPose.yaw = Math.degrees($scope.imuData.fusionQPose[2]);

                 $scope.compass.x = $scope.imuData.compass[0];
                 $scope.compass.y = $scope.imuData.compass[1];
                 $scope.compass.z = $scope.imuData.compass[2];

                  $scope.accelerometer.x = $scope.imuData.accel[0];
                  $scope.accelerometer.y = $scope.imuData.accel[1];
                  $scope.accelerometer.z = $scope.imuData.accel[2];


                  $scope.temperature = $scope.imuData.temperature;
                  $scope.pressure = $scope.imuData.pressure;
                 //console.log('Status: ',status);
              }).error(function(data, status, headers, config) {
                 // console.log('Error: ',data);
                 // console.log('Status: ',data);
              });
         }, 1000);

        // $scope.roll = function(){
        //     console.log('roll');
        //     $scope.figureStyle={
        //          'transform':' rotateZ( 20deg )'
        //     };
        // }
    }
);
