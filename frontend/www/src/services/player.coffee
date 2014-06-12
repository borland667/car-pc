angular.module('carPc')
    .service 'player', (httpHelper) ->
        this.browse = (path) ->
            url = '/player/browse/'
            params = undefined
            if path
                params = {'dir': path}
            return httpHelper.get(url, params).then (response) ->
                return response.data

        this.playlist = ->
            url = '/player/playlist/'
            return httpHelper.get(url).then (response) ->
                return response.data

        this.inPlay = (path) ->
            url = '/player/in_play/'
            params = {'input': path}
            return httpHelper.post(url, params)

        this.play = (id) ->
            url = '/player/play/'
            params = {'id': id}
            return httpHelper.post(url, params)

        this.pause = ->
            url = '/player/pause/'
            return httpHelper.post(url)

        this.stop = ->
            url = '/player/stop/'
            return httpHelper.post(url)

        this.next = ->
            url = '/player/next/'
            return httpHelper.post(url)

        this.previous = ->
            url = '/player/previous/'
            return httpHelper.post(url)

        this.inEnqueue = (path) ->
            url = '/player/in_enqueue/'
            params = {'input': path}
            return httpHelper.post(url, params)

        this.empty = ->
            url = '/player/empty/'
            return httpHelper.post(url)

        return
