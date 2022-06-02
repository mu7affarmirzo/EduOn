from django.urls import path, include

urlpatterns = [
    path('accounts/', include('api.v1.accounts.urls')),
    path('courses/', include('api.v1.courses.urls')),
    path('orders/', include('api.v1.orders.urls')),
]
