/* global devstudyAPP */
'use strict';
// 41.893549, 12.493280
// 41.893925, 12.493009
devstudyAPP.controller('MonitoringHectorController',
function($scope, $http, $interval, $mdDialog) {
    $scope.ip_address = 'http://172.20.10.7';
    $scope.linkRover = $scope.ip_address + ':3001';
    $scope.linkStreamRover = $scope.ip_address + ':8081/stream.mjpg';

    $scope.link = false;

    $scope.imu_flag = false;
    $scope.viewImu = function() {
        $scope.imu_flag = !$scope.imu_flag;
    }
    $scope.viewMap = function() {
        $scope.map_flag = !$scope.map_flag;
    }
    $scope.distance_flag = false;
    $scope.viewDistance = function() {
        $scope.distance_flag = !$scope.distance_flag;
    }

    $scope.fusion_flag = false;
    $scope.viewFusion = function() {
        $scope.fusion_flag = !$scope.fusion_flag;
    }

  $scope.status = '  ';
  $scope.customFullscreen = true;

  $scope.data_scan_distances = [{x: 0,y: 10}, {x: 5,y: 12}, {x: 10,y: 5}, {x: 15,y: -5},{x: 10,y: -1},{x: 5,y: -1},{x: 0,y: -10},
                                {x: -5,y: -1},{x: -10,y: -1},{x: -15,y: 1},{x: -10,y: 4},{x: -5,y: 10},{x: 0,y: 10}];

  $scope.openScanDistancesModal = function(ev) {
    $scope.data_scan_distances = [{
    }];
    $scope.setScanDistances();
    $mdDialog.show({
      controller: 'ScanDistancesController',
      templateUrl: 'views/pages/scan_distances_view.html',
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


    setTimeout(function() {
        $scope.$apply(); //this triggers a $digest
        $scope.colors = ['#45b7cd', '#ff6384', '#ff8e72'];
        $scope.labels = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10];
        $scope.series = ['Series A', 'Series B'];
        $scope.data_distance = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_distance2 = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.onClick = function (points, evt) {
          console.log(points, evt);
        };
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.optionslol = {
          scales: {
            xAxes: [
                {
                  id: 'x-axis-1',
                  type: 'linear',
                  display: true,
                  ticks: {min: -250, max:250}
                }
              ],
            yAxes: [
              {
                id: 'y-axis-1',
                type: 'linear',
                display: true,
                ticks: {min: -250, max:250}
              }
            ]
          }
        };
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

        $scope.data_accelerometer_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_accelerometer_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_accelerometer_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_gyroscope_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_gyroscope_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_gyroscope_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_compass_x = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_compass_y = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_compass_z = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_fusion_pose_roll = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_fusion_pose_pitch = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];
        $scope.data_fusion_pose_yaw = [[65, 59, 80, 81, 56, 55, 40, 65, 59, 80]];

    }, 0);
    $scope.fusionPose = {};
    $scope.mapData = {
        coors: [],
        position:{},
        target:{}
    };
    $scope.timer = 0;

    var socket = io.connect($scope.linkRover);

    socket.on("reconnect_attempt", function(){
        console.log(':(');
        $scope.link = false;
    });
    socket.on("disconnect", function(){
        console.log(':(');
        $scope.link = false;
    });

    socket.on('news', function (data) {
        $scope.$apply(function(){
            $scope.mapData.position.lat = data.gps.latitude;
            $scope.mapData.position.lon = data.gps.longitude;

            $scope.accelerometer = {
              ax: data.accel[0],
              ay: data.accel[1],
              az: data.accel[2]
            };
            $scope.data_accelerometer_x[0].push($scope.accelerometer.ax);
            $scope.data_accelerometer_x[0].shift();
            $scope.data_accelerometer_y[0].push($scope.accelerometer.ay);
            $scope.data_accelerometer_y[0].shift();
            $scope.data_accelerometer_z[0].push($scope.accelerometer.az-1);
            $scope.data_accelerometer_z[0].shift();

            $scope.gyroscope = {
              roll: data.gyro[0],
              pitch: data.gyro[1],
              yaw: data.gyro[2]
            };
            $scope.data_gyroscope_x[0].push($scope.gyroscope.roll);
            $scope.data_gyroscope_x[0].shift();
            $scope.data_gyroscope_y[0].push($scope.gyroscope.pitch);
            $scope.data_gyroscope_y[0].shift();
            $scope.data_gyroscope_z[0].push($scope.gyroscope.yaw);
            $scope.data_gyroscope_z[0].shift();

            $scope.compass = {
              compass1: data.compass[0],
              compass2: data.compass[1],
              compass3: data.compass[2]
            };
            $scope.data_compass_x[0].push($scope.compass.compass1);
            $scope.data_compass_x[0].shift();
            $scope.data_compass_y[0].push($scope.compass.compass2);
            $scope.data_compass_y[0].shift();
            $scope.data_compass_z[0].push($scope.compass.compass3);
            $scope.data_compass_z[0].shift();


            $scope.fusionPose.roll = (data.fusionPose[0]*180/3.14);
            $scope.fusionPose.pitch = (data.fusionPose[1]*180/3.14);
            if (data.fusionPose[2] >= -3.14159/2) {
                data.fusionPose[2] = data.fusionPose[2] - 3.14159/2
            } else {
                data.fusionPose[2] = data.fusionPose[2] + 3.14159*3/2
            }
            $scope.fusionPose.yaw = (data.fusionPose[2]*180/3.14);

            $scope.data_fusion_pose_roll[0].push($scope.fusionPose.roll);
            $scope.data_fusion_pose_roll[0].shift();
            $scope.data_fusion_pose_pitch[0].push($scope.fusionPose.pitch);
            $scope.data_fusion_pose_pitch[0].shift();
            $scope.data_fusion_pose_yaw[0].push($scope.fusionPose.yaw);
            $scope.data_fusion_pose_yaw[0].shift();

            $scope.voltage = data.voltage;

            $scope.motors = {
                motor1: data.rotation_motors[0]*data.motors[0],
                motor2: data.rotation_motors[1]*data.motors[1],
                motor3: data.rotation_motors[2]*data.motors[2],
                motor4: data.rotation_motors[3]*data.motors[3]
            };
            $scope.figureStyle1={
                  'transform':' rotateZ( '+$scope.fusionPose.roll+'deg ) '
             };
             $scope.figureStyle2={
                  'transform': 'rotateZ( '+$scope.fusionPose.pitch+'deg ) '
             };
             $scope.figureStyle3={
                  'transform': 'rotateZ( '+$scope.fusionPose.yaw+'deg )'
             };
             $scope.distance = data.distance;
             $scope.data_distance[0].push($scope.distance);
             $scope.data_distance[0].shift();
             $scope.distance2 = data.distance2;
             $scope.data_distance2[0].push($scope.distance2);
             $scope.data_distance2[0].shift();

             $scope.link = true;

         });
        socket.emit('my other event', { my: 'data' });
     });

    socket.on('scan_distances_data_by_main', function (data) {
        if (data.distance == -1) {
            data.distance = 400;
            console.log('out of range');
        } else {
            var x = data.distance*-Math.sin(-data.angle*3.141592/180);
            var y = data.distance*Math.cos(-data.angle*3.141592/180);
            $scope.data_scan_distances.push({
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

    $scope.setOnlyData = function(){
        console.log('click only data');
        socket.emit('task', { typeTask: 'only_data' });
        $scope.task = 1;
    };
    $scope.setAzimutZero = function(degree_target){
        socket.emit('task', { typeTask: 'azimut_zero', degree_target: degree_target});
        $scope.task = 2;
    };
    $scope.setStartAndStop = function(){
        socket.emit('task', { typeTask: 'start_and_stop' });
        $scope.task = 3;
    };
    $scope.setScanDistances= function(){
        socket.emit('task', { typeTask: 'scan_distances' });
        $scope.task = 4;
    };
    $scope.setOrientationPantiltAxisZ = function(degree_target){
        socket.emit('task', { typeTask: 'pantilt', degree_target: degree_target});
        $scope.task = 5;
    };

    $scope.setPantiltOrientation = function(pantilt_degree_target_x,pantilt_degree_target_y){
        socket.emit('task', { typeTask: 'pantilt_orientation', pantilt_degree_target_x: pantilt_degree_target_x,pantilt_degree_target_y:pantilt_degree_target_y});
    }

     $scope.flagMotors = false;
     $scope.mouseDownGo = function(){
         $scope.flagMotors = true;
     };
     $scope.mouseUpGo = function(){
         $scope.flagMotors = false;
     };
     $scope.key = function($event){
        if ($event.keyCode == 38){
            console.log("up arrow");
            socket.emit('command', { command: "up_arrow" });
        }else if ($event.keyCode == 39){
            console.log("right arrow");
            socket.emit('command', { command: "right_arrow" });
        }else if ($event.keyCode == 40){
            console.log("down arrow");
            socket.emit('command', { command: "down_arrow" });
        }else if ($event.keyCode == 37){
            console.log("command arrow");
            socket.emit('command', { command: "left_arrow" });
        }else if ($event.keyCode == 88){
            console.log("stop");
            socket.emit('command', { command: "stop" });
        }
    }
    var coors = [];

    $scope.latitude = 41.882409;
    $scope.longitude =12.578443;

    $scope.latTarget = 41.881728;
    $scope.lonTarget = 12.578192;

    $scope.count = 0;
    $scope.setTargetCoordinates = function(longitude,latitude){
        // console.log(longitude,latitude);
        $scope.mapData.target = {
            latitude:latitude,
            longitude:longitude
        }
        $scope.mapData.position=(coors[$scope.count]);
        $scope.count = $scope.count + 1;
        socket.emit('task', { typeTask: 'target_coordinates', longitude: longitude, latitude:latitude});
        $scope.task = 6;
    };


});
