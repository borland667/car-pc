angular.module('carPc')
    .controller 'ObdLastResultsCtrl', ($scope, $ionicLoading, $ionicPopup, httpHelper, obd) ->
        $scope.sensorResults = undefined

        loadResults = ->
            # first load
            if $scope.sensorResults == undefined
                $ionicLoading.show({
                    template: 'Loading...'
                })

                obd.getLastResults().then(
                    (results) ->
                        $ionicLoading.hide()
                        $scope.sensorResults = results
                    (response) ->
                        $ionicLoading.hide()
                        httpHelper.loadFailAlert(response)
                )
        loadResults()