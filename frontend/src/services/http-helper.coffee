angular.module('carPc')
    .service 'httpHelper', ($http, $ionicPopup, config) ->
        serviceAddress = config.serviceAddress

        this.get = (url, params) ->
            encodeParams = encodeQueryData(params)
            urlWithParams = "#{ serviceAddress }#{ url }?#{encodeParams}"
            return $http.get(urlWithParams)

        this.post = (url, params) ->
            djangoParams = undefined
            if params
                djangoParams = $.param(params)
            return $http.post("#{ serviceAddress }#{ url }", djangoParams)

        this.loadFailAlert = (response) ->
            msg = response?.status or 'Error'
            alertPromise = $ionicPopup.alert({
                title: 'Load Error'
                template: "Response status: #{ msg }"
            })
            return alertPromise

        return