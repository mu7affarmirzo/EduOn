from django.urls import path, include
from api.v1.accounts.views import hi, registration_view, account_list_view

app_name = 'accounts'

urlpatterns = [
    path('hi', hi, name='hi'),
    path('register', registration_view, name='registration'),
    path('list', account_list_view, name='list'),
]
