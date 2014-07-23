angular.module('carPc')
    .service 'movie', (httpHelper, SERVER_URL, $sce) ->
        this.browse = ->
            url = '/movie/browse/'
            return httpHelper.get(url).then (response) ->
                return response.data

        this.getUrl = (movieName) ->
            url = "#{ SERVER_URL }/movie/get?name=#{ movieName }"
            return $sce.trustAsResourceUrl(url)

        return