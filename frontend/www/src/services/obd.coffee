angular.module('carPc')
    .service 'obd', (httpHelper) ->
        this.startCapture = ->
            return httpHelper.post('/obd/start_capture/', {'start': 1})
        this.stopCapture = ->
            return httpHelper.post('/obd/stop_capture/', {'stop': 1})

        return