from rest_framework import serializers
from core.models import Product, Link, OrderItem, Order, Manufacturer, Category, Brand, OemPart


class ProductSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.SerializerMethodField('get_manufacturer_name')
    brand_name = serializers.SerializerMethodField('get_brand_name')
    category_name = serializers.SerializerMethodField('get_category_name')
    oem_part_code = serializers.SerializerMethodField('get_oem_part_code')

    def get_manufacturer_name(self, obj):
        return obj.manufacturer_name

    def get_brand_name(self, obj):
        return obj.brand_name

    def get_category_name(self, obj):
        return obj.category_name

    def get_oem_part_code(self, obj):
        return obj.oem_part_code

    class Meta:
        model = Product
        fields = '__all__' #use all fields


class LinkSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField('get_orders')  # gets orders

    def get_orders(self, obj):
        return OrderSerializer(Order.objects.filter(code=obj.code), many=True).data

    class Meta:
        model = Link
        fields = '__all__' #use all fields


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__' #use all fields


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' #use all fields


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__' #use all fields


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__' #use all fields


class OemPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = OemPart
        fields = '__all__' #use all fields


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField('get_total')
    customer_name = serializers.SerializerMethodField('get_customer_name')

    def get_total(self, obj):
        items = OrderItem.objects.filter(order_id=obj.id)
        return sum((o.price * o.quantity) for o in items)  # get order sum

    def get_customer_name(self, obj):
        return obj.customer_name

    class Meta:
        model = Order
        fields = '__all__'  # use all fields