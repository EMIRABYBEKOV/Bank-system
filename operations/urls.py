from django.urls import path, include
from .views import CreateWallet, ChangeCurrency, TransferView, TakeCreditView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('credit', TakeCreditView, basename='credit')


urlpatterns = [
    path('wallet/create', CreateWallet.as_view({'post': 'create'})),
    path('wallet/get', CreateWallet.as_view({'get': 'get'})),
    path('wallet/change/currency', ChangeCurrency.as_view({'post': 'post'})),
    path('transfer', TransferView.as_view({'post': 'post'})),
    path('', include(router.urls)),

    # path('credit/<int:identification_number>', TakeCreditView.as_view())

]