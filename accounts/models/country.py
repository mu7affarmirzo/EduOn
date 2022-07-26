from django.db import models


class CountryModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = "accounts"


class ProvinceModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = "accounts"


class DistrictModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    province = models.ForeignKey(ProvinceModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = "accounts"
