from django.urls import path, include
from .views import (AccountRegistrationView,
                    SearchListView,
                    AccountView,
                    # list_api,
                    send_mail_for_verification,
                    check_code_for_verification,
                    AccountListView)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# router.register('func', AccountView, basename='account_func')
router.register('register', AccountRegistrationView)

urlpatterns = [
    path('account', include(router.urls)),
    path('account/list', AccountListView.as_view()),

    path('search', SearchListView.as_view(), name='search'),
    path('verification', send_mail_for_verification),
    path('check_code', check_code_for_verification),
    path('account/<int:pk>', AccountView.as_view())
]