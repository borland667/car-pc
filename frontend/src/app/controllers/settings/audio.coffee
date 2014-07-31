angular.module('carPc')
    .controller 'SettingsAudioCtrl', ($scope, $q, $ionicLoading, $timeout, httpHelper, audio) ->
        $scope.data = {
            'currentCard': ''
            'cardList': undefined
        }

        # load audio card info
        loadCards = (isFirst) ->
            if isFirst
                $ionicLoading.show({template: 'Loading...'})

            currentPromise = audio.getCurrentCard()
            currentPromise.then (cardName) ->
                $scope.data.currentCard = cardName

            listPromise = audio.cardsList()
            listPromise.then (cardList) ->
                $scope.data.cardList = (card.name for card in cardList)

            $q.all([currentPromise, listPromise]).then(
                ->
                    $ionicLoading.hide()
                ->
                    $ionicLoading.hide()
                    httpHelper.loadFailAlert()
            )
        loadCards(true)

        $scope.updateCard = ->
            $timeout(
                ->
                    audio.setCurrentCard($scope.data.currentCard).then(
                        -> loadCards()
                        httpHelper.loadFailAlert
                    )
                100
            )


