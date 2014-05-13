angular.module('carPc', [
    'ngResource'
    'ngSanitize'
    'ngRoute'
    'ngAnimate'
    'ngCookies'

    'toaster'
])
    .config ($routeProvider) ->
        $routeProvider
            .when('/',
                templateUrl: '/static/core/scripts/controllers/main.html'
                controller: 'MainCtrl'
                label: 'Главная'
            )

            .otherwise(redirectTo: '/')

    .config ($httpProvider) ->
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

    .run ($location, $rootScope) ->
        $rootScope.$on '$routeChangeSuccess', (event, current, previous) ->
            $rootScope.title = current.$$route?.label or ''