angular.module('carPc')
    .controller 'PlayerBrowseCtrl', ($scope, $location, player) ->
        $scope.baseDir = undefined
        $scope.load = (path) ->
            player.browse(path).then (items) ->
                $scope.content = []
                $scope.current = undefined
                $scope.parent = undefined
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

                if not $scope.baseDir
                    $scope.baseDir = $scope.current




        openDir = (item) ->
            $scope.load item.path

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

        $scope.openControl = ->
            $location.path('/player/control/')

        $scope.load()