angular.module('carPc')
    .controller 'SettingsCtrl', ($scope, $ionicLoading,
                                 modalHelper, systemStatus, video, obd) ->
        $scope.status = {
            videoCapturing: undefined
            obdCapturing: undefined
        }

        loadStatus = ->
            # for first load
            if $scope.status.videoCapturing == undefined and $scope.status.obdCapturing == undefined
                $ionicLoading.show({
                    template: 'Loading...'
                })

            systemStatus.loadStatus().then(
                (status) ->
                    $ionicLoading.hide()
                    $scope.status.videoCapturing = status.VIDEO_STARTED == "1"
                    $scope.status.obdCapturing = status.OBD_STARTED == "1"
                loadFail
            )
        loadStatus()

        loadFail = (response) ->
            $ionicLoading.hide()
            console.error 'loadFail!', response
            modalHelper.show('Load Error', "Response status: #{ response.status }")

        videoChanged = (value) ->
            if value
                p = video.startCapture()
            else
                p = video.stopCapture()
            p.then loadStatus, loadFail

        obdChanged = (value) ->
            if value
                p = obd.startCapture()
            else
                p = obd.stopCapture()
            p.then loadStatus, loadFail


        $scope.$watch 'status.videoCapturing', (newValue, oldValue) ->
            if oldValue != undefined
                videoChanged(newValue)

        $scope.$watch 'status.obdCapturing', (newValue, oldValue) ->
            if oldValue != undefined
                obdChanged(newValue)