from django.contrib import admin
from django.contrib.admin import register

from accounts.models.account import Account
from accounts.models.card import CreditCardModel
from accounts.models.country import *
from accounts.models.code import *
from accounts.models.otp import *


class CountryAdmin(admin.ModelAdmin):
    pass


class AccountsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountsAdmin)
admin.site.register(CreditCardModel, AccountsAdmin)

admin.site.register(CountryModel, CountryAdmin)
admin.site.register(ProvinceModel, CountryAdmin)
admin.site.register(DistrictModel, CountryAdmin)

admin.site.register(CodeModel)


@register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'otp', 'created_at', 'is_active')
