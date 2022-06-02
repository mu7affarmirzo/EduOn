from django.contrib import admin
from orders.models.cart import CartModel, CartItemModel


admin.site.register(CartModel)
admin.site.register(CartItemModel)
