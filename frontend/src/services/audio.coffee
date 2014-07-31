angular.module('carPc')
    .service 'audio', (httpHelper) ->

        this.cardsList = ->
            return httpHelper.get('/audio/list_cards/').then (response) ->
                return response.data.cards

        this.getCurrentCard = ->
            return httpHelper.get('/audio/get_current/').then (response) ->
                return response.data.card_name

        this.setCurrentCard = (cardName) ->
            return httpHelper.post('/audio/set_current/', {'card_name': cardName})

        return