from django.conf import settings
from django.db import models


class WalletModel(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='wallet', on_delete=models.SET_NULL, blank=True, null=True)
    card_number = models.CharField(max_length=255, null=True, blank=True)
    expire = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    @property
    def phone(self):
        try:
            return str(self.owner.phone_number)
        except:
            return str('')

    def __str__(self):
        return str(self.card_number)


class TransferModel(models.Model):
    wallet = models.ForeignKey(WalletModel, on_delete=models.SET_NULL, null=True)
    amount = models.CharField(max_length=255, null=True, blank=True)
    type = models.BooleanField(default=False, null=True, blank=True)
    tr_id = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.tr_id)


class CardModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    card_number = models.CharField(max_length=255)
    expire = models.CharField(max_length=255)

    def __str__(self):
        return str(self.card_number)

    class Meta:
        unique_together = ('owner', 'card_number')


class VoucherModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    value = models.BigIntegerField(default=50000)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}- {self.value}"
