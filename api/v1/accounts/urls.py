from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.accounts.views import registration_view, \
    account_list_view, \
    step_one, step_two, \
    update_account_view, \
    ChangePasswordView, DevicesListView, \
    DevicesDetailView, account_detail_view, deactivate_account_view

app_name = 'accounts'

urlpatterns = [
    path('step-one/', step_one, name='step-one'),
    path('step-two/', step_two, name='step-two'),
    path('register', registration_view, name='registration'),
    # path('login/', obtain_auth_token, name='login'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('list', account_list_view, name='list'),
    path('update', update_account_view, name='update'),
    path('change-password/<int:pk>', ChangePasswordView.as_view(), name='update'),

    path('device', DevicesListView.as_view(), name='devices'),
    path('device/<int:pk>', DevicesDetailView.as_view(), name='devices-detail'),

    path('profile', account_detail_view, name='my-profile'),
    path('deactivate', deactivate_account_view, name='deactivate'),
]
