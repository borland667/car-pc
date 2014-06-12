angular.module('carPc')
    .service 'systemStatus', ($rootScope, $cookieStore, httpHelper, SYSTEM_STATUS_UPDATE) ->

        this.setStatus = (status) ->
            # check status difference
            currentStatus = this.getStatus()
            if currentStatus and JSON.stringify(currentStatus) == JSON.stringify(status)
                return

            $cookieStore.put('systemStatus', status)
            $rootScope.$broadcast(SYSTEM_STATUS_UPDATE, status)

        this.getStatus = ->
            return $cookieStore.get('systemStatus')

        this.loadStatus = ->
            httpHelper.get('/status/system_status/').then (response) =>
                status = response.data
                this.setStatus(status)
                return status

        return