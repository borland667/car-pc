angular.module('carPc', [
    'ionic'
    'ngCookies'
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
            templateUrl: 'src/controllers/menu.html'
        })

        $stateProvider.state('app.player', {
            url: '/player'
            views:
                menuContent:
                    templateUrl: 'src/controllers/player/player.html'
                    controller: 'PlayerCtrl'
        })
        $stateProvider.state('app.browse', {
            url: '/browse?path'
            views:
                menuContent:
                    templateUrl: 'src/controllers/player/browse.html'
                    controller: 'BrowseCtrl'
        })

        $stateProvider.state('app.settings', {
            url: '/settings'
            views:
                menuContent:
                    templateUrl: 'src/controllers/settings.html'
                    controller: 'SettingsCtrl'
        })

        $urlRouterProvider.otherwise('/app/player')

        return

    .config ($httpProvider) ->
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'