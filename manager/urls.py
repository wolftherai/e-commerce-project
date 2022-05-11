from django.urls import path, include
from .views import ProductFrontendAPIView, ProductBackendAPIView, LinkAPIView, StatsAPIView, RankingsAPIViewWithoutRedis, LinkAPIViewNotAuthenticated
#from .views import ManagerAPIView, ProductGenericAPIView, LinkAPIView, OrderAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('products/frontend', ProductFrontendAPIView.as_view()),
    path('products/backend', ProductBackendAPIView.as_view()),
    #path('cart', LinkAPIViewNotAuthenticated.as_view()),  # LinkAPIViewNotAuthenticated
    path('links', LinkAPIView.as_view()),
    path('stats', StatsAPIView.as_view()),
    path('rankings', RankingsAPIViewWithoutRedis.as_view())
]