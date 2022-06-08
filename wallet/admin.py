from django.contrib import admin
from wallet.models import WalletModel, TransferModel

admin.site.register(WalletModel)
admin.site.register(TransferModel)
