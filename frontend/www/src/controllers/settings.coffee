angular.module('carPc')
    .controller 'SettingsCtrl', ($scope, systemStatus, video, obd) ->
        $scope.status = {
            videoCapturing: undefined
            obdCapturing: undefined
        }

        loadStatus = ->
            systemStatus.loadStatus().then (status) ->
                $scope.status.videoCapturing = status.VIDEO_STARTED == "1"
                $scope.status.obdCapturing = status.OBD_STARTED == "1"
        loadStatus()

        videoChanged = (value) ->
            if value
                p = video.startCapture()
            else
                p = video.stopCapture()
            p.then loadStatus

        obdChanged = (value) ->
            if value
                p = obd.startCapture()
            else
                p = obd.stopCapture()
            p.then loadStatus


        $scope.$watch 'status.videoCapturing', (newValue, oldValue) ->
            if oldValue != undefined
                videoChanged(newValue)

        $scope.$watch 'status.obdCapturing', (newValue, oldValue) ->
            if oldValue != undefined
                obdChanged(newValue)