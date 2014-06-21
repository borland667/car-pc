angular.module('carPc')
    .controller 'MenuCtrl', ($scope, SYSTEM_STATUS_UPDATE, systemStatus, video) ->

        processStatus = (status) ->
            console.log 'system status', status
            $scope.status = status


        unbindStatus = $scope.$on SYSTEM_STATUS_UPDATE, (event, status) ->
            processStatus(status)
        $scope.$on '$destroy', -> unbindStatus()
        loadStatus = ->
            systemStatus.loadStatus().then processStatus
        loadStatus()

        $scope.toggleVideoUpload = ->
            console.log $scope.status.VIDEO_UPLOAD_STARTED
            if $scope.status.VIDEO_UPLOAD_STARTED == '1'
                video.stopUpload().then loadStatus
            else
                video.startUpload().then loadStatus