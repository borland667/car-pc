angular.module('carPc')
    .service 'httpHelper', ($http, SERVER_URL) ->
        this.get = (url, params) ->
            encodeParams = encodeQueryData(params)
            urlWithParams = "#{ SERVER_URL }#{ url }?#{encodeParams}"
            return $http.get(urlWithParams)

        this.post = (url, params) ->
            djangoParams = undefined
            if params
                djangoParams = $.param(params)
            return $http.post("#{ SERVER_URL }#{ url }", djangoParams)

        return