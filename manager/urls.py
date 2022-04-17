from django.urls import path, include

#from .views import ManagerAPIView, ProductGenericAPIView, LinkAPIView, OrderAPIView

urlpatterns = [
    path('', include('common.urls')),
#    path('managers', ManagerAPIView.as_view()),
]