from rest_framework import serializers
from core.models import Product, Link, OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' #use all fields


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__' #use all fields


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__' #use all fields


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        items = OrderItem.onjects.filter(order_id=obj.id)
        return sum((o.price * o.quantity) for o in items)  # get order sum

    class Meta:
        model = Order
        fields = '__all__' #use all fields