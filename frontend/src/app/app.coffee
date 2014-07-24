angular.module('carPc', [
    'ionic'
    'ngCookies'
    'carPcConfig'
])
    .run ($ionicPlatform) ->
        $ionicPlatform.ready ->
            if window.cordova and window.cordova.plugins.Keyboard
                cordova.plugins.Keyboard.hideKeyboardAccessoryBar true
            if window.StatusBar
                StatusBar.styleDefault()

    .config ($stateProvider, $urlRouterProvider) ->
        $stateProvider.state('app', {
            url: '/app'
            abstract: true
            templateUrl: 'src/app/controllers/menu.html'
        })

        $stateProvider.state('app.player', {
            url: '/player'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/player/player.html'
                    controller: 'PlayerCtrl'
        })
        $stateProvider.state('app.browse', {
            url: '/browse?path'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/player/browse.html'
                    controller: 'PlayerBrowseCtrl'
        })

        $stateProvider.state('app.movie_browse', {
            url: '/movie'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/movie/browse.html'
                    controller: 'MovieBrowseCtrl'
        })
        $stateProvider.state('app.movie_player', {
            url: '/movie/player?name'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/movie/player.html'
                    controller: 'MoviePlayerCtrl'
        })

        $stateProvider.state('app.obd_last_results', {
            url: '/obd/last_results'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/obd/last_results.html'
                    controller: 'ObdLastResultsCtrl'
        })

        $stateProvider.state('app.settings', {
            url: '/settings'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/settings/settings.html'
                    controller: 'SettingsCtrl'
        })
        $stateProvider.state('app.settings_video', {
            url: '/settings/video'
            views:
                menuContent:
                    templateUrl: 'src/app/controllers/settings/video.html'
                    controller: 'SettingsVideoCtrl'
        })

        $urlRouterProvider.otherwise('/app/player')

        return

    .config ($httpProvider) ->
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'