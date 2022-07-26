import enum
from datetime import date

from django.db import models

from accounts.models.account import Account
from accounts.exceptions.models import ExpiredDateException


def validate_expire_date(value):
    if value < date.today():
        raise ExpiredDateException()
    return value


class CardType(enum.Enum):
    VISA = 'VISA'
    MASTER_CARD = 'MASTER_CARD'
    UZCARD = 'UZCARD'
    HUMO = 'HUMO'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class CreditCardModel(models.Model):
    number = models.CharField(max_length=20)
    expire_date = models.DateField(validators=[validate_expire_date])
    security_code = models.CharField(max_length=6)
    card_type = models.CharField(max_length=20, choices=CardType.choices())
    holder = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    class Meta:
        app_label = "accounts"

