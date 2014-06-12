angular.module('carPc')
    .controller 'BrowseCtrl', ($scope, $interval, player) ->
        $scope.title = 'Browse'