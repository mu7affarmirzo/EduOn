from django.urls import path, include

urlpatterns = [
    path('accounts/', include('api.v2.accounts.urls')),
    path('courses/', include('api.v2.courses.urls')),
    path('orders/', include('api.v2.orders.urls')),
    path('wallet/', include('api.v2.wallet.urls')),
]
