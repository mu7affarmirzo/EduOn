import random

from django.db import models
from accounts.models.account import Account

from django.db.models.signals import post_save
from django.dispatch import receiver


class CodeModel(models.Model):
    number = models.CharField(max_length=5, null=True, blank=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        digits_list = [x for x in range(10)]
        code_items =[]
        for i in range(5):
            num = random.choice(digits_list)
            code_items.append(num)

        code_str = "".join(str(code) for code in code_items)
        self.number = code_str

        super().save(*args, **kwargs)


@receiver(signal=post_save, sender=Account)
def post_save_verification_code(sender, instance, created, *args, **kwargs):
    if created:
        CodeModel.objects.create(account=instance)
