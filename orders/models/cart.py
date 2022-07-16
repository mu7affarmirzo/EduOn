from django.db import models

from accounts.models import Account
from courses.models.courses import CourseModel


class CartItemModel(models.Model):
    user = models.ForeignKey(Account,
                             on_delete=models.SET_NULL, null=True)
    ordered = models.BooleanField(default=False)
    course = models.ForeignKey(CourseModel, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.course.name}"

    def get_total_item_price(self):
        return self.quantity * self.course.price

    def get_total_discount_item_price(self):
        return self.quantity * self.course.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.course.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class CartModel(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(CourseModel, on_delete=models.SET_NULL, null=True)
    is_referral = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.owner.get_username())}"

    class Meta:
        unique_together = ('owner', 'course',)

