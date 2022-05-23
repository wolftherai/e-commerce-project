import stripe
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.authentication import JWTAuthentication



import decimal

from app.settings import *
from .serializers import LinkSerializer
from core.models import Product, Link, Order, OrderItem, User


class LinkAPIView(APIView):
    # authentication_classes = [JWTAuthentication]  # try to authenticate user
    # permission_classes = [IsAuthenticated]

    def get(self, _, code=''):
        link = Link.objects.filter(code=code).first()
        serializer = LinkSerializer(link)
        return Response(serializer.data)


class OrderAPIView(APIView):

    @transaction.atomic  # help to insert only correct orders
    def post(self, request):
        data = request.data
        link = Link.objects.filter(code=data['code']).first()

        if not link:
            raise exceptions.APIException('Invalid code!')
        try:

            order = Order()
            order.link = link
            order.code = link.code
            order.user_id = link.user.id
            user = User.objects.filter(pk=link.user.id).first()
            if user.is_manager:
                order.manager_email = user.email
            order.first_name = data['first_name']
            order.last_name = data['last_name']
            order.email = data['email']
            order.address = data['address']
            order.country = data['country']
            order.city = data['city']
            order.zip = data['zip']
            # with transaction.atomic():
            order.save()

            line_items = []

            for item in data['products']:
                product = Product.objects.filter(pk=item['product_id']).first()
                quantity = decimal.Decimal(item['quantity'])
                # order item
                order_item = OrderItem()
                order_item.order = order
                order_item.product = product  #
                order_item.product_title = product.title
                order_item.price = product.price
                order_item.quantity = quantity
                if user.is_manager:
                    order_item.manager_revenue = decimal.Decimal(.1) * product.price * quantity
                    order_item.admin_revenue = decimal.Decimal(.9) * product.price * quantity
                else:
                    order_item.admin_revenue = decimal.Decimal(1.0) * product.price * quantity
                    order_item.manager_revenue = 0
                order_item.save()
                # with transaction.atomic():
                #order_item.save()

                # stripe data for checkout
                line_items.append({
                    'name': product.title,
                    'description': ('OEM:'+product.oem_part_number + '\n' + product.description),
                    'images': [
                        product.image
                    ],
                    'amount': int(100 * product.price),  # in cents
                    'currency': 'eur',
                    'quantity': quantity
                })
            stripe.api_key = 'sk_test_51KvJovG0fTE2q5oUVwt7EN0BGAQKvACTE9hYSH2GPvgufjuB8hOb8FfxKdKFgh23XikA16inMf2XEKdRoK6hMTsY00BjslDPRw'
            source = stripe.checkout.Session.create(
                success_url='http://localhost:5000/success?source={CHECKOUT_SESSION_ID}',  # redirects in order to confirm order
                cancel_url='http://localhost:5000/error',
                payment_method_types=['card'],
                line_items=line_items
            )

            order.transaction_id = source['id']
            order.save()

            return Response(source)

        except Exception:
            transaction.rollback()
            return Response({
                'message': 'Error occurred!'
            })


class OrderConfirmedAPIView(APIView):

    def post(self, request):
        order = Order.objects.filter(transaction_id=request.data['source']).first()
        if not order:
            raise exceptions.APIException('Order not found!')

        order.complete = 1
        order.save()

        # Customer Email
        send_mail(
            subject='An Order has been completed',
            message='Order #' + str(order.id) + 'with a total of € ' + str(order.order_price) + ' has been completed!',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[order.email]
        )

        # Manager

        send_mail(
            subject='An Order has been completed',
            message='Order #' + str(order.id) + 'with a total of € ' + str(order.manager_revenue) + ' has been completed!' + ' From link #' + str(order.code),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[DEFAULT_FROM_EMAIL, order.manager_email]
        )

        return Response({
            'message': 'success'
        })
