angular.module('carPc')
    .controller 'PlayerControlCtrl', ($scope, player) ->
        player.playlist().then (items) ->
            console.log items
            $scope.playlist = items

        $scope.player = player
