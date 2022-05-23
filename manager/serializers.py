from rest_framework import serializers
from core.models import Product, Link , OemPart#, Link, OrderItem, Order

from administrator.serializers import OemPartSerializer


class OemPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = OemPart
        fields = '__all__' #use all fields


class ProductSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.SerializerMethodField('get_manufacturer_name')
    brand_name = serializers.SerializerMethodField('get_brand_name')
    category_name = serializers.SerializerMethodField('get_category_name')
    oem_part_code = serializers.SerializerMethodField('get_oem_part_code')
    #car_models = serializers.SerializerMethodField('get_oem_car_models')
#    car_models = OemPart.objects
    oem_part = OemPartSerializer()#many=False

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
    class Meta:
        model = Link
        fields = '__all__'  # use all fields