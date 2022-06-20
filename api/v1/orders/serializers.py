from rest_framework import serializers
from orders.models.cart import CartModel, CartItemModel


class CartSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='get_price')
    class Meta:
        model = CartModel
        fields = ['id', 'course', 'price']

    def get_price(self, obj):
        return obj.course.price


class CartSummarySerializer(serializers.Serializer):
    items = CartSerializer(many=True, default=None)
    total = serializers.SerializerMethodField(method_name='get_total', default=0.0, source=items)

    def get_total(self, obj):
        sum = 0
        for i in obj['items']:
            sum += i.course.price
        return sum

    class Meta:
        fields = '__all__'

