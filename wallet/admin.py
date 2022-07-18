from django.contrib import admin
from wallet.models import WalletModel, TransferModel, VoucherModel, CardModel


@admin.register(WalletModel)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('phone', 'card_number', 'expire')


@admin.register(TransferModel)
class TransferModel(admin.ModelAdmin):
    readonly_fields = ('date_created',)
    list_display = ('wallet', 'tr_id', 'date_created')


admin.site.register(VoucherModel)
admin.site.register(CardModel)
