angular.module('carPc')
    .controller 'MainCtrl', ($scope, toaster, SYSTEM_STATUS_UPDATE, SystemStatus, Video) ->

        $scope.systemStatus = SystemStatus.getStatus()
        $scope.$on SYSTEM_STATUS_UPDATE, (event, status) ->
            $scope.systemStatus = status

        $scope.toggleVideo = ->
            if $scope.systemStatus.VIDEO_STARTED == '1'
                promise = Video.stopCapture()
            else
                promise = Video.startCapture()

            # refresh system status info
            promise.success ->
                SystemStatus.loadStatus()
            promise.error (data, status, headers, config) ->
                console.log status, headers, config
                toaster.pop('error', 'Error', 'Video capturing error: ' + status)

        # load system status info
        SystemStatus.loadStatus()
