import math, random, time
import string

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Product, Link, Order, User

from common.authentication import JWTAuthentication

from .serializers import ProductSerializer, LinkSerializer
from django.core.cache import cache


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
                if (s.lower() in p.title.lower() or (s.lower() in p.description.lower()) or (s.lower() in p.oem_part_number.lower()))
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


class LinkAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = LinkSerializer(data={
            'user': user.id,  # many to many connection
            'code': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),  # random string with letters and digits
            'products': request.data['products']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# basket type update
    def put(self, request):
        # response = self.partial_update(request, pk)  # updates only fields that are sent
        user = request.user
        serializer = LinkSerializer(user, data={
            'user': user.id,  # many to many connection
            'code': request.data['code'],
            'products': request.data['products']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()  # save changes

        return Response(serializer.data)


class LinkAPIViewNotAuthenticated(APIView):

    def post(self, request):
       # user = request.user
        serializer = LinkSerializer(data={
           # 'user': user.id,  # many to many connection
            'code': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),  # random string with letters and digits
            'products': request.data['products']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StatsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        links = Link.objects.filter(user_id=user.id) #get all links for user_id

        return Response([(self.format(link)) for link in links])  # loop through links

    def format(self, link):
        orders = Order.objects.filter(code=link.code, complete=1)  # get all completed orders with this code and revenue fields

        return {
            'id': link.id,
            'code': link.code,
            'count': len(orders),
            'revenue': sum(o.manager_revenue for o in orders)
        }


class RankingsAPIViewWithoutRedis(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        managers = User.objects.filter(is_manager=True)

        response = list({
            'name': a.name,
            'revenue': a.revenue
        } for a in managers)

        response.sort(key=lambda a: a['revenue'], reverse=True)

        return Response(response)


class RankingsAPIViewWithRedis(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        con = get_redis_connection("default")

        rankings = con.zrevrangebyscore('rankings', min=0, max=99999, withscores=True)  # sort data descending

        return Response({
            r[0].decode("utf-8"): r[1] for r in rankings
        })
