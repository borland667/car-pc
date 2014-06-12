angular.module('carPc')
    .controller 'BrowseCtrl', ($scope, $timeout, $location, $anchorScroll, player, $stateParams, $state) ->
        path = $stateParams.path
        $scope.content = []
        $scope.parent = undefined
        $scope.current = undefined
        $scope.loaded = false

        $scope.load = ->
            player.browse(path).then (items) ->
                $scope.loaded = true
                for item in items
                    if item.name == '..'
                        if path
                            $scope.parent = item

                        parts = item.path.split('/')
                        name = parts[parts.length - 2]
                        $scope.current = {
                            name: name
                            type: item.type
                            path: item.path.substr(0, item.path.length - 3)
                            uri: item.uri.substr(0, item.uri.length - 3)
                        }
                    else
                        $scope.content.push(item)
        $scope.load()

        $scope.goHome = ->
            $state.go('app.browse', {path: null})

        openDir = (item) ->
            $state.go('app.browse', {path: item.path})

        playFile = (playItem) ->
            player.empty()
                .then -> player.inPlay(playItem.path)
                .then ->
                    for item in $scope.content
                        if item.type == 'file' and item.path != playItem.path
                            player.inEnqueue(item.path)

        $scope.playDir = (item) ->
            player.empty()
                .then -> player.inPlay(item.path)

        $scope.process = (item) ->
            if item.type == 'dir'
                openDir(item)
            else
                playFile(item)


