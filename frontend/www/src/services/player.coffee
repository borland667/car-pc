angular.module('carPc')
    .service 'player', (httpHelper, $interval) ->
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

        this.status = ->
            url = '/player/status/'
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


        this.volume = (value) ->
            url = '/player/volume/'
            params = {'value': value}
            return httpHelper.post(url, params)

        this._volume_stope = undefined
        this.start_volume = (value) ->
            this.stop_volume()
            this.volume(value)
            this._volume_stope = $interval(
                =>
                    this.volume(value)
                300
            )
        this.stop_volume = ->
            if this._volume_stope
                $interval.cancel(this._volume_stope)


        this.seek = (value) ->
            url = '/player/seek/'
            params = {'value': value}
            return httpHelper.post(url, params)

        this._seek_stope = undefined
        this.start_seek = (value) ->
            this.stop_seek()
            this.seek(value)
            this._seek_stope = $interval(
                =>
                    this.seek(value)
                1000
            )
        this.stop_seek = ->
            if this._seek_stope
                $interval.cancel(this._seek_stope)
        return
