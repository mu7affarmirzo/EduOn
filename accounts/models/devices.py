from django.db import models

from accounts.models import Account


class DeviceModel(models.Model):
    device_name = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    imei = models.CharField(max_length=255, blank=True, null=True)
    mac = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    long = models.CharField(max_length=255, blank=True, null=True)
    firebase_reg_id = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='owner_devices')

    def __str__(self):
        return str(self.device_name)
