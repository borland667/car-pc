angular.module('carPc')
    .controller 'SettingsVideoCtrl', ($scope, $ionicLoading, $timeout, httpHelper, video) ->
        # load devices info
        loadDevices = (isFirst) ->
            if isFirst
                $ionicLoading.show({template: 'Loading...'})

            video.getDevices().then(
                (devices) ->
                    $ionicLoading.hide()
                    $scope.devices = devices
                (response) ->
                    $ionicLoading.hide()
                    httpHelper.loadFailAlert(response)
            )
        loadDevices(true)

        $scope.changeUses = (device) ->
            $timeout(
                ->
                    video.setDevicesUses(device.id, device.is_uses).then(
                        -> loadDevices()
                        httpHelper.loadFailAlert
                    )
                100
            )

        $scope.changeResolution = (device) ->
            video.setDevicesResolution(device.id, device.resolution).then(
                -> loadDevices()
                httpHelper.loadFailAlert
            )


