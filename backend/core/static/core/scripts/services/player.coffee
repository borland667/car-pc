angular.module('carPc')
    .service 'player', ($http) ->
        this.browse = (path) ->
            url = '/player/browse/?'
            if path
                url += $.param({'dir': path})
            return $http.get(url).then (response) ->
                return response.data

        this.playlist = ->
            url = '/player/playlist/'
            return $http.get(url).then (response) ->
                return response.data

        this.inPlay = (path) ->
            url = '/player/in_play/'
            params = $.param({'input': path})
            return $http.post(url, params)

        this.play = (id) ->
            url = '/player/play/'
            params = $.param({'id': id})
            return $http.post(url, params)

        this.pause = ->
            url = '/player/pause/'
            return $http.post(url)

        this.stop = ->
            url = '/player/stop/'
            return $http.post(url)

        this.next = ->
            url = '/player/next/'
            return $http.post(url)

        this.previous = ->
            url = '/player/previous/'
            return $http.post(url)

        this.inEnqueue = (path) ->
            url = '/player/in_enqueue/'
            params = $.param({'input': path})
            return $http.post(url, params)

        this.empty = ->
            url = '/player/empty/'
            return $http.post(url)

        return
