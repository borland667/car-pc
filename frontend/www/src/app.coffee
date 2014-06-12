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
            templateUrl: 'templates/menu.html'
        })

        $stateProvider.state('app.player', {
            url: '/player'
            views:
                menuContent:
                    templateUrl: 'templates/player/player.html'
                    controller: 'PlayerCtrl'
        })
        $stateProvider.state('app.browse', {
            url: '/browse?path'
            views:
                menuContent:
                    templateUrl: 'templates/player/browse.html'
                    controller: 'BrowseCtrl'
        })

        $stateProvider.state('app.settings', {
            url: '/settings'
            views:
                menuContent:
                    templateUrl: 'templates/settings.html'
                    controller: 'SettingsCtrl'
        })

        $urlRouterProvider.otherwise('/app/player')

        return

    .config ($httpProvider) ->
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'