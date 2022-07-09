from django.urls import path
from api.v1.wallet.views import info_wallet, transfer_to_wallet, CardListView, CardDetailView, history_wallet, \
    withdraw_from_wallet, VoucherListView

app_name = 'wallet'

urlpatterns = [
    path('info', info_wallet, name='info-wallet'),
    path('transfer', transfer_to_wallet, name='transfer-to-wallet'),
    path('withdraw', withdraw_from_wallet, name='withdraw-from-wallet'),
    path('history', history_wallet, name='history-of-wallet'),
    path('card', CardListView.as_view(), name='card-list'),
    path('card/<int:pk>', CardDetailView.as_view(), name='card-detail'),
    # path('vouchers', VoucherListView.as_view(), name='vouchers-list'),
]