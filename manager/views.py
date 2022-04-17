import math

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Product
from .serializers import ProductSerializer
from django.core.cache import cache
import time


class ProductFrontendAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2, key_prefix='products_frontend'))  # caching the whole page
    def get(self, _):
        time.sleep(2)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductBackendAPIView(APIView):

    def get(self, request):
        products = cache.get('products_backend')
        if not products:  # if products not set, load to cache
            time.sleep(2)  # imitate calculations
            products = list(Product.objects.all())
            cache.set('products_backend', products, timeout=60*30)  # 30 min timeout

        s = request.query_params.get('s', '')  # products filtering (search)
        if s:
            products = list([
                p for p in products
                if (s.lower() in p.title.lower() or (s.lower() in p.description.lower()))
            ])

        total = len(products)

        sort = request.query_params.get('sort', None)
        if sort == 'asc':
            products.sort(key=lambda p: p.price)  # sort by the price ascending
        elif sort == 'desc':
            products.sort(key=lambda p: p.price, reverse=True)  # sort by the price descending

        # pages pagination
        per_page = 9  # values
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        data = ProductSerializer(products[start:end], many=True).data  # after filtering add .data
        return Response({
            'data': data,
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total / per_page)
            }
        })
