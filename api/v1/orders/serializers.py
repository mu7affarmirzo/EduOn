from rest_framework import serializers
from orders.models.cart import CartModel, CartItemModel


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = ['id', 'course']
