// Generated by CoffeeScript 1.6.3
(function() {
  angular.module('carPc').controller('ObdLastResultsCtrl', function($scope, $ionicLoading, $ionicPopup, httpHelper, obd) {
    var loadResults;
    $scope.sensorResults = void 0;
    loadResults = function() {
      if ($scope.sensorResults === void 0) {
        $ionicLoading.show({
          template: 'Loading...'
        });
        return obd.getLastResults().then(function(results) {
          $ionicLoading.hide();
          return $scope.sensorResults = results;
        }, function(response) {
          $ionicLoading.hide();
          return httpHelper.loadFailAlert(response);
        });
      }
    };
    return loadResults();
  });

}).call(this);
