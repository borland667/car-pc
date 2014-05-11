angular.module('carPc', [
    'ngResource'
    'ngSanitize'
    'ngRoute'
    'ngAnimate'
])

.config ($routeProvider) ->
  $routeProvider
  .when('/',
      templateUrl: '/static/core/scripts/controllers/main.html'
      controller: 'MainCtrl'
      label: 'Главная'
    )

  .otherwise(redirectTo: '/')


.run ($location, $rootScope) ->
    $rootScope.$on '$routeChangeSuccess', (event, current, previous) ->
        $rootScope.title = current.$$route?.label or ''