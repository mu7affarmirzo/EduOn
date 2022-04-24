from django.urls import path
from api.v1.accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('hi', hi, name='hi'),
    path('register', registration_view, name='registration'),
    path('list', account_list_view, name='list'),
    path('sms-verification', sms_verification_view, name='sms-verification'),
    path('complete-reg', complete_registration_view, name='complete_registration_view'),
]
