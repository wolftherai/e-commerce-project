from rest_framework import serializers

from core.models import Product, Link, User #, OrderItem, Order

from common.serializers import UserSerializer


class Meta:
    model = User
    # fields = '__all__' #use all fields
    fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_manager']
    extra_kwargs = {
        'password': {'write_only': True}  # don't need to retrieve the password after creation
    }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # use all fields


class LinkSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Link
        fields = '__all__'  # use all fields