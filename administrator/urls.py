from django.urls import path, include

from .views import ManagerAPIView, ProductGenericAPIView, LinkAPIView, OrderAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('managers', ManagerAPIView.as_view()),
    path('products', ProductGenericAPIView.as_view()),
    path('products/<str:pk>', ProductGenericAPIView.as_view()), #products with primary key
    path('users/<str:pk>/links', LinkAPIView.as_view()), #products with primary key
    path('orders', OrderAPIView.as_view()), #products with primary key
]