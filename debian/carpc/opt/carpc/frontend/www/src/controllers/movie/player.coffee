angular.module('carPc')
    .controller 'MoviePlayerCtrl', ($scope, $stateParams, movie) ->
        $scope.movieName = $stateParams.name
        $scope.movieUrl = movie.getUrl($scope.movieName)
        console.log $scope.movieUrl
