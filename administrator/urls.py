from django.urls import path, include

from .views import ManagerAPIView, ProductGenericAPIView, LinkAPIView, OrderAPIView,\
    CategoryGenericAPIView, BrandGenericAPIView, ManufacturerGenericAPIView, OemPartAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('managers', ManagerAPIView.as_view()),

    path('products', ProductGenericAPIView.as_view()),
    path('products/<str:pk>', ProductGenericAPIView.as_view()),  # products with primary key

    path('categories', CategoryGenericAPIView.as_view()),
    path('categories/<str:pk>', CategoryGenericAPIView.as_view()),  # products with primary key

    path('brands', BrandGenericAPIView.as_view()),
    path('brands/<str:pk>', BrandGenericAPIView.as_view()),  # products with primary key

    path('manufacturers', ManufacturerGenericAPIView.as_view()),
    path('manufacturers/<str:pk>', ManufacturerGenericAPIView.as_view()),  # products with primary key

    path('oem_parts', OemPartAPIView.as_view()),

    path('users/<str:pk>/links', LinkAPIView.as_view()),  # user with primary key
    path('orders', OrderAPIView.as_view()),

]