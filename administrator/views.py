from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.serializers import UserSerializer
from common.authentication import JWTAuthentication
from administrator.serializers import ProductSerializer, LinkSerializer, OrderSerializer
from core.models import User, Product, Link, Order
from django.core.cache import cache


class ManagerAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def get(self, _):
        managers = User.objects.filter(is_manager=True).order_by('-id')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data)


class ProductGenericAPIView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # serialize products

    def get(self, request, pk=None):  # if pk is not set we take all the products
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)

    def post(self, request):
        response = self.create(request)  # create products
        for key in cache.keys('*'):  # search in all keys (frontend) and delete cache after changes
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)  # updates only fields that are sent
        for key in cache.keys('*'):  # search in all keys and delete cache after changes
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response

    def delete(self, request, pk=None):
        response = self.destroy(request, pk)  # deletes only fields that are sent
        for key in cache.keys('*'):  # search in all keys and delete cache after changes
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response


class LinkAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        links = Link.objects.filter(user_id=pk)
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data)

class OrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(complete=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

