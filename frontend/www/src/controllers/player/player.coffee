angular.module('carPc')
    .controller 'PlayerCtrl', ($scope, $interval, $timeout, player, $ionicScrollDelegate) ->
        $scope.player = player
        player.playlist().then (items) ->
            $scope.playlist = items

        $scope.status = {}
        loadStatus = ->
            player.status().then (status) ->
                $scope.status = status
                $scope.position = Math.floor(status.position * 100)
        loadStatus()
        statusRefreshStopper = $interval(loadStatus, 500)
        $scope.$on '$destroy', ->
            $interval.cancel(statusRefreshStopper)

        # on track changing, scroll list
        $scope.$watch 'status.title', ->
            if not $scope.playlist or not $scope.status
                return

            # find playing element
            index = undefined
            $.each $scope.playlist, (i, item) ->
                if item.name == $scope.status.title and item.duration_sec == $scope.status.length
                    index = i

            if index != undefined
                listPosition = $ionicScrollDelegate.getScrollPosition().top
                itemPosition = $("#item_#{ index }").position().top
                # if item not in visible zone, scroll list
                if not (listPosition + 50  > itemPosition) or not (listPosition + 200  < itemPosition)
                    $ionicScrollDelegate.scrollTo(0, itemPosition, true)


