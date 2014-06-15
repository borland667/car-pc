angular.module('carPc')
    .controller 'SettingsCtrl', ($scope, $ionicLoading, $ionicPopup,
                                 httpHelper, systemStatus, systemControl, video, obd) ->
        $scope.status = {
            videoCapturing: undefined
            obdCapturing: undefined
        }

        loadFail = (response) ->
            $ionicLoading.hide()
            httpHelper.loadFailAlert(response)

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


        videoChanged = (value) ->
            if value
                p = video.startCapture()
            else
                p = video.stopCapture()
            p.then loadStatus, httpHelper.loadFailAlert

        obdChanged = (value) ->
            if value
                p = obd.startCapture()
            else
                p = obd.stopCapture()
            p.then loadStatus, httpHelper.loadFailAlert


        $scope.$watch 'status.videoCapturing', (newValue, oldValue) ->
            if oldValue != undefined
                videoChanged(newValue)

        $scope.$watch 'status.obdCapturing', (newValue, oldValue) ->
            if oldValue != undefined
                obdChanged(newValue)

        $scope.haltSystem = ->
            confirmPopup = $ionicPopup.confirm({
                title: 'Swith off Car PC',
                template: 'Are you sure you want to go system to halt?'
            })
            confirmPopup.then (res) ->
                if res
                    systemControl.sentToHalt()

        loadStatus()


