/* global devstudyAPP */
'use strict';
devstudyAPP.controller('ScanDistancesYumaController',
function($scope, $http, $interval, $mdDialog)  {
    setTimeout(function() {
        $scope.$apply(); //this triggers a $digest
        $scope.colors = ['#45b7cd', '#ff6384', '#ff8e72'];
        $scope.labels = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10];
        $scope.series = ['Series A', 'Series B'];

        $scope.onClick = function (points, evt) {
          console.log(points, evt);
        };
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1',fill: false, }, { yAxisID: 'y-axis-2',fill: false, }];
        $scope.options_scan_distances_modal = {
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
    }, 0);
    $scope.hide = function() {
        $mdDialog.hide();
    };

    $scope.cancel = function() {
        $mdDialog.cancel();
    };

    $scope.answer = function(answer) {
        $mdDialog.hide(answer);
    };
});
