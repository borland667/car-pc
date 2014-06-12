angular.module('carPc')
    .controller 'MainCtrl', ($scope, toaster, SYSTEM_STATUS_UPDATE, systemStatus, video) ->

        $scope.systemStatus = systemStatus.getStatus()
        $scope.$on SYSTEM_STATUS_UPDATE, (event, status) ->
            $scope.systemStatus = status

        $scope.toggleVideo = ->
            if $scope.systemStatus.VIDEO_STARTED == '1'
                promise = video.stopCapture()
            else
                promise = video.startCapture()

            # refresh system status info
            promise.success ->
                systemStatus.loadStatus()
            promise.error (data, status, headers, config) ->
                console.log status, headers, config
                toaster.pop('error', 'Error', 'Video capturing error: ' + status)

        # load system status info
        systemStatus.loadStatus()
