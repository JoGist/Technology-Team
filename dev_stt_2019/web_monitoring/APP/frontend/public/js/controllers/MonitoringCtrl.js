/* global devstudyAPP */
'use strict';

devstudyAPP.controller('MonitoringController',
function($scope, $http, $interval, $mdDialog){

    setTimeout(function() {
        $scope.$apply(); //this triggers a $digest
        $scope.colors = ['#45b7cd', '#ff6384', '#ff8e72'];
        $scope.labels = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10];
        $scope.series = ['Series A', 'Series B'];
        $scope.onClick = function (points, evt) {console.log(points, evt);};
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.options = {
          scales: {
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {min: 0, max:400}
              }
            ]
          }
        };
        $scope.options2 = {
          scales: {
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {min: 0, max:400}
              }
            ]
          }
        };
        $scope.optionsCompass1 = {
          scales: {
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {min: -25, max:+25}
              }
            ]
          }
        };
        $scope.optionsCompass2 = {
          scales: {
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {min: -35, max:+35}
              }
            ]
          }
        };
        $scope.optionsCompass3 = {
          scales: {
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {min: -50, max:+50}
              }
            ]
          }
        };
        $scope.optionsFusion = {
          scales: {
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                position: 'left',
                ticks: {min: -180, max:+180}
              }
            ]
          }
        };


    }, 0);


    //***********************************************************************//
    //Start YUMA Code
    $scope.ip_address_yuma = 'http://192.168.1.12';
    $scope.link_rover_yuma = $scope.ip_address_yuma + ':3001';
    $scope.link_stream_rover_yuma = $scope.ip_address_yuma + ':8081/stream.mjpg';
    $scope.yuma = {};
    $scope.yuma.active_control=true;

    $scope.yuma.imu_flag = false;
    $scope.yuma.viewImu = function() {
        $scope.yuma.imu_flag = !$scope.yuma.imu_flag;
    }

    $scope.yuma.distance_flag = false;
    $scope.yuma.viewDistance = function() {
        $scope.yuma.distance_flag = !$scope.yuma.distance_flag;
    }

    $scope.yuma.fusion_flag = false;
    $scope.yuma.viewFusion = function() {
        $scope.yuma.fusion_flag = !$scope.yuma.fusion_flag;
    }
    $scope.yuma.data_distance = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_distance2 = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];

    $scope.yuma.data_accelerometer_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_accelerometer_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_accelerometer_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_gyroscope_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_gyroscope_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_gyroscope_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_compass_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_compass_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_compass_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_fusion_pose_roll = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_fusion_pose_pitch = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.yuma.data_fusion_pose_yaw = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];

    $scope.yuma.fusionPose = {};
    $scope.yuma.timer = 0;


    $scope.openYumaScanDistancesModal = function(ev) {
      $scope.yuma.data_scan_distances = [];
      $scope.yuma.setScanDistances();
      $mdDialog.show({
        controller: 'ScanDistancesYumaController',
        templateUrl: 'views/pages/scan_distances/scan_distances_yuma_view.html',
        parent: angular.element(document.body),
        scope: this,
        targetEvent: ev,
        preserveScope: true,
        clickOutsideToClose:true,
        fullscreen: false // Only for -xs, -sm breakpoints.
      })
      .then(function(answer) {
        $scope.status = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.status = 'You cancelled the dialog.';
      });
    };


    var socket_yuma = io.connect($scope.link_rover_yuma);
    $scope.yuma_active= false;

    socket_yuma.on("reconnect_attempt", function(){
        console.log(':(');
        $scope.yuma_active = false;
    });
    socket_yuma.on("disconnect", function(){
        $scope.yuma_active = false;
    });

    socket_yuma.on('news', function (data) {
        $scope.$apply(function(){
            $scope.accelerometer = {
              ax: data.accel[0],
              ay: data.accel[1],
              az: data.accel[2]
            };
            $scope.yuma.data_accelerometer_x[0].push($scope.accelerometer.ax);
            $scope.yuma.data_accelerometer_x[0].shift();
            $scope.yuma.data_accelerometer_y[0].push($scope.accelerometer.ay);
            $scope.yuma.data_accelerometer_y[0].shift();
            $scope.yuma.data_accelerometer_z[0].push($scope.accelerometer.az-1);
            $scope.yuma.data_accelerometer_z[0].shift();

            $scope.gyroscope = {
              roll: data.gyro[0],
              pitch: data.gyro[1],
              yaw: data.gyro[2]
            };
            $scope.yuma.data_gyroscope_x[0].push($scope.gyroscope.roll);
            $scope.yuma.data_gyroscope_x[0].shift();
            $scope.yuma.data_gyroscope_y[0].push($scope.gyroscope.pitch);
            $scope.yuma.data_gyroscope_y[0].shift();
            $scope.yuma.data_gyroscope_z[0].push($scope.gyroscope.yaw);
            $scope.yuma.data_gyroscope_z[0].shift();

            $scope.compass = {
              compass1: data.compass[0],
              compass2: data.compass[1],
              compass3: data.compass[2]
            };
            $scope.yuma.data_compass_x[0].push($scope.compass.compass1);
            $scope.yuma.data_compass_x[0].shift();
            $scope.yuma.data_compass_y[0].push($scope.compass.compass2);
            $scope.yuma.data_compass_y[0].shift();
            $scope.yuma.data_compass_z[0].push($scope.compass.compass3);
            $scope.yuma.data_compass_z[0].shift();


            $scope.yuma.fusionPose.roll = (data.fusionPose[0]*180/3.14);
            $scope.yuma.fusionPose.pitch = (data.fusionPose[1]*180/3.14);
            if (data.fusionPose[2] >= -3.14159/2) {
                data.fusionPose[2] = data.fusionPose[2] - 3.14159/2
            } else {
                data.fusionPose[2] = data.fusionPose[2] + 3.14159*3/2
            }
            $scope.yuma.fusionPose.yaw = (data.fusionPose[2]*180/3.14);

            $scope.yuma.data_fusion_pose_roll[0].push($scope.yuma.fusionPose.roll);
            $scope.yuma.data_fusion_pose_roll[0].shift();
            $scope.yuma.data_fusion_pose_pitch[0].push($scope.yuma.fusionPose.pitch);
            $scope.yuma.data_fusion_pose_pitch[0].shift();
            $scope.yuma.data_fusion_pose_yaw[0].push($scope.yuma.fusionPose.yaw);
            $scope.yuma.data_fusion_pose_yaw[0].shift();

            $scope.motors = {
                motor1: data.rotation_motors[0]*data.motors[0],
                motor2: data.rotation_motors[1]*data.motors[1],
                motor3: data.rotation_motors[2]*data.motors[2],
                motor4: data.rotation_motors[3]*data.motors[3]
            };
            $scope.yuma.figureStyle1={
                  'transform':' rotateZ( '+$scope.yuma.fusionPose.roll+'deg ) '
             };
             $scope.yuma.figureStyle2={
                  'transform': 'rotateZ( '+$scope.yuma.fusionPose.pitch+'deg ) '
             };
             $scope.yuma.figureStyle3={
                  'transform': 'rotateZ( '+$scope.yuma.fusionPose.yaw+'deg )'
             };

             if($scope.yuma.fusionPose.yaw < 0){
                 $scope.yuma.compass_value  = 360+$scope.yuma.fusionPose.yaw;
             } else {
                $scope.yuma.compass_value = $scope.yuma.fusionPose.yaw;
             }

             $scope.yuma.distance = data.distance;
             $scope.yuma.data_distance[0].push($scope.yuma.distance);
             $scope.yuma.data_distance[0].shift();
             $scope.distance2 = data.distance2;
             $scope.yuma.data_distance2[0].push($scope.yuma.distance2);
             $scope.yuma.data_distance2[0].shift();

             $scope.yuma_active = true;

         });
        socket_yuma.emit('my other event', { my: 'data' });
     });

    socket_yuma.on('scan_distances_data', function (data) {
        if (data.distance == -1) {
            data.distance = 400;
            console.log('out of range');
        } else {
            var x = data.distance*-Math.sin(-data.angle*3.141592/180);
            var y = data.distance*Math.cos(-data.angle*3.141592/180);
            $scope.yuma.data_scan_distances.push({
                  x: x,
                  y: y
             });
         }
    });
    $scope.degree_target = 0;
    $scope.degreeTargetChange = function(degree_target){
        $scope.degree_target = degree_target;
    };

    $scope.pantilt_degree_target_x = 0;

    $scope.pantilt_degree_target_y = 0;

    $scope.yuma.setOnlyData = function(){
        socket_yuma.emit('task', { typeTask: 'only_data' });
        $scope.yuma.task = 1;
    };
    $scope.yuma.setAzimutZero = function(degree_target){
        socket_yuma.emit('task', { typeTask: 'azimut_zero', degree_target: degree_target});
        $scope.yuma.task = 2;
    };
    $scope.yuma.setStartAndStop = function(){
        socket_yuma.emit('task', { typeTask: 'start_and_stop' });
        $scope.yuma.task = 3;
    };
    $scope.yuma.setScanDistances= function(){
        socket_yuma.emit('task', { typeTask: 'scan_distances' });
        $scope.yuma.task = 4;
    };
    $scope.yuma.setPantiltOrientation = function(pantilt_degree_target_x,pantilt_degree_target_y){
        socket_yuma.emit('task', { typeTask: 'pantilt_orientation', pantilt_degree_target_x: pantilt_degree_target_x,pantilt_degree_target_y:pantilt_degree_target_y});
        $scope.yuma.task = 5;
    }
    $scope.yuma.setPantiltFollowOrientation = function(){

        socket_yuma.emit('task', { typeTask: 'pantilt_follow_orientation', degree_target: $scope.yuma.fusionPose.yaw});
        $scope.yuma.task = 6;
    }
    $scope.yuma.setYesOrNo = function(){
        socket_yuma.emit('task', { typeTask: 'yes_or_no'});
        $scope.yuma.task = 7;
    }
    //END YUMA CODE
    //***********************************************************************//





    //***********************************************************************//
    //Start Hector Code
    $scope.ip_address_hector = 'http://192.168.1.125';
    $scope.link_rover_hector = $scope.ip_address_hector + ':3001';
    $scope.link_stream_rover_hector = $scope.ip_address_hector + ':8081/stream.mjpg';
    $scope.hector = {};
    $scope.hector.active_control=true;

    $scope.hector.imu_flag = false;
    $scope.hector.viewImu = function() {
        $scope.hector.imu_flag = !$scope.hector.imu_flag;
    }

    $scope.hector.distance_flag = false;
    $scope.hector.viewDistance = function() {
        $scope.hector.distance_flag = !$scope.hector.distance_flag;
    }

    $scope.hector.fusion_flag = false;
    $scope.hector.viewFusion = function() {
        $scope.hector.fusion_flag = !$scope.hector.fusion_flag;
    }

    $scope.hector.data_distance = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_distance2 = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];

    $scope.hector.data_accelerometer_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_accelerometer_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_accelerometer_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_gyroscope_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_gyroscope_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_gyroscope_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_compass_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_compass_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_compass_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_fusion_pose_roll = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_fusion_pose_pitch = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
    $scope.hector.data_fusion_pose_yaw = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];

    $scope.hector.fusionPose = {};
    $scope.hector.timer = 0;


    var socket_hector = io.connect($scope.link_rover_hector);
    $scope.hector_active= false;

    socket_hector.on("reconnect_attempt", function(){
        console.log(':(');
        $scope.hector_active = false;
    });
    socket_hector.on("disconnect", function(){
        $scope.hector_active = false;
    });

    socket_hector.on('news', function (data) {
        $scope.$apply(function(){
            $scope.accelerometer = {
              ax: data.accel[0],
              ay: data.accel[1],
              az: data.accel[2]
            };
            $scope.hector.data_accelerometer_x[0].push($scope.accelerometer.ax);
            $scope.hector.data_accelerometer_x[0].shift();
            $scope.hector.data_accelerometer_y[0].push($scope.accelerometer.ay);
            $scope.hector.data_accelerometer_y[0].shift();
            $scope.hector.data_accelerometer_z[0].push($scope.accelerometer.az-1);
            $scope.hector.data_accelerometer_z[0].shift();

            $scope.gyroscope = {
              roll: data.gyro[0],
              pitch: data.gyro[1],
              yaw: data.gyro[2]
            };
            $scope.hector.data_gyroscope_x[0].push($scope.gyroscope.roll);
            $scope.hector.data_gyroscope_x[0].shift();
            $scope.hector.data_gyroscope_y[0].push($scope.gyroscope.pitch);
            $scope.hector.data_gyroscope_y[0].shift();
            $scope.hector.data_gyroscope_z[0].push($scope.gyroscope.yaw);
            $scope.hector.data_gyroscope_z[0].shift();

            $scope.compass = {
              compass1: data.compass[0],
              compass2: data.compass[1],
              compass3: data.compass[2]
            };
            $scope.hector.data_compass_x[0].push($scope.compass.compass1);
            $scope.hector.data_compass_x[0].shift();
            $scope.hector.data_compass_y[0].push($scope.compass.compass2);
            $scope.hector.data_compass_y[0].shift();
            $scope.hector.data_compass_z[0].push($scope.compass.compass3);
            $scope.hector.data_compass_z[0].shift();


            $scope.hector.fusionPose.roll = (data.fusionPose[0]*180/3.14);
            $scope.hector.fusionPose.pitch = (data.fusionPose[1]*180/3.14);
            if (data.fusionPose[2] >= -3.14159/2) {
                data.fusionPose[2] = data.fusionPose[2] - 3.14159/2
            } else {
                data.fusionPose[2] = data.fusionPose[2] + 3.14159*3/2
            }
            $scope.hector.fusionPose.yaw = (data.fusionPose[2]*180/3.14);

            $scope.hector.data_fusion_pose_roll[0].push($scope.hector.fusionPose.roll);
            $scope.hector.data_fusion_pose_roll[0].shift();
            $scope.hector.data_fusion_pose_pitch[0].push($scope.hector.fusionPose.pitch);
            $scope.hector.data_fusion_pose_pitch[0].shift();
            $scope.hector.data_fusion_pose_yaw[0].push($scope.hector.fusionPose.yaw);
            $scope.hector.data_fusion_pose_yaw[0].shift();

            $scope.motors = {
                motor1: data.rotation_motors[0]*data.motors[0],
                motor2: data.rotation_motors[1]*data.motors[1],
                motor3: data.rotation_motors[2]*data.motors[2],
                motor4: data.rotation_motors[3]*data.motors[3]
            };
            $scope.hector.figureStyle1={
                  'transform':' rotateZ( '+$scope.hector.fusionPose.roll+'deg ) '
             };
             $scope.hector.figureStyle2={
                  'transform': 'rotateZ( '+$scope.hector.fusionPose.pitch+'deg ) '
             };
             $scope.hector.figureStyle3={
                  'transform': 'rotateZ( '+$scope.hector.fusionPose.yaw+'deg )'
             };

             if($scope.hector.fusionPose.yaw < 0){
                $scope.hector.compass_value  = 360+$scope.hector.fusionPose.yaw;
             } else {
                $scope.hector.compass_value = $scope.hector.fusionPose.yaw;
             }
             $scope.hector.distance = data.distance;
             $scope.hector.data_distance[0].push($scope.hector.distance);
             $scope.hector.data_distance[0].shift();
             $scope.hector.distance2 = data.distance2;
             $scope.hector.data_distance2[0].push($scope.hector.distance2);
             $scope.hector.data_distance2[0].shift();
             $scope.hector_active = true;

         });
        socket_hector.emit('my other event', { my: 'data' });
     });
    socket_hector.on('scan_distances_data', function (data) {
        if (data.distance == -1) {
            data.distance = 400;
            console.log('out of range');
        } else {
            var x = data.distance*-Math.sin(-data.angle*3.141592/180);
            var y = data.distance*Math.cos(-data.angle*3.141592/180);
            $scope.hector.data_scan_distances.push({
                  x: x,
                  y: y
             });
         }
    });
    $scope.degree_target = 0;
    $scope.degreeTargetChange = function(degree_target){
        $scope.degree_target = degree_target;
    };

    $scope.pantilt_degree_target_x = 0;

    $scope.pantilt_degree_target_y = 0;

    $scope.openHectorScanDistancesModal = function(ev) {
      $scope.hector.data_scan_distances = [];
      $scope.setScanDistances();
      $mdDialog.show({
        controller: 'ScanDistancesController',
        templateUrl: 'views/pages/scan_distances/scan_distances_hector_view.html',
        parent: angular.element(document.body),
        scope: this,
        targetEvent: ev,
        preserveScope: true,
        clickOutsideToClose:true,
        fullscreen: false // Only for -xs, -sm breakpoints.
      })
      .then(function(answer) {
        $scope.status = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.status = 'You cancelled the dialog.';
      });
    };


    $scope.hector.setOnlyData = function(){
        socket_hector.emit('task', { typeTask: 'only_data' });
        $scope.hector.task = 1;
    };
    $scope.hector.setAzimutZero = function(degree_target){
        socket_hector.emit('task', { typeTask: 'azimut_zero', degree_target: degree_target});
        $scope.hector.task = 2;
    };
    $scope.hector.setStartAndStop = function(){
        socket_hector.emit('task', { typeTask: 'start_and_stop' });
        $scope.hector.task = 3;
    };
    $scope.hector.setScanDistances= function(){
        socket_hector.emit('task', { typeTask: 'scan_distances' });
        $scope.hector.openScanDistancesModal();
        $scope.hector.task = 4;
    };
    $scope.hector.setPantiltOrientation = function(pantilt_degree_target_x,pantilt_degree_target_y){
        socket_hector.emit('task', { typeTask: 'pantilt_orientation', pantilt_degree_target_x: pantilt_degree_target_x,pantilt_degree_target_y:pantilt_degree_target_y});
        $scope.hector.task = 5;
    }
    $scope.hector.setPantiltFollowOrientation = function(){
        socket_hector.emit('task', { typeTask: 'pantilt_follow_orientation', degree_target: $scope.hector.fusionPose.yaw});
        $scope.hector.task = 6;
    }
    $scope.hector.setYesOrNo = function(){
        socket_hector.emit('task', { typeTask: 'yes_or_no'});
        $scope.hector.task = 7;
    }
    $scope.hector.setRoam= function(){
        socket_hector.emit('task', { typeTask: 'roam', degree_target: $scope.hector.fusionPose.yaw});
        $scope.hector.task = 8;
    }
    $scope.hector.setTask9 = function(){
        socket_hector.emit('task', { typeTask: 'name_task_9', degree_target: $scope.hector.fusionPose.yaw});
        $scope.hector.task = 9;
    }
    //END Hector CODE
    //***********************************************************************//



    //Start both CODE
    //***********************************************************************//

    $scope.setOnlyData = function(){
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'only_data' });
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'only_data' });
        }
        $scope.task = 1;
    };
    $scope.setAzimutZero = function(degree_target){
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'azimut_zero', degree_target: degree_target});
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'azimut_zero', degree_target: degree_target});
        }
        $scope.task = 2;
    };
    $scope.setStartAndStop = function(){
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'start_and_stop' });
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'start_and_stop' });
        }
        $scope.task = 3;
    };
    $scope.setScanDistances= function(){
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'scan_distances' });
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'scan_distances' });
        }
        $scope.task = 4;
    };
    $scope.setPantiltOrientation = function(pantilt_degree_target_x,pantilt_degree_target_y){
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'pantilt_orientation', pantilt_degree_target_x: pantilt_degree_target_x,pantilt_degree_target_y:pantilt_degree_target_y});
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'pantilt_orientation', pantilt_degree_target_x: pantilt_degree_target_x,pantilt_degree_target_y:pantilt_degree_target_y});
        }
        $scope.task = 5;
    }
    $scope.setYoN= function(){
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'yes_or_no'});
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'yes_or_no' });
        }
        $scope.task = 7;
    };
    $scope.setYes= function(){
        console.log('10');
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'yes'});
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'yes' });
        }
        $scope.task = 10;
    };
    $scope.setNo= function(){
        console.log('11');
        if ($scope.yuma.active_control) {
            socket_yuma.emit('task', { typeTask: 'no'});
        }
        if ($scope.hector.active_control) {
            socket_hector.emit('task', { typeTask: 'no' });
        }
        $scope.task = 11;
    };

});
