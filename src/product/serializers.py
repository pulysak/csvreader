from rest_framework.serializers import ModelSerializer
from .models import Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('sku', 'name', 'barcode', 'photo_url', 'price', 'producer')
