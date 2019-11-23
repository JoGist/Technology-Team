devstudyAPP.directive("showOnceBackgroundLoaded", [function () {
  return {
    restrict: "A",
    scope: false,
    link: function (scope, element, attributes) {
		//element.addClass("ng-hide");
		var image = new Image();
		image.onload = function () {
			// the image must have been cached by the browser, so it should load quickly
			scope.$apply(function () {
			  element.css({ backgroundImage: 'url("' + attributes.showOnceBackgroundLoaded + '")' });
			 // element.removeClass("ng-hide");
			});
		};
		image.src = attributes.showOnceBackgroundLoaded;
		if (attributes.showOnceBackgroundLoaded2) {
			var image2 = new Image();
			image2.onload = function () {
				// the image must have been cached by the browser, so it should load quickly
				scope.$apply(function () {
				  element.css({ backgroundImage: 'url("' + attributes.showOnceBackgroundLoaded2 + '")' });
				 // element.removeClass("ng-hide");
				});
			};
			image2.src = attributes.showOnceBackgroundLoaded2;
		}
    }
  };
}]);

devstudyAPP.directive('myDirective', function($compile) {
  return {
    restrict: 'E',
    scope: {
      ngModel: '='
    },
    template: '<div class="some">' +
      '<input style="border-style: inset; border-width: 0; border-radius:10px; width: 29px; background:#FB9E5F; color:white; position: absolute; top: 2;right: 10px; margin: 8px" id="{{id}}" ng-model="value"></div>',
    replace: true,
    require: 'ngModel',
    link: function($scope, elem, attr, ctrl) {
      $scope.label = attr.ngModel;
      $scope.id = attr.ngModel;
      console.debug(attr.ngModel);
      console.debug($scope.$parent.$eval(attr.ngModel));
      var textField = $('input', elem).
        attr('ng-model', attr.ngModel).
        val($scope.$parent.$eval(attr.ngModel));

      $compile(textField)($scope.$parent);
    }
  };
});

devstudyAPP.directive('boxInput', function($compile) {
  return {
    restrict: 'E',
    scope: {
      ngModel: '='
    },
    template: '<div class="some">' +
      '<input style="border-style: double; border-width: 1; border-color: #FFF; border-radius:10px;     width: -webkit-fill-available; padding: 0 5; background:#FB9E5F; color:#FFF; top: 2;right: 10px;" id="{{id}}" ng-model="value"></div>',
    replace: true,
    require: 'ngModel',
    link: function($scope, elem, attr, ctrl) {
      $scope.label = attr.ngModel;
      $scope.id = attr.ngModel;
      console.debug(attr.ngModel);
      console.debug($scope.$parent.$eval(attr.ngModel));
      var textField = $('input', elem).
        attr('ng-model', attr.ngModel).
        val($scope.$parent.$eval(attr.ngModel));

      $compile(textField)($scope.$parent);
    }
  };
});

devstudyAPP.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if (event.which === 13) {
                scope.$apply(function () {
                    scope.$eval(attrs.ngEnter);
                });
                event.preventDefault();
            }
        });
    };
})

devstudyAPP.directive('tchOlMap', function ($timeout) {

        var MAP_DOM_ELEMENT_ID = 'tchMap';

        return {
            restrict: 'E',
            scope: {
              val: '='
            },
            replace: true,
            template: '<div id="' + MAP_DOM_ELEMENT_ID + '" class="full-height"></div>',
            link: function postLink(scope, element, attrs, ngModel) {
                var map = new OpenLayers.Map(MAP_DOM_ELEMENT_ID);
                map.addLayer(new OpenLayers.Layer.OSM());
                map.setCenter(new OpenLayers.LonLat(12.57805556, 41.88166667).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 18);
                var markers = new OpenLayers.Layer.Markers( "Markers" );
                var position = new OpenLayers.Layer.Markers( "Position" );
                var size = new OpenLayers.Size(5,5);
                var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
                var size_position = new OpenLayers.Size(15,15);
                var offset_position = new OpenLayers.Pixel(-7, -15);
                var icon = new OpenLayers.Icon('/imgs/point.png', size, offset);
                var icon_position = new OpenLayers.Icon('/imgs/marker.png', size_position, offset_position);
                var lat = 41.88166667;
                var lon = 12.57805556;
                coordinates = {lat:41+52.9122/60,lon:12+34.6849/60};
                // console.log(coordinates);
                markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(coordinates.lon,coordinates.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")),icon));
                positionMarker = new OpenLayers.Marker(new OpenLayers.LonLat(coordinates.lon,coordinates.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")),icon_position)
                position.addMarker(positionMarker);
                coors = scope.val.coors;
                // for(var k=0;k<coors.length;k++){
                //     coordinates = coors[k];
                //     markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(coordinates.lon,coordinates.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")),icon.clone()));
                // // markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(12.34,41.529).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")),icon.clone()));
                // }
                map.addLayer(position);
                // map.on('click', function(evt){
                //     console.log(ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326'));
                // });
                console.log(map);
                scope.$watch('val', function(newValue, oldValue) {
                    if (newValue && newValue.position && newValue.position.lat && newValue.position.lon)
                        // console.log(markers.markers);
                        markers.addMarker(new OpenLayers.Marker(new OpenLayers.LonLat(newValue.position.lon,newValue.position.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")),icon.clone()));

                        position.removeMarker(positionMarker);
                        positionMarker = new OpenLayers.Marker(new OpenLayers.LonLat(newValue.position.lon,newValue.position.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")),icon_position.clone())
                        position.addMarker(positionMarker);
                        map.addLayer(markers);
                        map.addLayer(position);
                    }, true);
                // console.log(scope);
            }
        }

    });
