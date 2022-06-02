from django.urls import path, include
from api.v1.orders.views import CartListView, CartDetailView

app_name = 'orders'

urlpatterns = [
    path('cart', CartListView.as_view(), name='cart'),
    path('cart-remove/<int:pk>', CartDetailView.as_view(), name='cart-remove'),
]
