from django.contrib import admin
from wallet.models import WalletModel, TransferModel, VoucherModel

admin.site.register(WalletModel)
# admin.site.register(TransferModel)

@admin.register(TransferModel)
class TransferModel(admin.ModelAdmin):
    readonly_fields = ('date_created',)


admin.site.register(VoucherModel)
