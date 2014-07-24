angular.module('carPc')
    .service 'systemControl', (httpHelper) ->
        this.sentToHalt = ->
            url = '/system_control/halt/'
            return httpHelper.post(url, {halt: 1})
        return