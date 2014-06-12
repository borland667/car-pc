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
                label: 'Main'
            )

            .when('/player/control/',
                templateUrl: '/static/core/scripts/controllers/player/control.html'
                controller: 'PlayerControlCtrl'
                label: 'Player'
            )
            .when('/player/browse/',
                templateUrl: '/static/core/scripts/controllers/player/browse.html'
                controller: 'PlayerBrowseCtrl'
                label: 'Browse'
            )

            .otherwise(redirectTo: '/')

    .config ($httpProvider) ->
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'

    .run ($location, $rootScope) ->
        $rootScope.$on '$routeChangeSuccess', (event, current, previous) ->
            $rootScope.title = current.$$route?.label or ''