angular.module('carPc')
    .service 'video', (httpHelper) ->
        this.startCapture = ->
            return httpHelper.post('/video/start_capture/', {'start': 1})
        this.stopCapture = ->
            return httpHelper.post('/video/stop_capture/', {'stop': 1})

        this.getDevices = ->
            return httpHelper.get('/video/devices/').then (response) ->
                return response.data

        this.setDevicesUses = (id, is_uses) ->
            if is_uses
                params = {is_uses: 1}
            else
                params = {is_uses: 0}
            return httpHelper.post("/video/devices/#{ id }/uses/", params)

        this.setDevicesResolution = (id, resolution) ->
            params = {resolution: resolution}
            return httpHelper.post("/video/devices/#{ id }/resolution/", params)

        return