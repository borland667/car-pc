angular.module('carPc')
    .controller 'ObdLastResultsCtrl', ($scope, $ionicLoading, $ionicPopup, $timeout, $cookieStore,
                                       httpHelper, obd) ->
        $scope.sensorResults = undefined
        $scope.shouldShowReorder = false
        $scope.showHidden = false

        if $cookieStore.get('ObdLastResultsCtrl.autoRefresh') == undefined
            $scope.autoRefresh = true
        else
            $scope.autoRefresh = $cookieStore.get('ObdLastResultsCtrl.autoRefresh')

        loadResults = ->
            # first load
            if $scope.sensorResults == undefined
                $ionicLoading.show({
                    template: 'Loading...'
                })

            obd.getLastResults().then(
                (results) ->
                    $ionicLoading.hide()

                    hiddenSensors = $cookieStore.get('ObdLastResultsCtrl.hiddenSensors') or {}
                    sensorsOrder = $cookieStore.get('ObdLastResultsCtrl.sensorsOrder') or []
                    haveNewIndexes = false
                    for result in results
                        # add hidden settings from cookie
                        if hiddenSensors[result.pid]
                            result.isHidden = true
                        else
                            result.isHidden = false

                        # add sort index
                        sensorIndex = sensorsOrder.indexOf(result.pid)
                        if sensorIndex == -1
                            sensorsOrder.push(result.pid)
                            sensorIndex = sensorsOrder.indexOf(result.pid)
                            haveNewIndexes = true
                        result.index = sensorIndex

                    if haveNewIndexes
                        $cookieStore.put('ObdLastResultsCtrl.sensorsOrder', sensorsOrder)

                    $scope.sensorResults = results

                    # infinitly refreshing
                    if $scope.autoRefresh and not $scope.scopeDestroied
                        $timeout(loadResults, 1000)

                (response) ->
                    $ionicLoading.hide()
                    httpHelper.loadFailAlert(response)
            )
        loadResults()

        $scope.reorderSensors = (pid, fromIndex, toIndex) ->
            sensorsOrder = $cookieStore.get('ObdLastResultsCtrl.sensorsOrder')
            pid = sensorsOrder.splice(fromIndex, 1)[0]
            sensorsOrder.splice(toIndex, 0, pid)
            $cookieStore.put('ObdLastResultsCtrl.sensorsOrder', sensorsOrder)

        $scope.hideSensor = (result) ->
            result.isHidden = true

            hiddenSensors = $cookieStore.get('ObdLastResultsCtrl.hiddenSensors') or {}
            hiddenSensors[result.pid] = 1
            $cookieStore.put('ObdLastResultsCtrl.hiddenSensors', hiddenSensors)

        $scope.showSensor = (result) ->
            result.isHidden = false

            hiddenSensors = $cookieStore.get('ObdLastResultsCtrl.hiddenSensors') or {}
            if hiddenSensors[result.pid]
                delete hiddenSensors[result.pid]
                $cookieStore.put('ObdLastResultsCtrl.hiddenSensors', hiddenSensors)

        $scope.$watch 'autoRefresh', ->
            # save setting in cookie
            $cookieStore.put('ObdLastResultsCtrl.autoRefresh', $scope.autoRefresh)
            # start infinity refreshing
            if $scope.autoRefresh
                loadResults()

        $scope.$on '$destroy', ->
            $scope.scopeDestroied = true
