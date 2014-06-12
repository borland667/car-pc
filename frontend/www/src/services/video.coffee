angular.module('carPc')
    .service 'video', (httpHelper) ->
        this.startCapture = ->
            return httpHelper.post('/video/start_capture/', {'start': 1})
        this.stopCapture = ->
            return httpHelper.post('/video/stop_capture/', {'stop': 1})

        return