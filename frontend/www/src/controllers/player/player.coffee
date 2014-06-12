angular.module('carPc')
    .controller 'PlayerCtrl', ($scope, $interval, player) ->
        $scope.player = player
        player.playlist().then (items) ->
            $scope.playlist = items

        loadStatus = ->
            player.status().then (status) ->
                $scope.status = status
                $scope.position = Math.floor(status.position * 100)
        loadStatus()
        statusRefreshStopper = $interval(loadStatus, 500)
        $scope.$on '$destroy', ->
            $interval.cancel(statusRefreshStopper)