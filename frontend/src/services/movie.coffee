angular.module('carPc')
    .service 'movie', ($sce, httpHelper, config) ->
        serviceAddress = config.serviceAddress

        this.browse = ->
            url = '/movie/browse/'
            return httpHelper.get(url).then (response) ->
                return response.data

        this.getUrl = (movieName) ->
            url = "#{ serviceAddress }/movie/get?name=#{ movieName }"
            return $sce.trustAsResourceUrl(url)

        return