from django.urls import path
from api.v1.wallet.views import (
    info_wallet, transfer_to_wallet, CardListView,
    CardDetailView, history_wallet, withdraw_from_wallet,
    transactions_history_view, confirm_transfer_to_wallet, confirm_withdraw
)

app_name = 'wallet'

urlpatterns = [
    path('info', info_wallet, name='info-wallet'),
    path('transfer', transfer_to_wallet, name='transfer-to-wallet'),
    path('confirm-transfer', confirm_transfer_to_wallet, name='transfer-to-wallet'),
    path('withdraw', withdraw_from_wallet, name='withdraw-from-wallet'),
    path('confirm-withdraw', confirm_withdraw, name='withdraw-from-wallet'),
    path('history', history_wallet, name='history-of-wallet'),
    path('transaction-history', transactions_history_view, name='history-of-transactions'),
    path('card', CardListView.as_view(), name='card-list'),
    path('card/<int:pk>', CardDetailView.as_view(), name='card-detail'),
]