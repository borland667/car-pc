angular.module('carPc')
    .controller 'MovieBrowseCtrl', ($scope, $location, movie) ->
        movie.browse().then (movies) ->
            $scope.movies = movies

        $scope.play = (movieName) ->
            $location.search('name', movieName).path("/app/movie/player")

