from django.urls import path, include
from .views import ProductFrontendAPIView, ProductBackendAPIView
#from .views import ManagerAPIView, ProductGenericAPIView, LinkAPIView, OrderAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('products/frontend', ProductFrontendAPIView.as_view()),
    path('products/backend', ProductBackendAPIView.as_view()),
]