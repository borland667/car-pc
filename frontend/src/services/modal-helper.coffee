angular.module('carPc')
    .service 'modalHelper', ($rootScope, $ionicModal, $timeout) ->
        this.show = (title, content) ->
            _modal = undefined

            modalScope = $rootScope.$new(true)
            modalScope.title = title
            modalScope.message = content

            modalPromise = $ionicModal.fromTemplateUrl('src/services/modal-helper.html', {
                scope: modalScope
                animation: 'slide-in-up'
            })

            modalPromise.then((modal) ->
                _modal = modal
                _modal.show()
            )

            unbindHidden = modalScope.$on 'modal.hidden', ->
                $timeout(
                    ->
                        _modal.remove()
                        modalScope.$destroy()
                    100
                )
                unbindHidden()

        return