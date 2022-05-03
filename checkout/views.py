from django.db import transaction
from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.authentication import JWTAuthentication

import decimal
from .serializers import LinkSerializer
from core.models import Product, Link, Order, OrderItem, User


class LinkAPIView(APIView):
  #  authentication_classes = [JWTAuthentication]  # try to authenticate user
  #  permission_classes = [IsAuthenticated]

    def get(self, _, code=''):
        link = Link.objects.filter(code=code).first()
        serializer = LinkSerializer(link)
        return Response(serializer.data)


class OrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        link = Link.objects.filter(code=data['code']).first()

        if not link:
            raise exceptions.APIException('Invalid code!')
        try:

            order = Order()
            order.code = link.code
            order.user_id = link.user.id
            order.manager_email = link.user.email
            order.first_name = data['first_name']
            order.last_name = data['last_name']
            order.email = data['email']
            order.address = data['address']
            order.country = data['country']
            order.city = data['city']
            order.zip = data['zip']
            #with transaction.atomic():
            order.save()
            for item in data['products']:
                product = Product.objects.filter(pk=item['product_id']).first()
                quantity = decimal.Decimal(item['quantity'])

                order_item = OrderItem()
                order_item.order = order
                order_item.product_title = product.title
                order_item.price = product.price
                order_item.quantity = quantity
                order_item.manager_revenue = decimal.Decimal(.1) * product.price * quantity
                order_item.admin_revenue = decimal.Decimal(.9) * product.price * quantity
                order_item.save()
                #with transaction.atomic():
                order_item.save()

            return Response({
                'message': 'success'
            })

        except Exception:
            transaction.rollback()
            return Response({
                'message': 'Error occurred!'
            })
