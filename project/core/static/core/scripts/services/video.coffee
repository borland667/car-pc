angular.module('carPc')
    .service 'Video', ($http) ->
        this.startCapture = ->
            params = $.param({'start': 1})
            return $http.post('/video/start_capture/', params)
        this.stopCapture = ->
            params = $.param({'stop': 1})
            return $http.post('/video/stop_capture/', params)

        return