from rest_framework import serializers
from core.models import Product, Link #, Link, OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' #use all fields


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'  # use all fields