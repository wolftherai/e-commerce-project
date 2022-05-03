from django.urls import path, include
from .views import LinkAPIView, OrderAPIView, OrderConfirmedAPIView
urlpatterns = [
    path('links/<str:code>', LinkAPIView.as_view()),
    path('orders', OrderAPIView.as_view()),
    path('orders/confirm', OrderConfirmedAPIView.as_view()),
]