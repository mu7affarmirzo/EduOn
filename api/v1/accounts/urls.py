from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('step-one/', step_one, name='step-one'),
    path('step-two/', step_two, name='step-two'),
    path('register', registration_view, name='registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('list', account_list_view, name='list'),
    path('update', update_account_view, name='update'),
    path('become-speaker', become_speaker_view, name='become-speaker'),
    path('change-password', update_password_view, name='update-password'),
    path('forgot-password', forgot_password_view, name='forgot-password'),

    path('device', DevicesListView.as_view(), name='devices'),
    path('device/<int:pk>', DevicesDetailView.as_view(), name='devices-detail'),

    path('profile', account_detail_view, name='my-profile'),
    path('speaker-profile/<int:pk>', speaker_detail_view, name='speaker-profile'),
    path('speakers-list/', speakers_list_view, name='speakers-list'),
    path('deactivate', deactivate_account_view, name='deactivate'),
]
