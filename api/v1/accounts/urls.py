from django.urls import path
from api.v1.accounts.views import registration_view, account_list_view

app_name = 'accounts'

urlpatterns = [
    path('register', registration_view, name='registration'),
    path('list', account_list_view, name='list'),
]
