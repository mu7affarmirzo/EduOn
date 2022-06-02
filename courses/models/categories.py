from django.db import models


class CategoriesModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategoriesModel(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(CategoriesModel, related_name='subcategory', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
