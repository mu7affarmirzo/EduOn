from rest_framework import serializers

from api.v1.courses.serializers import CourseSerializer
from orders.models.cart import CartModel


class CartSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='get_price')

    class Meta:
        model = CartModel
        fields = ['price', 'is_referral', 'course']

    def get_price(self, obj):
        return obj.course.price


class CartItemsSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='get_price')
    course = CourseSerializer()

    class Meta:
        model = CartModel
        fields = ['id', 'price', 'is_referral', 'course']

    def get_price(self, obj):
        return obj.course.price


class CartSummarySerializer(serializers.Serializer):
    items = CartItemsSerializer(many=True, default=None)
    total = serializers.SerializerMethodField(method_name='get_total', default=0.0, source=items)

    def get_total(self, obj):
        sum = 0
        print(len(obj['items']))
        for i in obj['items']:
            sum += i.course.price
        return sum

    class Meta:
        fields = '__all__'

